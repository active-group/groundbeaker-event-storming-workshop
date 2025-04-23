from commands import *
from entities import *
from events import *
from aggregate_root import AggregateRoot
import pprint

def main():
    root = AggregateRoot()
    commands = [
        # TODO Insert a sequence of example commands.
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

