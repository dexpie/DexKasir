
import hashlib

def format_rupiah(amount):
    """Format number to Rupiah currency string."""
    try:
        return f"Rp {amount:,.0f}".replace(",", ".")
    except:
        return f"Rp {amount}"

def hash_password(password):
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()
