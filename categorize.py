from categories import TRANSACTION_CATEGORIES

def categorize_transaction(description: str) -> str:
    """Categorize a transaction based on its description."""
    description = description.upper()
    
    for category, keywords in TRANSACTION_CATEGORIES.items():
        if any(keyword in description for keyword in keywords):
            return category
            
    return 'Other'