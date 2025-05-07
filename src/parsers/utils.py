def calculate_discount(old_price: float, new_price: float) -> int:
    if old_price <= 0 or new_price >= old_price:
        return 0
    return int(round((1 - new_price / old_price) * 100))