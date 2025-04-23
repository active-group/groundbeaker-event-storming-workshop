from dataclasses import dataclass
from functools import reduce

class ExecError(Exception):
    pass

@dataclass
class AggregateRoot:
    # Fields that hold the current state of the domain.

    
    # Execute a `command` against the current state of the aggregate root
    # (`self`). Returns a list of events that result from executing that
    # command. When the `command` is invalid, raises an `ExecError`.
    def exec_command(self, command: List[Command]) -> List[Event]:
        pass

    # Apply an `event` against the current state of the aggregate root
    # (`self`). The result is a new copy of the aggregate root, representing the
    # new state after the event has happened.
    #
    # We always assume that events that happened in the past result in a valid
    # new state, Therefore, we don't do any error checking when applying events.
    def apply_event(self, event: Event) -> 'AggregateRoot':
        return self

    @staticmethod
    def apply_events(events: List[Event]) -> 'AggregateRoot':
        return reduce(lambda aggregate_root, event: aggregate_root.apply_event(event),
                      events,
                      # TODO Initialize fields
                      AggregateRoot())

