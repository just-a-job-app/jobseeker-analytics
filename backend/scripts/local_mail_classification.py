import json
from transformers import pipeline
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import re
from typing import List
import argparse


class EmailClassifierAgent:
    """
    An agent that classifies emails using a zero-shot classification model.
    """

    def __init__(self, model_name: str = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"):
        """
        Initializes the EmailClassifierAgent with a specified model.
        
        Args:
            model_name (str): The name of the model to use for classification.
        """
        self.device = 0 if torch.cuda.is_available() else -1
        print(f"Using device: {'cuda' if self.device == 0 else 'cpu'}")
        self.classifier = pipeline(
            "zero-shot-classification",
            model=model_name,
            device=self.device
        )

        self.candidate_labels = [
            "Closed – Rejection / Freeze / Withdrawn",
            "Offer / Paperwork",
            "Interview Invitation or Assessment sent",
            "Initial Contact / Application Received",
            "Offer Declined / Other"
        ]

        self.label_map = {
            "Rejection": [
                "Rejection"
            ],
            "Other": ["Offer made", "Hiring freeze notification",
                "Withdrew application", "Informational Outreach"],
            "Interview Invitation": [
                "Interview invitation"
            ],
            "Application confirmation": ["Application confirmation"],
            "Assessment sent": ["Assessment sent"],
            "Availability request": ["Availability request"],
            "Action required from company": ["Action required from company"],
            "Did not apply - inbound request": ["Did not apply - inbound request"],
            "Information request": ["Information request"]
        }

    def extract_latest_email(self, text: str) -> str:
        """
        Given the *full* body text of a threaded e-mail,
        return only the newest (top-most) message.

        Heuristics
        ----------
        1.  Keep everything that appears *before* the first
            "reply / forward / quoted" marker.
        2.  Strip common footers and long dash lines.
        3.  Collapse extra whitespace.

        Works well on:
          •  '--- original message ---' blocks
          •  "On Tue, 5 Mar 2025 … wrote:" quotes
          •  Outlook "From: / Sent:" headers
          •  LinkedIn InMail footers
        """
        if not text:
            return text

        # normalise line endings
        text_norm = text.replace("\r\n", "\n")

        # ---------- 1.  find the first sign of an older message ----------
        split_markers = [
            r"\n-{2,}\s*original message\s*-{2,}",        # --- original message ---
            r"\n-{4,}\s*forwarded message\s*-{4,}",       # ---- Forwarded message ----
            r"\n-{2,}\s*end of original message\s*-{2,}",
            r"\nOn .{10,200}wrote:",                      # On Mon, … wrote: (removed ? after })
            r"\nFrom:\s.+\n?Sent:\s",                     # Outlook header
            r"\nMessage replied:",                        # LinkedIn InMail threads
            r"\n>\s",                                     # Lines starting with > (quoted text)
            r"On [A-Z][a-z]{2}, .{5,50} at .{5,20} .{5,50} wrote:",  # On Thu, Feb 1, 2024 at 4:45 PM Name wrote: (removed \n at start)
            r"On \w{3}, \w{3} \d{1,2}, \d{4} at \d{1,2}:\d{2} [AP]M .+ wrote:",  # Another date format (removed \n at start)
            r"\n\s*--\s*\n",                             # Email signature separator
            r"\nSent from my (iPhone|Android|mobile)",    # Mobile signatures
            r"\nGet Outlook for (iOS|Android)",           # Outlook mobile signatures
            r"original message",                          # Simple "original message" anywhere
            r"wrote:",                                    # Simple "wrote:" pattern
        ]

        cut_at = len(text_norm)
        for pat in split_markers:
            m = re.search(pat, text_norm, flags=re.IGNORECASE)
            if m:
                cut_at = min(cut_at, m.start())

        head = text_norm[:cut_at]

        # ---------- 2.  remove footers ----------
        footer_markers = [
            r"\n-{20,}",                                 # long "–––––––––" lines
            r"\nThis email was intended",                # LinkedIn footer
            r"\nYou are receiving LinkedIn notification emails",
            r"\nUnsubscribe:", r"\nHelp:",
            r"© \d{4} LinkedIn"
        ]
        for pat in footer_markers:
            m = re.search(pat, head, flags=re.IGNORECASE)
            if m:
                head = head[:m.start()]

        # ---------- 3.  tidy up ----------
        head = re.sub(r"\s+\n", "\n", head)              # trim trailing spaces before newlines
        return head.strip()

    def check_emails_if_job_related(self, subject: str, body: str) -> bool:
        """
        Check if the email text is related to a job application.
        
        Args:
            text (str): The email body text.
        
        Returns:
            bool: True if the email is related to a job application, False otherwise.
        """
        text = f"{subject} {body}"
        candidate_labels = ["Job Related", "Not Job Related"]
        result = self.classifier(text, candidate_labels)
        predicted_label = result['labels'][0]
        
        return predicted_label == "Job Related"

    def classify_email_category(self, text: str) -> tuple:
        """
        Classify a job-related email into specific categories.
        
        Args:
            text (str): The email text to classify.
            
        Returns:
            tuple: (predicted_label, confidence, full_result)
        """
        result = self.classifier(text, self.candidate_labels) 
        predicted_label = result['labels'][0]
        confidence = result['scores'][0]
        
        return predicted_label, confidence, result

    def is_prediction_correct(self, predicted_label: str, actual_label: str) -> bool:
        """
        Check if the predicted label matches the actual label based on label mapping.
        
        Args:
            predicted_label (str): The predicted category label.
            actual_label (str): The actual ground truth label.
            
        Returns:
            bool: True if the prediction is correct, False otherwise.
        """
        return actual_label in self.label_map.get(predicted_label, [])

    def save_wrong_predictions(self, item_data: dict, predicted_label: str, actual_label: str, 
                             confidence: float, result: dict, sequence: str, 
                             f_pred, f_wrong, item_num: int):
        """
        Save wrong predictions to both detailed and simple format files.
        
        Args:
            item_data (dict): The original email item data
            predicted_label (str): The predicted category
            actual_label (str): The actual ground truth label
            confidence (float): The prediction confidence
            result (dict): The full classifier result
            sequence (str): The processed email sequence
            f_pred: File handle for detailed predictions
            f_wrong: File handle for wrong classifications
            item_num (int): Item number for logging
        """
        
        # Save simple wrong classification
        f_wrong.write(f"ID: {item_data.get('id', 'unknown')}\n")
        f_wrong.write(f"Predicted: {predicted_label}\n")
        f_wrong.write(f"Actual: {actual_label}\n")
        f_wrong.write(f"Confidence: {confidence:.3f}\n")
        f_wrong.write(f"Sequence: {sequence[:500]}{'...' if len(sequence) > 500 else ''}\n")
        f_wrong.write("-" * 40 + "\n\n")

    def save_job_related_wrong_prediction(self, item_data: dict, predicted_job_related: bool, 
                                        actual_job_related: bool, email_content: str):
        """
        Save wrong job-related predictions to a separate file.
        
        Args:
            item_data (dict): The original email item data
            predicted_job_related (bool): Predicted job-related status
            actual_job_related (bool): Actual job-related status
            email_content (str): The email content
        """
        with open('wrong_boolean_classification.txt', 'a', encoding='utf-8') as f_bool:
            f_bool.write(f"ID: {item_data.get('id', 'unknown')}\n")
            f_bool.write(f"Email Content: {email_content[:500]}{'...' if len(email_content) > 500 else ''}\n")
            f_bool.write(f"Actual Label: {item_data.get('application_status')}\n")
            f_bool.write(f"Predicted Job-Related: {predicted_job_related}\n")
            f_bool.write(f"Actual Job-Related: {actual_job_related}\n")
            f_bool.write("-" * 40 + "\n\n")


def load_training_data(filename: str = 'training_data_cleaned.json') -> List[dict]:
    """
    Load training data from JSON file.
    
    Args:
        filename (str): The JSON file to load
        
    Returns:
        List[dict]: The loaded data
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded {len(data)} items from {filename}")
        return data
    except FileNotFoundError:
        print(f"Error: {filename} not found in the current directory.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode {filename}. Please check its format.")
        return []


def preprocess_email(agent: EmailClassifierAgent, item: dict) -> tuple:
    """
    Preprocess an email item to extract and clean the content.
    
    Args:
        agent: The EmailClassifierAgent instance
        item: The email item data
        
    Returns:
        tuple: (processed_sequence, was_trimmed)
    """
    body = item.get('body', '')
    original_length = len(body)
    
    # Extract latest email content
    body = agent.extract_latest_email(body)
    was_trimmed = len(body) != original_length
    
    # Create sequence and clean it
    sequence_to_classify = item.get('subject', '') + " " + body
    sequence_to_classify = sequence_to_classify.replace('-', '')
    sequence_to_classify = sequence_to_classify.replace('\n', ' ')
    sequence_to_classify = sequence_to_classify.lower().strip()
    
    return sequence_to_classify, was_trimmed


def process_email_classification(agent: EmailClassifierAgent, data: List[dict]):
    """
    Process and classify emails, calculating accuracy metrics.
    
    Args:
        agent: The EmailClassifierAgent instance
        data: List of email data items
    """
    # Initialize counters
    correct_predictions = 0
    processed_items = 0
    processed_all_items = 0
    job_related_correct = 0
    job_related_total = 0
    total_items_to_process = len(data)

    print(f"Starting classification for {total_items_to_process} items...")

    with open('exp.txt', 'w', encoding='utf-8') as f_out, \
         open('predictions.txt', 'w', encoding='utf-8') as f_pred, \
         open('wrong_classifications.txt', 'w', encoding='utf-8') as f_wrong:
        
        # Clear the wrong boolean classification file
        open('wrong_boolean_classification.txt', 'w').close()
        
        for i, item in enumerate(data):
            # Preprocess email
            sequence_to_classify, was_trimmed = preprocess_email(agent, item)
            actual_label = item.get('application_status')

            if not sequence_to_classify or not actual_label:
                continue

            if was_trimmed:
                print(f"Trimmed mail replay to the latest for ID {item.get('id', 'unknown')}")

            processed_all_items += 1
            
            # Truncate email content to prevent token limit issues
            max_email_length = 512
            truncated_email = sequence_to_classify[:max_email_length]

            # Check if email is job-related
            job_related = agent.check_emails_if_job_related(item.get('subject', ''), truncated_email)
            
            # Track job-related classification accuracy
            job_related_total += 1
            actual_is_job_related = actual_label not in ["False positive, not related to job search", "Not Job-Related"]
            
            if job_related == actual_is_job_related:
                job_related_correct += 1
            else:
                # Save wrong job-related prediction
                agent.save_job_related_wrong_prediction(item, job_related, actual_is_job_related, truncated_email)
            
            print(f"Job-related prediction: {job_related}, Actual: {actual_is_job_related}")

            # Skip non-job-related emails
            if actual_label in ["False positive, not related to job search", "Not Job-Related"]:
                continue

            if not job_related:
                print(f"Skipping item {i + 1} (ID: {item.get('id', 'unknown')}) - Predicted as Not Job Related")
                continue

            processed_items += 1

            # Classify email category
            try:
                predicted_label, confidence, result = agent.classify_email_category(truncated_email)
                
                print(f"Raw classifier output: {result}")
                print(f"Predicted: {predicted_label} (confidence: {confidence:.3f})")
                
            except Exception as e:
                print(f"Error during classification: {e}")
                continue

            # Check if prediction is correct
            is_correct = agent.is_prediction_correct(predicted_label, actual_label)
            
            # Enhanced print output with clear formatting
            print(f"\n--- Item {i + 1} (ID: {item.get('id', 'unknown')}) ---")
            print(f"Predicted Category: {predicted_label}")
            print(f"Actual Label: {actual_label}")
            print(f"Prediction Result: {'✅ CORRECT' if is_correct else '❌ WRONG'}")
            if not is_correct:
                print(f"Expected categories for '{predicted_label}': {agent.label_map.get(predicted_label, [])}")
            print("-" * 60)

            if is_correct:
                correct_predictions += 1
            else:
                # Save wrong predictions
                agent.save_wrong_predictions(item, predicted_label, actual_label, confidence, 
                                           result, sequence_to_classify, f_pred, f_wrong, i + 1)
            
            # Summary line for the log file
            status_emoji = "✅" if is_correct else "❌"
            output_line = f"{status_emoji} Item {i + 1}/{total_items_to_process} -> Predicted: '{predicted_label}' | Actual: '{actual_label}' | Result: {'CORRECT' if is_correct else 'WRONG'}"
            f_out.write(output_line + '\n')

        # Calculate and write final accuracy
        if processed_items > 0:
            accuracy = (correct_predictions / processed_items) * 100
            job_related_accuracy = (job_related_correct / job_related_total) * 100 if job_related_total > 0 else 0
            
            summary_lines = [
                "\n--- Classification Complete ---",
                f"Total items processed: {processed_all_items}",
                f"Job-related items classified: {processed_items}",
                f"Correct category predictions: {correct_predictions}",
                f"Category classification accuracy: {accuracy:.2f}%",
                "",
                "--- Job-Related Classification Results ---",
                f"Total job-related classifications: {job_related_total}",
                f"Correct job-related predictions: {job_related_correct}",
                f"Job-related classification accuracy: {job_related_accuracy:.2f}%"
            ]
            
            for line in summary_lines:
                print(line)
                f_out.write(line.lstrip() + '\n')
        else:
            no_data_msg = "No data was classified."
            print(no_data_msg)
            f_out.write(no_data_msg + '\n')


def main():
    """
    Main function to run the email classification pipeline.
    """

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Email classification pipeline')
    parser.add_argument('--filename', type=str, 
                       default='training_data_cleaned.json',
                       help='Full path to the training data JSON file')
    
    args = parser.parse_args()

    # Initialize the classifier agent
    agent = EmailClassifierAgent()
    
    # Load training data
    data = load_training_data(filename=args.filename)
    if not data:
        return
    
    # Process and classify emails
    process_email_classification(agent, data)


if __name__ == "__main__":
    main()
