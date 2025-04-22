from dataclasses import dataclass
from commands import *
from entities import *
from events import *
from typing import List, Optional
from functools import reduce

class ExecError(Exception):
    pass

@dataclass
class AggregateRoot:
    # Fields that hold the current state of the domain.
    shopping_carts: dict[int, ShoppingCart]
    products: dict[int, Product]
    
    # Execute a `command` against the current state of the aggregate root
    # (`self`). Returns a list of events that result from executing that
    # command. When the `command` is invalid, raises an `ExecError`.
    def exec_command(self, command: Command) -> List[Event]:
        if isinstance(command, RegisterProduct):
            return self.__exec_register_product(command.id, command.name)
        if isinstance(command, AddProductToCart):
            return self.__exec_add_product_to_cart(command.product_id, command.cart_id)
        elif isinstance(command, RemoveProductFromCart):
            return self.__exec_remove_product_from_cart(command.product_id, command.cart_id)

    # Apply an `event` against the current state of the aggregate root
    # (`self`). The result is a new copy of the aggregate root, representing the
    # new state after the event has happened.
    #
    # We always assume that events that happened in the past result in a valid
    # new state, Therefore, we don't do any error checking when applying events.
    def apply_event(self, event: Event) -> 'AggregateRoot':
        if isinstance(event, ProductRegistered):
            return self.__apply_register_product(event.id, event.name)
        elif isinstance(event, ShoppingCartCreated):
            return self.__apply_add_shopping_cart(event.id)
        elif isinstance(event, ProductAddedToCart):
            return self.__apply_add_product_to_shopping_cart(event.cart_id, event.product_id)
        elif isinstance(event, ProductRemovedFromCart):
            return self.__apply_remove_product_from_shopping_cart(event.cart_id, event.product_id)

    @staticmethod
    def apply_events(events: List[Event]) -> 'AggregateRoot':
        return reduce(lambda aggregate_root, event: aggregate_root.apply_event(event),
                      events,
                      AggregateRoot(dict(), dict()))
    
    # Helpers
    def __apply_add_shopping_cart(self, cart_id: int) -> 'AggregateRoot':
        if self.shopping_carts.get(cart_id) is None:
            new_shopping_carts = self.shopping_carts.copy()
            new_shopping_carts[cart_id] = ShoppingCart(cart_id, dict())
            return AggregateRoot(shopping_carts=new_shopping_carts, products=self.products.copy())
        else:
            return self

    def __apply_register_product(self, product_id: int, product_name: str) -> 'AggregateRoot':
        new_products = self.products.copy()
        new_products[product_id] = Product(id=product_id, name=product_name)
        return AggregateRoot(shopping_carts=self.shopping_carts.copy(), products=new_products)
    
    def __apply_add_product_to_shopping_cart(self, cart_id: int, product_id: int) -> 'AggregateRoot':
        if self.shopping_carts.get(cart_id) is not None:
            new_shopping_carts = self.shopping_carts.copy()
            new_shopping_cart = new_shopping_carts[cart_id].add_product(product_id)
            new_shopping_carts[cart_id] = new_shopping_cart
            return AggregateRoot(shopping_carts=new_shopping_carts, products=self.products.copy())
        else:
            return self

    # Add a product to a cart. Noop if shopping cart doesn't exist.
    def __apply_remove_product_from_shopping_cart(self, cart_id: int, product_id: int) -> 'AggregateRoot':
        if self.shopping_carts.get(cart_id) is not None:
            new_shopping_carts = self.shopping_carts.copy()
            new_shopping_cart = new_shopping_carts[cart_id].remove_product(product_id)
            new_shopping_carts[cart_id] = new_shopping_cart
            return AggregateRoot(shopping_carts=new_shopping_carts, products=self.products.copy())
        else:
            return self
        
    # Execute commands
    # Helpers
    def __exec_register_product(self, product_id: int, product_name: str) -> List[Event]:
        if self.products.get(product_id) is None:
            return [ProductRegistered(id=product_id, name=product_name)]
        else:
            raise ExecError("product already registered")
                    
    def __exec_add_product_to_cart(self, product_id: int, cart_id: int) -> List[Event]:
        if self.products.get(product_id) is not None:
            if self.shopping_carts.get(cart_id) is not None:
                event = ProductAddedToCart(cart_id=cart_id, product_id=product_id)
                return [event]
            else:
                events = [ShoppingCartCreated(id=cart_id),
                          ProductAddedToCart(cart_id=cart_id, product_id=product_id)]
                return events
        else:
            raise ExecError("no such product")

    def __exec_remove_product_from_cart(self, product_id: int, cart_id: int) -> List[Event]:
        if self.products.get(product_id) is not None:
            if self.shopping_carts.get(cart_id) is not None:
                event = ProductRemovedFromCart(cart_id=cart_id, product_id=product_id)
                return [event]
            else:
                raise ExecError("no such shopping cart")
        else:
            raise ExecError("no such product")
