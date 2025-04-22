from dataclasses import dataclass

# Events
@dataclass
class ProductRegistered:
    id: int
    name: str

@dataclass 
class ShoppingCartCreated:
    id: int

@dataclass
class ProductAddedToCart:
    cart_id: int
    product_id: int

@dataclass
class ProductRemovedFromCart:
    cart_id: int
    product_id: int

Event = ProductRegistered | ShoppingCartCreated | ProductAddedToCart | ProductRemovedFromCart


