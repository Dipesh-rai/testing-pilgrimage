# utils.py
from decimal import Decimal

def calculate_group_discount(base_price, participants, discounts):
    best_discount = None
    for discount in discounts:
        if participants >= discount.min_participants:
            if not best_discount or discount.min_participants > best_discount.min_participants:
                best_discount = discount
    
    if best_discount:
        if best_discount.discount_type == 'percent':
            return base_price * (1 - best_discount.discount_per_pax/100)
        return base_price - best_discount.discount_per_pax
    return base_price