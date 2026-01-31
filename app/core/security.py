"""
Security - Token generation and validation
"""
import secrets
import string
from datetime import datetime

def generate_tracking_token(length: int = 12) -> str:
    """
    Generate a unique tracking token
    
    Format: LF-XXXXXX-XXXXXX
    Example: LF-A3B9C2-D4E5F6
    
    Args:
        length: Token length (default: 12)
    
    Returns:
        Tracking token string
    """
    chars = string.ascii_uppercase + string.digits
    token_part1 = ''.join(secrets.choice(chars) for _ in range(6))
    token_part2 = ''.join(secrets.choice(chars) for _ in range(6))
    
    return f"LF-{token_part1}-{token_part2}"


def validate_tracking_token(token: str) -> bool:
    """
    Validate tracking token format
    
    Args:
        token: Token string to validate
    
    Returns:
        True if valid format, False otherwise
    """
    if not token or not isinstance(token, str):
        return False
    
    parts = token.split('-')
    
    if len(parts) != 3:
        return False
    
    if parts[0] != 'LF':
        return False
    
    if len(parts[1]) != 6 or len(parts[2]) != 6:
        return False
    
    # Check if alphanumeric
    if not parts[1].isalnum() or not parts[2].isalnum():
        return False
    
    return True