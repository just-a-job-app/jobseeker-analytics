import argparse
import asyncio
import os
from tqdm import tqdm
from firecrawl import FirecrawlApp, ScrapeOptions
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.json import SimpleJsonOutputParser
from docx import Document
from PyPDF2 import PdfReader
from pylatexenc import latex2text
from dotenv import load_dotenv
from typing import Dict, List
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

class ResumeJobMatcher:
    def __init__(self):
        # Get API keys from environment variables
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
        
        if not anthropic_api_key or not firecrawl_api_key:
            raise ValueError("Missing API keys. Please ensure ANTHROPIC_API_KEY and FIRECRAWL_API_KEY are set in your .env file")

        self.firecrawl = FirecrawlApp()
        self.llm = ChatAnthropic(model="claude-3-7-sonnet-20250219", temperature=0)

        # Schema for resume analysis
        self.resume_schema = {
            "job_titles": List[str],
            "skills": List[str],
            "search_query": str
        }

        # Schema for job matching
        self.job_match_schema = {
            "match_score": int,
            "matching_skills": List[str],
            "missing_skills": List[str],
            "company_description": str
        }

        # Prompt for resume analysis
        self.resume_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are an expert resume analyzer. Analyze the resume and identify relevant job titles, skills, and create a search query to find matching jobs.",
            ),
            (
                "human",
                """
Resume:
{resume}

Exclude terms: {exclude_terms}

Analyze this resume and provide a JSON response with:
1. List of job titles that match the candidate's experience
2. List of key skills identified
3. A Google-style search query to find matching jobs. The query should:
   - Include site: operators for reputable job boards like:
     * site:boards.greenhouse.io
     * site:lever.co
     * site:jobs.ashbyhq.com
     * site:workatastartup.com
   - Use OR between different job boards
   - Focus on the most relevant skills and titles
   - Be concise but specific
   - Exclude any jobs containing the specified terms using -term syntax
   - If exclude_terms is empty, no exclusions are needed

Format the response as a JSON object with these exact keys: job_titles, skills, search_query

Example search query format with exclusions:
(skill1 AND skill2) site:(boards.greenhouse.io OR lever.co OR jobs.ashbyhq.com OR workatastartup.com) -intern -crypto
""",
            ),
        ])

        # Prompt for job matching
        self.job_match_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are an expert job matcher. Analyze the resume against the job posting and provide a detailed match analysis, considering both recency and frequency of relevant experience. Calculate match scores based on specific criteria and weights.",
            ),
            (
                "human",
                """
Resume:
{resume}

Job Posting:
{job_posting}

Analyze the match between this resume and job posting. Calculate the match score using these specific criteria:

1. Experience Recency (40% of total score):
   - Current role: 40 points
   - Last 1 year: 30 points
   - Last 2 years: 20 points
   - Last 3 years: 10 points
   - Over 3 years: 5 points
   Multiply by 0.4 for final recency score

2. Skill Match (40% of total score):
   - Required skills present: 25 points per skill
   - Preferred skills present: 15 points per skill
   - Skills used frequently in resume: +5 points per skill
   - Skills used in current role: +10 points per skill
   Multiply by 0.4 for final skill score

3. Role Alignment (20% of total score):
   - Title match: 10 points
   - Industry match: 5 points
   - Level match (junior/mid/senior): 5 points
   Multiply by 0.2 for final alignment score

Final score = (Recency Score + Skill Score + Alignment Score)
Round to nearest integer.

Provide a JSON response with:
1. Overall match score (0-100) calculated using the above formula
2. List of matching skills with their recency and points earned
3. List of missing skills
4. Brief company description

Format the response as a JSON object with these exact keys: match_score, matching_skills, missing_skills, company_description

Example matching_skills format with points:
["Python", "Django", "AWS"]
""",
            ),
        ])

        self.resume_parser = SimpleJsonOutputParser()
        self.job_match_parser = SimpleJsonOutputParser()

    async def analyze_resume(self, resume: str, include_remote: bool = False, exclude_terms: List[str] = None) -> Dict:
        """Analyze resume and generate search query."""
        formatted_prompt = self.resume_prompt.format(
            resume=resume,
            exclude_terms=", ".join(exclude_terms) if exclude_terms else "none"
        )
        response = await self.llm.ainvoke(formatted_prompt)
        result = self.resume_parser.parse(response.content)
        
        # Add remote as an AND search term if specified
        if include_remote:
            # Check if the query already has AND conditions
            if " AND " in result["search_query"]:
                result["search_query"] = f"{result['search_query']} AND remote"
            else:
                # If no AND conditions, wrap the existing query in parentheses
                result["search_query"] = f"({result['search_query']}) AND remote"
        
        return result

    async def parse_resume(self, resume_path: str) -> str:
        """Parse resume from various file formats."""
        file_ext = os.path.splitext(resume_path)[1].lower()
        
        try:
            if file_ext == '.txt':
                with open(resume_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif file_ext == '.pdf':
                reader = PdfReader(resume_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
            
            elif file_ext == '.docx':
                doc = Document(resume_path)
                return "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            elif file_ext in ['.tex', '.ltx']:
                with open(resume_path, 'r', encoding='utf-8') as f:
                    latex_content = f.read()
                converter = latex2text()
                return converter.convert(latex_content)
            
            else:
                raise ValueError(f"Unsupported file format: {file_ext}. Supported formats are: .txt, .pdf, .docx, .tex, .ltx")
        
        except Exception as e:
            raise Exception(f"Error parsing resume file: {str(e)}")

    async def search_jobs(self, query: str, max_results: int = 10):
        """Search for jobs using Firecrawl."""
        # Search for more results than needed to allow for filtering
        search_limit = max_results * 3  # Get 3x more results for filtering
        
        response = self.firecrawl.search(
            query=query,
            limit=search_limit,
            scrape_options=ScrapeOptions(formats=["markdown", "links"])
        )
        
        jobs = []
        # Process search results directly
        for result in response.data:
            jobs.append({
                "title": result["title"],
                "url": result["url"],
                "description": result.get("markdown", ""),
                "company_info": result.get("description", ""),  # Use description as company info
            })
        return jobs

    async def match_resume_to_job(self, resume: str, job: dict) -> dict:
        """Match resume to a job posting."""
        formatted_prompt = self.job_match_prompt.format(
            resume=resume,
            job_posting=job["description"],
        )
        response = await self.llm.ainvoke(formatted_prompt)
        return self.job_match_parser.parse(response.content)

    async def run(self, resume_path: str, max_jobs: int = 10, include_remote: bool = False, exclude_terms: List[str] = None):
        """Run the complete matching process."""
        print("\n=== Starting Resume Analysis ===")
        # Parse and analyze resume
        resume = await self.parse_resume(resume_path)
        resume_analysis = await self.analyze_resume(resume, include_remote, exclude_terms)
        
        print("\n=== Resume Analysis Results ===")
        print(f"Identified Job Titles: {', '.join(resume_analysis['job_titles'])}")
        print(f"Key Skills: {', '.join(resume_analysis['skills'])}")
        print(f"\nGenerated Search Query: {resume_analysis['search_query']}")
        if exclude_terms:
            print(f"Excluding terms: {', '.join(exclude_terms)}")
        
        print("\n=== Searching for Jobs ===")
        # Search for jobs using the generated query
        jobs = await self.search_jobs(resume_analysis["search_query"], max_results=max_jobs)
        print(f"Found {len(jobs)} potential jobs")
        
        print("\n=== Matching Jobs to Resume ===")
        # Match resume to each job
        results = []
        for job in tqdm(jobs, desc="Matching jobs"):
            try:
                match_result = await self.match_resume_to_job(resume, job)
                # Ensure we have a valid match score
                if match_result and isinstance(match_result.get("match_score"), (int, float)):
                    results.append({
                        "job_title": job["title"],
                        "job_url": job["url"],
                        **match_result
                    })
            except Exception as e:
                print(f"Warning: Failed to match job {job['title']}: {str(e)}")
                continue
        
        # Sort results by match score, filtering out any None scores
        results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        final_results = results[:max_jobs]  # Return only the top N matches
        
        # Save results to file
        self.save_results_to_file(final_results, resume_path)
        
        return final_results

    def save_results_to_file(self, results: List[Dict], resume_path: str):
        """Save matching results to a text file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        resume_name = os.path.splitext(os.path.basename(resume_path))[0]
        output_file = f"job_matches_{resume_name}_{timestamp}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== Job Matching Results ===\n\n")
            for result in results:
                f.write(f"Job: {result['job_title']}\n")
                f.write(f"URL: {result['job_url']}\n")
                f.write(f"Match Score: {result['match_score']}%\n")
                f.write(f"Company: {result['company_description']}\n")
                f.write("\nMatching Skills:\n")
                for skill in result['matching_skills']:
                    f.write(f"✅ {skill}\n")
                f.write("\nMissing Skills:\n")
                for skill in result['missing_skills']:
                    f.write(f"❌ {skill}\n")
                f.write("-" * 80 + "\n\n")
        
        print(f"\nResults saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Resume to Job Description Matcher")
    parser.add_argument("--resume", required=True, help="Path to resume file (supported formats: .txt, .pdf, .docx, .tex, .ltx)")
    parser.add_argument("--max-jobs", type=int, default=10, help="Max number of jobs to match")
    parser.add_argument("--remote", action="store_true", help="Include remote jobs in search")
    parser.add_argument("--exclude", nargs="+", help="Terms to exclude from search (e.g., intern crypto)")
    args = parser.parse_args()

    matcher = ResumeJobMatcher()
    results = asyncio.run(matcher.run(args.resume, args.max_jobs, args.remote, args.exclude))

    # Print results to console
    print("\n=== Top Matching Jobs ===")
    for result in results:
        print(f"\nJob: {result['job_title']}")
        print(f"URL: {result['job_url']}")
        print(f"Match Score: {result['match_score']}%")
        print(f"Company: {result['company_description']}")
        print("\nMatching Skills:")
        for skill in result['matching_skills']:
            print(f"✅ {skill}")
        print("\nMissing Skills:")
        for skill in result['missing_skills']:
            print(f"❌ {skill}")
        print("-" * 80)

if __name__ == "__main__":
    main()