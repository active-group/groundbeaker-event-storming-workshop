from commands import *
from entities import *
from events import *
from aggregate_root import AggregateRoot
import pprint

def main():
    root = AggregateRoot(dict(), dict())
    commands = [
        RegisterProduct(id=0, name="iPad"),
        RegisterProduct(id=1, name="Drinking Bottle"),
        AddProductToCart(cart_id=0, product_id=0),
        AddProductToCart(cart_id=0, product_id=0),
        AddProductToCart(cart_id=0, product_id=1),
        AddProductToCart(cart_id=1, product_id=1),
        RemoveProductFromCart(cart_id=0, product_id=0)
        ]

    events = []
    loop = 0
    for command in commands:
        new_events = root.exec_command(command)
        events += new_events
        print("==========")
        print("Command", loop, ":", command)
        root = AggregateRoot.apply_events(events)
        pprint.pp(root)
        loop += 1

    print("List of generated events")
    pprint.pp(events)

if __name__ == '__main__': main()

