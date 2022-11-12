"""
This is an abstract class, not meant to be instantiated directly.

This class is the base class for all calculators. It provides the basic
functionality for all calculators ie. passing in certain parameters and
calculating the total emissions.

The calculator is exclusively a calculator, it will not store any data.
"""

from typing import Any, List

class CarbonCalculator:

    def __init__(self):
        """Instantiates a CarbonCalculator object."""
        raise NotImplementedError

    def calculate(self, items: List[str]) -> float:
        """Calculates the total emissions for the given items.

        Args:
            items: The list of items to calculate the emissions for.

        Returns:
            The summed emissions for the given items.
        """
        raise NotImplementedError

    def _get_emissions(self) -> float:
        """Helper function that fetches the emissions dictionary.

        Args:
            the item to fetch the emissions for.

        Returns:
            The emissions for the given item.
        """
        raise NotImplementedError