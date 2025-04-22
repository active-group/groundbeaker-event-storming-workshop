from dataclasses import dataclass

# Commands
@dataclass
class RegisterProduct:
    id: int
    name: str

@dataclass
class AddProductToCart:
    product_id: int
    cart_id: int

@dataclass
class RemoveProductFromCart:
    product_id: int
    cart_id: int
    
Command = RegisterProduct | AddProductToCart | RemoveProductFromCart

