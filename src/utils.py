def clean_price(price_text: str) -> int | None:
    """
    Converts strings like '۱۵,۷۰۰,۰۰۰,۰۰۰ تومان' or 'ودیعه: ۳۰۰٬۰۰۰٬۰۰۰' 
    into a clean Integer. Returns None if invalid or 'Negotiable'.
    """
    if not price_text:
        return None
    
    # 1. Convert Persian digits to English (۰ -> 0)
    persian_numbers = "۰۱۲۳۴۵۶۷۸۹"
    english_numbers = "0123456789"
    
    mapping_table = str.maketrans(persian_numbers, english_numbers)
    text = price_text.translate(mapping_table)
    
    # 2. Remove non-digits (commas, letters, spaces) - Example: "15,700 Toman" -> "15700"
    clean_digit = "".join([char for char in text if char.isdigit()])
    
    if not clean_digit:
        return None
    # final output
    return int(clean_digit)