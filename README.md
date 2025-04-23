# About This Repo

This is some example code for the workhops "Designing with Events". It is not
intended for any productive use but can be used as a kind of template on which
to base your first steps in translating the results of an event storming into
code.

## Prerequisites

An installation of the [nix cli](https://nixos.org). Follow the steps there for
installation instructions.

## Run the program

We interface with the project via [Poetry](https://python-poetry.org). It comes
with the provided nix-flake.

To run the program, given you've installed nix (see above):

```
git clone https://github.com/active-group/groundbeaker-event-storming-workshop.git
cd groundbreaker-event-storming-workshop
nix develop # make sure you have nix installed
poetry run python src/groundbreaker/__init__.py
```
