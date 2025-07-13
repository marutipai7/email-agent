import re
from typing import List
from extractor.pydantic_models import Contact

def extract_emails(text:str, source:str="user_input") -> List[Contact]:
    # Simple regex for emails
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    found_emails = re.findall(email_pattern, text)
    
    contacts = []
    for email in set(found_emails):             # Use 'set' to avoid duplicates
        try:
            contact = Contact(email=email, source=source)
            contacts.append(contact)
        except Exception as e:
            print(f"Error creating contact for email {email}: {e}")
    return contacts


def classify_email_type(email:str) -> str:
    # Placeholder for email classification logic
    if any(email.endswith(domain) for domain in ["@spam.com", "@junkmail.com", '.ru', '.cn','.xyz']):
        return "spam"
    elif any(email.endswith(domain) for domain in ["@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com"]):
        return "personal"
    else:
        return "business"