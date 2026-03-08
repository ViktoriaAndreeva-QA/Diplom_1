import pytest
from unittest.mock import Mock
from praktikum.burger import Burger
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_FILLING, INGREDIENT_TYPE_SAUCE


@pytest.fixture
def burger():
    """Фикстура: пустой бургер"""
    return Burger()

@pytest.fixture
def burger_with_four_ingredients():
    """Фикстура: бургер с 2 соусами и 2 начинками"""
    burger = Burger()
    burger.add_ingredient(Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100))
    burger.add_ingredient(Ingredient(INGREDIENT_TYPE_SAUCE, "sour cream", 200))
    burger.add_ingredient(Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 100))
    burger.add_ingredient(Ingredient(INGREDIENT_TYPE_FILLING, "dinosaur", 200))
    return burger

@pytest.fixture
def mock_bun():
    """Мок булочки для тестов get_price и get_receipt"""
    def _create(price=100, name="white bun"):
        mock = Mock()
        mock.get_price.return_value = price
        mock.get_name.return_value = name
        return mock
    return _create

@pytest.fixture
def mock_ingredient():
    """Мок ингредиентов для тестов get_price и get_receipt"""
    def _create(price=50, name="mock sauce", type=INGREDIENT_TYPE_SAUCE):
        mock = Mock()
        mock.get_price.return_value = price
        mock.get_name.return_value = name
        mock.get_type.return_value = type
        return mock
    return _create
