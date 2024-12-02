import re
from thefuzz import fuzz
from typing import Dict, List, Set

def load_company_mappings() -> Dict[str, str]:
    """Define common company name variations and their normalized forms."""
    return {
        "WM SUPERCENTER": "WALMART",
        "WALMART.COM": "WALMART",
        "WAL-MART": "WALMART",
        "WALMART WALMART": "WALMART",
        "WALMART 800": "WALMART",
        "SAMSCLUB": "SAMS CLUB",
        "HEB ONLINE": "HEB",
        "DD DOORDASH": "DOORDASH",
        "DOORDASH*": "DOORDASH",
        "IC* INSTACART": "INSTACART",
        "ATT*": "AT&T",
        "AMEX": "AMERICAN EXPRESS",
        "PP*": "PAYPAL",
        "SQ *": "SQUARE",
        "GRUBHUB*": "GRUBHUB",
        "UBER   *": "UBER",
        "APPLE.COM": "APPLE",
        "GOOGLE *": "GOOGLE",
    }

def should_exact_match(description: str) -> bool:
    """Check if this description should only be matched exactly."""
    keywords = ['ZELLE', 'INTERNET TRANSFER', 'TRANSFER TO']
    return any(keyword in description.upper() for keyword in keywords)

def initial_clean(name: str) -> str:
    """Initial cleaning of company names."""
    if not name:
        return ""
    
    # If it's a transfer-type transaction, return it as-is
    if should_exact_match(name):
        return name.upper().strip()
    
    result = name.upper().strip()
    
    # Remove common patterns
    patterns_to_remove = [
        r'\s+\d{6,}',
        r'#\d+',
        r'F\d{4,}',
        r'\*[A-Z0-9]+',
        r'\s+PMT\s*$',
        r'\s+RETRY\s+PYMT\s*$',
        r'ACH\s+PMT\s*$',
        r'AUTO\s+PYMT\s*$',
        r'\s+MOBILE\s+PMT\s*$',
        r'\s+ONLINE\s+PMT\s*$',
        r'\b\d{3}-\d{3}-\d{4}\b',
        r'\b\d{1,3}\s*[A-Z\s]+ST[A-Z\s]*\b',
        r'\s+\d{1,5}\s+[A-Z\s]+(?:STREET|ST|AVENUE|AVE|ROAD|RD|DRIVE|DR|LANE|LN|BLVD|PARKWAY|PKY|HWY)\b',
        r'(?<=\s)\d{5}(?:-\d{4})?(?=\s|$)',
        r'WWW\.[A-Z0-9.-]+\.[A-Z]{2,}',
        r'\.COM/?[A-Z]*\s*$',
        r',\s*[A-Z]{2},\s*US[A]?$',
        r',\s*[A-Z]{2}\s*$',
    ]
    
    for pattern in patterns_to_remove:
        result = re.sub(pattern, '', result)
    
    result = ' '.join(result.split())
    return result.strip('* ')

def find_best_match(name: str, known_companies: Set[str], threshold: int = 85) -> str:
    """Find the best matching company name using fuzzy matching."""
    best_ratio = 0
    best_match = name
    
    for known in known_companies:
        ratio = fuzz.ratio(name, known)
        if ratio > best_ratio and ratio >= threshold:
            best_ratio = ratio
            best_match = known
    
    return best_match

def build_company_groups(descriptions: List[str]) -> Dict[str, str]:
    """Build groups of similar company names."""
    cleaned_names = [initial_clean(desc) for desc in descriptions]
    unique_companies = set(cleaned_names)
    mapping = {}
    processed = set()
    
    base_mappings = {
        "WM SUPERCENTER": "WALMART",
        "WALMART.COM": "WALMART",
        "WAL-MART": "WALMART",
        "WALMART WALMART": "WALMART",
        "WALMART 800": "WALMART",
        "SAMSCLUB": "SAMS CLUB",
        "HEB ONLINE": "HEB",
        "DD DOORDASH": "DOORDASH",
        "DOORDASH*": "DOORDASH",
        "IC* INSTACART": "INSTACART",
        "ATT*": "AT&T",
        "AMEX": "AMERICAN EXPRESS",
        "PP*": "PAYPAL",
        "SQ *": "SQUARE",
        "GRUBHUB*": "GRUBHUB",
        "UBER   *": "UBER",
        "APPLE.COM": "APPLE",
        "GOOGLE *": "GOOGLE",
    }
    
    for name in unique_companies:
        if name in processed:
            continue
            
        if not name:
            continue
            
        # Transfer transactions get exact matching
        if should_exact_match(name):
            mapping[name] = name
            processed.add(name)
            continue
        
        # Check predefined mappings
        found = False
        for key, value in base_mappings.items():
            if name.startswith(key):
                mapping[name] = value
                processed.add(name)
                found = True
                break
        
        if found:
            continue
            
        # Find similar names using fuzzy matching
        similar_group = []
        for other in unique_companies:
            if other not in processed and not should_exact_match(other) and fuzz.ratio(name, other) > 85:
                similar_group.append(other)
                processed.add(other)
        
        if similar_group:
            canonical = min(similar_group, key=len)
            for variant in similar_group:
                mapping[variant] = canonical
    
    return mapping

def normalize_company_with_fuzzy(name: str, company_groups: Dict[str, str]) -> str:
    """
    Normalize company name using fuzzy matching and predefined groups.
    
    Args:
        name: Raw company name
        company_groups: Mapping of company name variants to canonical forms
    
    Returns:
        Normalized company name
    """
    cleaned = initial_clean(name)
    
    # If we have an exact match in our groups, use it
    if cleaned in company_groups:
        return company_groups[cleaned]
    
    # If no exact match, try to find the best match
    return find_best_match(cleaned, set(company_groups.values()))

def create_normalizer(transactions: List[str]):
    """Create a normalizer function pre-loaded with transaction data."""
    company_groups = build_company_groups(transactions)
    
    def normalizer(name: str) -> str:
        return normalize_company_with_fuzzy(name, company_groups)
    
    return normalizer

# Example usage:
def test_normalizer(transactions: List[str]):
    """Test the normalizer with actual transaction data."""
    normalizer = create_normalizer(transactions)
    
    test_cases = [
        "WALMART.COM 8009256278 702 SW 8TH ST BENTONVILLE, AR, US",
        "WALMART 800 BENTONVILLE",
        "WALMART WALMART.COM",
        "WAL-MART #2637",
        "WM SUPERCENTER #1129",
    ]
    
    print("Testing normalizer with Walmart variations:")
    for test in test_cases:
        normalized = normalizer(test)
        print(f"\nOriginal:   {test}")
        print(f"Normalized: {normalized}")