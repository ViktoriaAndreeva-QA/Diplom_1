import pytest
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_FILLING, INGREDIENT_TYPE_SAUCE
from data.test_data import BUNS, SAUCES, FILLINGS


class TestBurger:
    """Тесты для класса Burger"""

    #===============================================
    # Тесты для метода set_buns
    #===============================================
    @pytest.mark.parametrize("bun_name, bun_price", BUNS)
    def test_set_buns_choosing_a_bun_success(self, burger, bun_name, bun_price):
        """Выбор булочки"""
        bun = Bun(bun_name, bun_price)
        burger.set_buns(bun)

        assert burger.bun == bun

    @pytest.mark.parametrize("first_bun_data, second_bun_data", [
        (BUNS[0], BUNS[1]),
        (BUNS[1], BUNS[2]),
        (BUNS[2], BUNS[0])
    ])
    def test_set_buns_change_bun_success(self, burger, first_bun_data, second_bun_data):
        """Проверяет, что можно заменить одну булочку на другую (разные комбинации)"""
        first_bun = Bun(*first_bun_data)
        second_bun = Bun(*second_bun_data)
    
        burger.set_buns(first_bun)
        burger.set_buns(second_bun)
    
        assert burger.bun == second_bun

    #===============================================
    # Тесты для метода add_ingredient
    #===============================================
    @pytest.mark.parametrize("ingredient_data", [
        (SAUCES[1]),
        (FILLINGS[2]),
    ])
    def test_add_ingredient_adds_one_ingredient_success(self,burger, ingredient_data):
        """Проверяет успешное добавление одного ингредиента (соус или начинка)"""
        ingredient = Ingredient(*ingredient_data)
    
        burger.add_ingredient(ingredient)

        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == ingredient

    def test_add_ingredient_adds_sauce_and_filling_success(self, burger):
        """Проверяет успешное добавление соуса и начинки в бургер"""
        sauce = Ingredient(*SAUCES[0])
        filling = Ingredient(*FILLINGS[0])

        burger.add_ingredient(sauce)
        burger.add_ingredient(filling)

        types = [ing.get_type() for ing in burger.ingredients]
        
        assert len(burger.ingredients) == 2
        assert INGREDIENT_TYPE_SAUCE in types
        assert INGREDIENT_TYPE_FILLING in types

    def test_add_ingredient_adds_multiple_same_ingredients_success(self, burger):
        """Проверяет успешное добавление нескольких одинаковых ингредиентов (например, двойной соус)"""
        burger.add_ingredient(Ingredient(*SAUCES[2]))
        burger.add_ingredient(Ingredient(*SAUCES[2]))

        assert len(burger.ingredients) == 2
        assert burger.ingredients[0].get_name() == burger.ingredients[1].get_name()

    def test_add_ingredient_adds_multiple_fillings_success(self, burger):
        """Проверяет успешное добавление нескольких разных начинок"""
        filling1 = Ingredient(*FILLINGS[0])
        filling2 = Ingredient(*FILLINGS[1])
    
        burger.add_ingredient(filling1)
        burger.add_ingredient(filling2)
    
        assert len(burger.ingredients) == 2
        assert burger.ingredients[0] == filling1
        assert burger.ingredients[1] == filling2

    #===============================================
    # Тесты для метода remove_ingredient
    #===============================================
    @pytest.mark.parametrize("index_to_remove", [0, 1, 2, 3])
    def test_remove_ingredient_removes_element_success(self, burger_with_four_ingredients, index_to_remove):
        """Проверяет удаление ингредиента по индексу"""
        removed_name = burger_with_four_ingredients.ingredients[index_to_remove].get_name()
        initial_count = len(burger_with_four_ingredients.ingredients)
    
        burger_with_four_ingredients.remove_ingredient(index_to_remove)
    
        remaining_names = [ing.get_name() for ing in burger_with_four_ingredients.ingredients]
    
        assert len(burger_with_four_ingredients.ingredients) == initial_count - 1
        assert removed_name not in remaining_names
        
    def test_remove_ingredient_remove_single_ingredient_success(self, burger):
        """Проверяет удаление единственного ингредиента"""
        sauce = Ingredient(*SAUCES[1])
        burger.add_ingredient(sauce)
        
        burger.remove_ingredient(0)
        
        assert len(burger.ingredients) == 0

    def test_remove_ingredient_remove_all_elements_success(self, burger_with_four_ingredients):
        """Проверяет удаление всех ингредиентов по одному"""
        initial_count = len(burger_with_four_ingredients.ingredients)
    
        for _ in range(initial_count):
            burger_with_four_ingredients.remove_ingredient(0)
    
        assert len(burger_with_four_ingredients.ingredients) == 0

    def test_remove_ingredient_from_empty_burger_raises_error(self, burger):
        """Проверяет, что нельзя удалить ингредиент из пустого бургера"""
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)

        assert len(burger.ingredients) == 0

    def test_remove_ingredient_index_too_small_raises_error(self, burger_with_four_ingredients):
        """Проверяет, что попытка удаления ингредиента, индекс которого меньше минимального допустимого, вызывает ошибку"""
        min_valid_index = -len(burger_with_four_ingredients.ingredients)
        initial_count = len(burger_with_four_ingredients.ingredients)
    
        with pytest.raises(IndexError):
            burger_with_four_ingredients.remove_ingredient(min_valid_index - 1)
    
        assert len(burger_with_four_ingredients.ingredients) == initial_count

    @pytest.mark.parametrize("invalid_index", [4, 100])
    def test_remove_ingredient_nonexistent_index_too_large_raises_error(self, burger_with_four_ingredients, invalid_index):
        """Проверяет, что попытка удаления ингредиента, индекс которого больше максимального допустимого, вызывает ошибку"""
        initial_count = len(burger_with_four_ingredients.ingredients)
    
        with pytest.raises(IndexError):
            burger_with_four_ingredients.remove_ingredient(invalid_index + 1)
    
        assert len(burger_with_four_ingredients.ingredients) == initial_count

    #===============================================
    # Тесты для метода move_ingredient
    #===============================================
    @pytest.mark.parametrize("index, new_index, expected_order", [
        (0, 2, ["sour cream", "cutlet", "hot sauce", "dinosaur"]),
        (3, 0, ["dinosaur", "hot sauce", "sour cream", "cutlet"]),
        (1, 3, ["hot sauce", "cutlet", "dinosaur", "sour cream"]),
        (2, 1, ["hot sauce", "cutlet", "sour cream", "dinosaur"])
    ])
    def test_move_ingredient_moving_to_another_position_success(self, burger_with_four_ingredients, index, new_index, expected_order):
        """Проверяет перемещение ингредиента на другую позицию"""
        burger_with_four_ingredients.move_ingredient(index, new_index)
    
        result_order = [ing.get_name() for ing in burger_with_four_ingredients.ingredients]
        assert result_order == expected_order

    @pytest.mark.parametrize("first_move, second_move", [
        ((1, 2), (2, 1)),
        ((0, 3), (3, 0)),
        ((2, 0), (0, 2))
    ])
    def test_move_ingredient_returns_to_original_position_after_moving_success(self, burger_with_four_ingredients, first_move, second_move):
        """Проверяет, что перемещение ингредиента обратимо"""
        original_order = [ing.get_name() for ing in burger_with_four_ingredients.ingredients]
    
        index, new_index = first_move
        burger_with_four_ingredients.move_ingredient(index, new_index)
    
        index, new_index = second_move
        burger_with_four_ingredients.move_ingredient(index, new_index)
    
        final_order = [ing.get_name() for ing in burger_with_four_ingredients.ingredients]
        assert final_order == original_order

    def test_move_ingredient_index_less_than_minimum_raises_error(self, burger_with_four_ingredients):
        """Проверяет, что индекс меньше минимального (-len) вызывает ошибку"""
        min_valid_index = -len(burger_with_four_ingredients.ingredients)
        original_state = [ing.get_name() for ing in burger_with_four_ingredients.ingredients]
    
        with pytest.raises(IndexError):
            burger_with_four_ingredients.move_ingredient(min_valid_index - 1, 0)
    
        assert [ing.get_name() for ing in burger_with_four_ingredients.ingredients] == original_state

    def test_move_ingredient_index_more_than_maximum_raises_error(self, burger_with_four_ingredients):
        """Проверяет, что индекс больше максимального (len-1) вызывает ошибку"""
        max_valid_index = len(burger_with_four_ingredients.ingredients) - 1
        original_state = [ing.get_name() for ing in burger_with_four_ingredients.ingredients]
    
        with pytest.raises(IndexError):
            burger_with_four_ingredients.move_ingredient(max_valid_index + 1, 0)
    
        assert [ing.get_name() for ing in burger_with_four_ingredients.ingredients] == original_state
    
    def test_move_ingredient_from_empty_burger_raises_error(self, burger):
        """Проверяет, что нельзя перемещать ингредиенты в пустом бургере"""
        with pytest.raises(IndexError):
            burger.move_ingredient(0, 0)
    
        assert len(burger.ingredients) == 0

    #===============================================
    # Тесты для метода get_price
    #===============================================
    def test_get_price_with_bun_only_success(self, burger, mock_bun):
        """Проверяет цену бургера только с булочками (без ингредиентов)"""
        burger.set_buns(mock_bun())

        assert burger.get_price() == 200

    def test_get_price_with_bun_and_one_ingredient_success(self, burger, mock_bun, mock_ingredient):
        """Проверяет цену бургера с булочками и одним ингредиентом"""
        burger.set_buns(mock_bun(150))
        burger.add_ingredient(mock_ingredient(100))

        assert burger.get_price() == 400

    @pytest.mark.parametrize("bun_price, ingredient_prices, expected", [
        (200, [150, 150], 700),
        (200, [50, 100, 135, 85], 770),
        (150, [100, 150, 100, 250], 900)
    ])
    def test_get_price_with_bun_and_a_few_ingredients_success(self,burger, mock_bun, mock_ingredient, bun_price, ingredient_prices, expected):
        """Проверяет цену бургера с булочками и несколькими ингредиентами"""
        burger.set_buns(mock_bun(bun_price))

        for price in ingredient_prices:
            burger.add_ingredient(mock_ingredient(price))

        assert burger.get_price() == expected

    def test_get_price_without_bun_raises_error(self, burger):
        """Проверяет, что без булочки и ингредиентов возникает ошибка"""
        with pytest.raises(AttributeError):
            burger.get_price()

    def test_get_price_with_a_few_ingredients_and_without_buns_raises_error(self, burger, mock_ingredient):
        burger.add_ingredient(mock_ingredient())
        burger.add_ingredient(mock_ingredient(150, "chili sauce"))
        burger.add_ingredient(mock_ingredient(100, "hot sauce"))

        with pytest.raises(AttributeError):
            burger.get_price()

        assert len(burger.ingredients) == 3
        assert burger.bun is None

    #===============================================
    # Тесты для метода get_receipt
    #===============================================
    @pytest.mark.parametrize("bun_name, bun_price, expected_price", [
        ("black bun", 100, 200),
        ("white bun", 200, 400),
        ("red bun", 300, 600)
    ])
    def test_get_receipt_with_a_different_buns_only_success(self, burger, mock_bun, bun_name, bun_price, expected_price):
        """Проверяет чек для бургера с разными булочками"""
        burger.set_buns(mock_bun(bun_price, bun_name))

        expected = f"(==== {bun_name} ====)\n(==== {bun_name} ====)\n\nPrice: {expected_price}"

        assert burger.get_receipt() == expected
    
    def test_get_receipt_with_buns_and_one_ingredient_success(self, burger, mock_bun, mock_ingredient):
        """Проверяет чек для бургера с булочками и одним ингредиентом"""
        burger.set_buns(mock_bun(100, "black bun"))
        burger.add_ingredient(mock_ingredient(150, "dinosaur", INGREDIENT_TYPE_FILLING))

        expected = "(==== black bun ====)\n= filling dinosaur =\n(==== black bun ====)\n\nPrice: 350"

        assert burger.get_receipt() == expected

    def test_get_receipt_type_of_ingredients_is_in_lowercase_success(self, burger, mock_bun, mock_ingredient):
        """Проверяет, что тип ингредиентов выводится в чек в нижнем регистре"""
        burger.set_buns(mock_bun(100, "black bun"))
        burger.add_ingredient(mock_ingredient(150, "chili sauce", INGREDIENT_TYPE_SAUCE))
        burger.add_ingredient(mock_ingredient(100, "tomato", INGREDIENT_TYPE_FILLING))
    
        receipt = burger.get_receipt()

        assert "= sauce chili sauce =" in receipt
        assert "SAUCE" not in receipt
        assert "= filling tomato =" in receipt
        assert "FILLING" not in receipt

    def test_get_receipt_format_with_mocks(self, burger, mock_bun, mock_ingredient):
        """Проверяет полный формат чека"""
        burger.set_buns(mock_bun(100, "black bun"))
        burger.add_ingredient(mock_ingredient(50, "chili sauce", INGREDIENT_TYPE_SAUCE))
    
        receipt = burger.get_receipt()
        lines = receipt.split('\n')
    
        assert lines == [
            "(==== black bun ====)",
            "= sauce chili sauce =",
            "(==== black bun ====)",
            "",
            "Price: 250"
        ]

    @pytest.mark.parametrize("bun_name, bun_price, ingredients, expected_price", [
        ("white bun", 100, [("sauce", "hot sauce", 50)], 250),
        ("black bun", 150, [("filling", "cutlet", 75)], 375),
        ("white bun", 100, [("sauce", "hot sauce", 50), ("sauce", "hot sauce", 50)], 300),
        ("red bun", 200, [("sauce", "hot sauce", 50), ("filling", "cutlet", 75)], 525),
        ("sesame bun", 250, [("sauce", "hot sauce", 50), ("sauce", "sour cream", 60), 
                    ("filling", "cutlet", 75), ("filling", "dinosaur", 85)], 770)
    ])
    def test_get_receipt_various_combinations(self, burger, mock_bun, mock_ingredient, bun_name, bun_price, ingredients, expected_price):
        """Проверяет чек для разных комбинаций ингредиентов"""
        burger.set_buns(mock_bun(bun_price, bun_name))
    
        for ing_type, ing_name, ing_price in ingredients:
            mock_type = INGREDIENT_TYPE_SAUCE if ing_type == "sauce" else INGREDIENT_TYPE_FILLING
            burger.add_ingredient(mock_ingredient(ing_price, ing_name, mock_type))
    
        receipt = burger.get_receipt()
    
        assert receipt.startswith(f"(==== {bun_name} ====)")
        assert f"Price: {expected_price}" in receipt
    
        for ing_type, ing_name, _ in ingredients:
            assert f"= {ing_type} {ing_name} =" in receipt

    def test_get_receipt_without_bun_and_ingredients_raises_error(self, burger):
        """Проверяет, что без булочек и ингредиентов, при попытке получить чек возникает ошибка"""
        with pytest.raises(AttributeError):
            burger.get_receipt()

    def test_get_receipt_with_ingredients_but_without_buns_raises_error(self, burger, mock_ingredient):
        """Проверяет, что при попытке получить чек для бургера с ингредиентами, но без булочек, возникает ошибка"""
        burger.add_ingredient(mock_ingredient(50, "hot sauce", INGREDIENT_TYPE_SAUCE))
    
        with pytest.raises(AttributeError):
            burger.get_receipt()
