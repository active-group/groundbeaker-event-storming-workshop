from dataclass import dataclass

# Commands
@dataclass
class AddProductToCart:
    productId: int
    cartId: int

@dataclass
class RemoveProductFromCart:
    productId: int
    cartId: int
    
Command = AddProductToCart | RemoveProductFromCart

@dataclass 
class ShoppingCartCreated:
    id: int

@dataclass
class ProductAddedToCart:
    cartId: int
    productId: int

Event = ShoppingCartCreated | ProductAddedToCart

# Entities
@dataclass(frozen=True)
class ShoppingCart:
    id: int
    products: dict[int, int]

    def contains_product(self, product_id) -> bool:
        return product_id in self.products

    def add_product(self, product_id) -> 'ShoppingCart':
        if product_id in self.products:
            product_amount = self.products[product_id]
            products = self.products.copy()
            products[product_id] = product_amount + 1
            return ShoppingCart(id=self.id, products=products)
        else:
            return self
        
            

