from dataclasses import dataclass

# Entities
@dataclass
class Product:
    id: int
    name: str
    
@dataclass
class ShoppingCart:
    id: int
    products: dict[int, int]

    def contains_product(self, product_id) -> bool:
        return product_id in self.products

    # Add a new product to the shopping cart.
    def add_product(self, product_id) -> 'ShoppingCart':
        new_products = self.products.copy()
        new_products[product_id] = new_products.get(product_id, 0) + 1
        return ShoppingCart(id=self.id, products=new_products)

    # Remove one instance of a product from the shopping cart.
    def remove_product(self, product_id) -> 'ShoppingCart':
        if product_id not in self.products:
            return self
        else:
            new_products = self.products.copy()
            current_quantity = new_products[product_id]
            if current_quantity <= 1:
                del new_products[product_id]
            else:
                new_products[product_id] = current_quantity - 1
            return ShoppingCart(id=self.id, products=new_products)


