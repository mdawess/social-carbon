"""
Carbon Calculator for food emissions

The first of (hopefully) many carbon calculators for various
emissions.
"""

from typing import List, Dict, Optional
from src.cc.calculator import CarbonCalculator
import json
import requests

class FoodCalculator(CarbonCalculator):

    def __init__(self):
        """Instantiates a FoodCalculator object.

        Args:
            food_footprints: A dictionary of food footprints.
        """
        self.food_footprints = self._get_emissions()
        self.food_weights = self._get_weights()

    def calculate(self, items: Optional[List[str]], food: Optional[str]) -> float:
        """Calculates the total emissions for the given items.

        Args:
            items: The list of items to calculate the emissions for.
            estimated_wight: The estimated weight of each item in kg.

        Returns:
            The summed emissions for the given items.
        """
        # NOTE: This assumes only one of the two arguments is given.

        emissions = 0
        if items:
            for item in items:
                if item in self.food_weights and item in self.food_footprints:
                    emissions += self.food_footprints[item] \
                        ['GHG emissions per kilogram (Poore & Nemecek, 2018)'] * self.food_weights[item]
                elif item in self.food_weights and item not in self.food_footprints:
                    emissions += self._calculate_complex_emissions(item)
            return emissions
        elif food:
            return self._calculate_complex_emissions(food)
        else:
            return 0

    def _get_emissions(self) -> Dict[str, Dict[str, float]]:
        """Helper function that fetches the emissions dictionary.

        Args:
            the item to fetch the emissions for.

        Returns:
            The emissions for the given item.
        """
        emissions_file = open('data/food_footprints.json')
        emissions = json.load(emissions_file)
        return emissions

    def _get_weights(self) -> Dict[str, float]:
        """Gets the weights of the items.

        Returns:
            A dictionary of the weights of the items.
        """
        weights_file = open('data/food_weights.json')
        weights = json.load(weights_file)
        return weights

    def _calculate_complex_emissions(self, food: str) -> float:
        """Calculates the emissions for a complex item such
        as pasta or a sandwich.

        Returns:
            The emissions for the complex item.
        """
        try:
            ingredients = self._get_complex_ingredients(food)
            emissions = 0
            for ingredient in ingredients:
                if ingredient in self.food_footprints:
                    emissions += self.food_footprints[ingredient] \
                        ['GHG emissions per kilogram (Poore & Nemecek, 2018)'] \
                            * ingredients[ingredient]
            return emissions
        except:
            return 0

    def _get_complex_ingredients(self, food: str) -> Dict[str, float]:
        """Calculates the emissions for a complex item such
        as pasta or a sandwich.

        Returns:
            The emissions for the complex item.
        """
        # TODO: Do I need the API key?

        # Find the id of a comparable recipe
        id_url = 'https://api.spoonacular.com/recipes/complexSearch?query={0}&number=1'
        id_url = id_url.format(food)
        recipe_id = requests.get(id_url).json()['results'][0]['id']

        # Get the ingredients for the recipe
        ingredients_url = 'https://api.spoonacular.com/recipes/{0}/information'
        ingredients_url = ingredients_url.format(recipe_id)
        ingredients = requests.get(ingredients_url).json()['extendedIngredients']

        ingredients_dict = {}
        for ingredient in ingredients:
            name = ingredient['name']
            weight = ingredient['measures']['metric']['amount']
            metric = ingredient['measures']['metric']['unitShort']
            converted_weight = self._unit_conversion(metric, weight)
            ingredients_dict[name] = converted_weight
        
        return ingredients_dict

    def _unit_conversion(self, unit: str, weight: float) -> float:
        """Converts the weight to kg.

        Args:
            unit: The unit of the weight.
            weight: The weight of the item.

        Returns:
            The weight in kg.
        """
        if unit == 'kg':
            return weight
        elif unit == 'g':
            return weight / 1000
        elif unit == 'mg':
            return weight / 1000000
        elif unit == 'lb':
            return weight * 0.453592
        elif unit == 'oz':
            return weight * 0.0283495
        elif unit == 'tsp':
            return weight * 0.000004929
        elif unit == 'tbsp':
            return weight * 0.00001479
        elif unit == 'cup':
            return weight * 0.000236588
        elif unit == 'ml':
            return weight * 0.000001
        elif unit == 'l':
            return weight * 0.001
        elif unit == 'cloves' or unit == 'clove':
            return weight * 0.0055
        else:
            return 0




    