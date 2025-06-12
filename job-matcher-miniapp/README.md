# Resume Description Match App

Analyzes resumes and matches them to job descriptions using Firecrawl and Anthropic APIs. The app provides detailed job matching with  scoring based on experience recency, skill relevance, and role alignment.

## Features

- **Multi-format Resume Support**
  - PDF files
  - Microsoft Word documents (DOCX)
  - Plain text files
  - LaTeX files

- **Intelligent Job Search**
  - Targets reputable job boards (Greenhouse, Lever, Ashby, Work at a Startup)
  - Remote job filtering
  - Industry/term exclusion
  - Customizable result limits

- **Sophisticated Matching Algorithm**
  - Experience recency scoring (40%)
  - Skill relevance matching (40%)
  - Role alignment analysis (20%)
  - Detailed match breakdowns

- **Comprehensive Output**
  - Console progress indicators
  - Detailed match reports
  - Timestamped output files
  - Skill matching analysis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resume-description-match-app.git
cd resume-description-match-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with your API keys:
```
ANTHROPIC_API_KEY=your_anthropic_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

## Usage

Basic usage:
```bash
python match-app.py --resume path/to/your/resume.pdf
```

### Command Line Options

- `--resume`: Path to your resume file (required)
  - Supported formats: PDF, DOCX, TXT, LaTeX
  - Example: `--resume my_resume.pdf`

- `--max-jobs`: Maximum number of jobs to match (default: 10)
  - Example: `--max-jobs 20`

- `--remote`: Include only remote jobs
  - Example: `--remote`

- `--exclude`: Terms to exclude from search
  - Example: `--exclude intern crypto`

### Example Commands

1. Basic job matching:
```bash
python match-app.py --resume resume.pdf
```

2. Remote jobs only:
```bash
python match-app.py --resume resume.pdf --remote
```

3. Exclude specific terms:
```bash
python match-app.py --resume resume.pdf --exclude intern crypto
```

4. Custom number of results:
```bash
python match-app.py --resume resume.pdf --max-jobs 20
```

## Match Score Calculation

The app uses a sophisticated scoring system to evaluate job matches:

### Experience Recency (40%)
- Current role: 40 points
- Last year: 30 points
- Last 2 years: 20 points
- Last 3 years: 10 points
- Over 3 years: 5 points

### Skill Match (40%)
- Required skills: 25 points each
- Preferred skills: 15 points each
- Bonus for frequent use: +5 points
- Bonus for current role: +10 points

### Role Alignment (20%)
- Title match: 10 points
- Industry match: 5 points
- Level match: 5 points

## Output

The app generates two types of output:

1. **Console Output**
   - Progress indicators
   - Search query details
   - Match results summary

2. **Text File**
   - Timestamped output file
   - Detailed match analysis
   - Skill matching breakdown
   - Company information

## Dependencies

- firecrawl
- langchain-anthropic
- python-dotenv
- python-docx
- PyPDF2
- pylatexenc
- tqdm

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Firecrawl API for job search capabilities
- Anthropic API for resume analysis and matching
- All contributors who have helped improve this tool 
