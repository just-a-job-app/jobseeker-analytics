import logging
from sqlmodel import Session, select
from db.companies import Companies

logger = logging.getLogger(__name__)


def company_exists(company_name: str, company_email_domain: str) -> bool:
    """
    Returns True if the company exists in the database, False otherwise.
    """
    from database import engine
    with Session(engine) as session:
        company = (
            session.exec(select(Companies).where(Companies.company_name == company_name and 
                                               Companies.company_email_domain == company_email_domain)).first()
        )

        if not company:
            return False
        else:
            return True
        
def add_company(company_name: str, company_email_domain: str) -> Companies:
    """
    Writes company data to the companies model
    """
    from database import engine
    with Session(engine) as session:
        # Check if the company already exists in the database
        existing_company = session.exec(select(Companies)
                                        .where(Companies.company_name == company_name and 
                                               Companies.company_email_domain == company_email_domain)).first()

        if not existing_company:
            # add a new company record
            new_company = Companies(
                company_name=company_name,
                company_email_domain=company_email_domain,
            )

            session.add(new_company)
            session.commit()
            session.refresh(new_company)
            logger.info(f"Created new company record for {company_name}")
            return new_company
        else:
            logger.info(f"{company_name} already exists in the database.")
            return existing_company
        
