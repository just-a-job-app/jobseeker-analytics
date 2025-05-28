import logging
import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib

# Set up logger
logger = logging.getLogger(__name__)

def preprocess_email(email_data: dict) -> str:
    """
    Preprocesses email content for classification.
    Handles encoding issues, anonymization, and cleaning.
    """
    logger.info("Starting email preprocessing")
    try:
        # Combine subject and body
        text_content = email_data.get("subject", "")
        logger.debug(f"Initial text content length: {len(text_content)}")
        
        # Add body content if available
        if email_data.get("text_content"):
            text_content += "\n" + email_data["text_content"]
            logger.debug("Added text content from email body")
        
        # Add HTML content if available (converted to text)
        if email_data.get("html_content"):
            soup = BeautifulSoup(email_data["html_content"], "html.parser")
            html_text = soup.get_text(separator=" ", strip=True)
            text_content += "\n" + html_text
            logger.debug("Added text content from HTML")
        
        # Clean and normalize text
        text_content = clean_text(text_content)
        logger.debug(f"Text content after cleaning: {len(text_content)} characters")
        
        # Anonymize sensitive information
        text_content = anonymize_content(text_content)
        logger.debug("Completed anonymization of sensitive information")
        
        logger.info("Successfully preprocessed email")
        return text_content
    except Exception as e:
        logger.exception(f"Error preprocessing email: {e}")
        return ""

def clean_text(text: str) -> str:
    """
    Cleans and normalizes text content.
    """
    logger.debug("Starting text cleaning")
    try:
        # Remove special characters and normalize whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        logger.debug("Removed special characters and normalized whitespace")
        
        # Convert to lowercase
        text = text.lower()
        logger.debug("Converted text to lowercase")
        
        # Remove email signatures
        text = remove_signatures(text)
        logger.debug("Removed email signatures")
        
        # Remove common email boilerplate
        text = remove_boilerplate(text)
        logger.debug("Removed email boilerplate")
        
        return text.strip()
    except Exception as e:
        logger.exception(f"Error cleaning text: {e}")
        return text

def anonymize_content(text: str) -> str:
    """
    Anonymizes sensitive information in the email.
    """
    logger.debug("Starting content anonymization")
    try:
        # Remove email addresses
        text = re.sub(r'[\w\.-]+@[\w\.-]+', '[EMAIL]', text)
        logger.debug("Anonymized email addresses")
        
        # Remove phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
        logger.debug("Anonymized phone numbers")
        
        # Remove dates (keep the structure but anonymize)
        text = re.sub(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', '[DATE]', text)
        logger.debug("Anonymized dates")
        
        # Remove times
        text = re.sub(r'\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?', '[TIME]', text)
        logger.debug("Anonymized times")
        
        return text
    except Exception as e:
        logger.exception(f"Error anonymizing content: {e}")
        return text


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib

class ApplicationStatusClassifier:
    def __init__(self):
        logger.info("Initializing ApplicationStatusClassifier")
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=5000,
                ngram_range=(1, 2),
                stop_words='english'
            )),
            ('classifier', RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            ))
        ])
        logger.debug("Pipeline initialized with TfidfVectorizer and RandomForestClassifier")
        
    def train(self, X, y):
        """
        Train the classifier on preprocessed email data.
        X: list of preprocessed email texts
        y: list of application statuses
        """
        logger.info(f"Starting model training with {len(X)} samples")
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            logger.debug(f"Split data into training ({len(X_train)} samples) and test ({len(X_test)} samples) sets")
            
            self.pipeline.fit(X_train, y_train)
            logger.info("Model training completed")
            
            # Evaluate on test set
            accuracy = self.pipeline.score(X_test, y_test)
            logger.info(f"Model accuracy on test set: {accuracy:.2f}")
            return accuracy
        except Exception as e:
            logger.exception(f"Error during model training: {e}")
            raise
    
    def predict(self, email_text: str) -> dict:
        """
        Predict application status from preprocessed email text.
        """
        logger.info("Starting prediction for new email")
        try:
            # Preprocess the email
            processed_text = preprocess_email(email_text)
            logger.debug(f"Preprocessed text length: {len(processed_text)}")
            
            # Get prediction probabilities
            probas = self.pipeline.predict_proba([processed_text])[0]
            logger.debug(f"Raw prediction probabilities: {probas}")
            
            # Get the predicted class
            predicted_class = self.pipeline.classes_[probas.argmax()]
            confidence = float(probas.max())
            logger.info(f"Predicted class: {predicted_class} with confidence: {confidence:.2f}")
            
            return {
                "status": predicted_class,
                "confidence": confidence,
                "all_probabilities": dict(zip(self.pipeline.classes_, probas))
            }
        except Exception as e:
            logger.exception(f"Error during prediction: {e}")
            return {
                "status": "unknown",
                "confidence": 0.0,
                "all_probabilities": {}
            }
    
    def save_model(self, path: str):
        """Save the trained model to disk"""
        logger.info(f"Saving model to {path}")
        try:
            joblib.dump(self.pipeline, path)
            logger.info("Model saved successfully")
        except Exception as e:
            logger.exception(f"Error saving model: {e}")
            raise
    
    @classmethod
    def load_model(cls, path: str):
        """Load a trained model from disk"""
        logger.info(f"Loading model from {path}")
        try:
            instance = cls()
            instance.pipeline = joblib.load(path)
            logger.info("Model loaded successfully")
            return instance
        except Exception as e:
            logger.exception(f"Error loading model: {e}")
            raise


def process_email(email_text: str) -> dict:
    """
    Process email content to extract application status and metadata.
    """
    logger.info("Starting email processing")
    try:
        # Load the trained classifier
        logger.debug("Loading trained classifier")
        classifier = ApplicationStatusClassifier.load_model('models/application_classifier.joblib')
        
        # Get classification results
        logger.debug("Getting classification results")
        classification = classifier.predict(email_text)
        
        # Extract other metadata using existing LLM approach
        logger.debug("Extracting metadata using LLM")
        metadata = extract_metadata(email_text)
        
        result = {
            "application_status": classification["status"],
            "confidence": classification["confidence"],
            "company_name": metadata.get("company_name", "unknown"),
            "job_title": metadata.get("job_title", "unknown")
        }
        logger.info(f"Email processing completed. Status: {result['application_status']}, Confidence: {result['confidence']:.2f}")
        return result
    except Exception as e:
        logger.exception(f"Error processing email: {e}")
        return {
            "application_status": "unknown",
            "confidence": 0.0,
            "company_name": "unknown",
            "job_title": "unknown"
        }


def train_classifier(training_data: List[dict]):
    """
    Train the classifier on labeled email data.
    """
    logger.info(f"Starting classifier training with {len(training_data)} samples")
    try:
        # Prepare training data
        logger.debug("Preparing training data")
        X = [preprocess_email(email) for email in training_data]
        y = [email["status"] for email in training_data]
        
        # Initialize and train classifier
        logger.debug("Initializing classifier")
        classifier = ApplicationStatusClassifier()
        accuracy = classifier.train(X, y)
        
        # Save the trained model
        logger.debug("Saving trained model")
        classifier.save_model('models/application_classifier.joblib')
        
        logger.info(f"Classifier training completed with accuracy: {accuracy:.2f}")
        return accuracy
    except Exception as e:
        logger.exception(f"Error during classifier training: {e}")
        raise