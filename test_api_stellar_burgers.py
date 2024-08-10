import pytest
import allure

from constants import Constants
from method_api_stellar_burgers import MethodApi
from data_modules import DataResponse, DataIngredients


@allure.description('Тесты на ручку POST/api/auth/register')
class TestCreateUser:

    @allure.title('Проверим создание пользователя')
    def test_create_user_input_positive_data_successful(self):
        email = Constants.TEST_USER_EMAIL
        password = Constants.TEST_USER_PASSWORD
        name = Constants.TEST_USER_NAME
        response = MethodApi.create_user(self, email, password, name)
        acc_token = response.json()["accessToken"]
        success = response.json()["success"]
        assert response.status_code == 200
        assert success is True
        MethodApi.delete_user(self, acc_token)

    @allure.title('Проверим создание пользователя который уже зарегестрирован')
    def test_re_create_identical_user_input_positive_data_show_error(self):
        email = Constants.TEST_USER_EMAIL
        password = Constants.TEST_USER_PASSWORD
        name = Constants.TEST_USER_NAME
        response = MethodApi.create_user(self, email, password, name)
        acc_token = response.json()["accessToken"]
        response = MethodApi.create_user(self, email, password, name)
        success = response.json()["success"]
        message = response.json()["message"]
        assert response.status_code == 403
        assert success is False
        assert message == DataResponse.data_response_login_already_in_use
        MethodApi.delete_user(self, acc_token)

    @allure.title('Проверим создание пользователя при не заполнении одного из обязательных полей')
    @pytest.mark.parametrize('email, password, name',
                             [
                                (Constants.TEST_USER_EMAIL, Constants.TEST_USER_PASSWORD, ""),
                                (Constants.TEST_USER_EMAIL, "", Constants.TEST_USER_NAME),
                                ("", Constants.TEST_USER_PASSWORD, Constants.TEST_USER_NAME)
                             ]
                             )
    def test_create_user_input_positive_data_without_one_field_show_error(self, email, password, name):
        response = MethodApi.create_user(self, email, password, name)
        success = response.json()["success"]
        message = response.json()["message"]
        assert response.status_code == 403
        assert success is False
        assert message == DataResponse.data_response_if_one_fields_missing


@allure.description('Тесты на ручку POST/api/auth/login')
class TestLoginUser:

    @allure.title('Проверка авторизации с существующим пользователем')
    def test_login_existing_user_input_positive_data_successful(self):
        email = Constants.TEST_USER_EMAIL
        password = Constants.TEST_USER_PASSWORD
        name = Constants.TEST_USER_NAME
        response = MethodApi.create_user(self, email, password, name)
        acc_token = response.json()["accessToken"]
        response = MethodApi.login_user(self, Constants.TEST_USER_EMAIL, Constants.TEST_USER_PASSWORD)
        success = response.json()["success"]
        user = response.json()["user"]
        assert response.status_code == 200
        assert success is True
        assert user == {"email": Constants.TEST_USER_EMAIL, "name": Constants.TEST_USER_NAME}
        MethodApi.delete_user(self, acc_token)

    @allure.title('Проверка авторизации с неверным логином и/или паролем')
    @pytest.mark.parametrize('email_test, password_test',
                             [
                                 (Constants.TEST_USER_EMAIL, "fakepassword"),
                                 ("fakeemail@fmail.ru", Constants.TEST_USER_PASSWORD),
                                 ("fakeemail@fmail.ru", "fakepassword")
                             ])
    def test_login_existing_user_input_negative_data_show_error(self, email_test, password_test):
        email = Constants.TEST_USER_EMAIL
        password = Constants.TEST_USER_PASSWORD
        name = Constants.TEST_USER_NAME
        response = MethodApi.create_user(self, email, password, name)
        acc_token = response.json()["accessToken"]
        response = MethodApi.login_user(self, email_test, password_test)
        success = response.json()["success"]
        message = response.json()["message"]
        assert response.status_code == 401
        assert success is False
        assert message == DataResponse.data_response_incorrect_email_or_password
        MethodApi.delete_user(self, acc_token)


@allure.description("Тесты на ручку PATCH/api/auth/user")
class TestUpdateUser:

    @allure.title("Проверка изменения данных пользователя с авторизацией")
    @pytest.mark.parametrize('email_test, password_test, name_test',
                             [
                                 (Constants.TEST_USER_EMAIL, Constants.TEST_USER_PASSWORD, "update_name"),
                                 (Constants.TEST_USER_EMAIL, "update_password", Constants.TEST_USER_NAME),
                                 ("update_email", Constants.TEST_USER_PASSWORD, Constants.TEST_USER_NAME)
                             ]
                             )
    def test_update_user_with_auth_successful(self, email_test, password_test, name_test):
        email = Constants.TEST_USER_EMAIL
        password = Constants.TEST_USER_PASSWORD
        name = Constants.TEST_USER_NAME
        response = MethodApi.create_user(self, email, password, name)
        acc_token = response.json()["accessToken"]
        response = MethodApi.update_user(self, email_test, password_test, name_test, acc_token)
        success = response.json()["success"]
        user = response.json()["user"]
        assert response.status_code == 200
        assert success is True
        assert user == {"email": email_test, "name": name_test}
        MethodApi.delete_user(self, acc_token)

    @allure.title('Проверка изменения данных пользователя без авторизации')
    @pytest.mark.parametrize('email_test, password_test, name_test',
                             [
                                 (Constants.TEST_USER_EMAIL, Constants.TEST_USER_PASSWORD, "update_name"),
                                 (Constants.TEST_USER_EMAIL, "update_password", Constants.TEST_USER_NAME),
                                 ("update_email", Constants.TEST_USER_PASSWORD, Constants.TEST_USER_NAME)
                             ]
                             )
    def test_update_user_without_auth_show_error(self, email_test, password_test, name_test):
        email = Constants.TEST_USER_EMAIL
        password = Constants.TEST_USER_PASSWORD
        name = Constants.TEST_USER_NAME
        response = MethodApi.create_user(self, email, password, name)
        acc_token = response.json()["accessToken"]
        response = MethodApi.update_user(self, email_test, password_test, name_test, "")
        success = response.json()["success"]
        message = response.json()["message"]
        assert response.status_code == 401
        assert success is False
        assert message == DataResponse.data_response_not_authorized
        MethodApi.delete_user(self, acc_token)


@allure.description('Тесты на ручку POST/api/orders')
class TestCreateOrder:

    @allure.title('Проверка создания заказа с авторизацией пользователя')
    def test_create_order_user_with_auth_successful(self):
        email = Constants.TEST_USER_EMAIL
        password = Constants.TEST_USER_PASSWORD
        name = Constants.TEST_USER_NAME
        response = MethodApi.create_user(self, email, password, name)
        acc_token = response.json()["accessToken"]
        response = MethodApi.create_order_with_auth(self, DataIngredients.ingredients, acc_token)
        success = response.json()["success"]
        order = response.json()["order"]["ingredients"][1]
        assert response.status_code == 200
        assert success is True
        assert "_id" in order
        MethodApi.delete_user(self, acc_token)

    @allure.title('Проверка создания заказа с авторизацией пользователя без ингредиентов')
    def test_create_order_user_with_auth_no_ingredients_show_error(self):
        email = Constants.TEST_USER_EMAIL
        password = Constants.TEST_USER_PASSWORD
        name = Constants.TEST_USER_NAME
        response = MethodApi.create_user(self, email, password, name)
        acc_token = response.json()["accessToken"]
        response = MethodApi.create_order_with_auth(self, {"ingredients": ""}, acc_token)
        success = response.json()["success"]
        message = response.json()["message"]
        assert response.status_code == 400
        assert success is False
        assert message == DataResponse.data_response_no_ingredients
        MethodApi.delete_user(self, acc_token)

    @allure.title('Проверка создания заказа с авторизацией пользователя с невалидным значением ингредиента')
    def test_create_order_user_with_auth_invalid_ingredient_show_error(self):
        email = Constants.TEST_USER_EMAIL
        password = Constants.TEST_USER_PASSWORD
        name = Constants.TEST_USER_NAME
        response = MethodApi.create_user(self, email, password, name)
        acc_token = response.json()["accessToken"]
        response = MethodApi.create_order_with_auth(self, {"ingredients": "fake"}, acc_token)
        assert response.status_code == 500
        MethodApi.delete_user(self, acc_token)

    @allure.title('Проверка создания заказа без авторизации пользователя')
    def test_create_order_user_without_auth_successful(self):
        response = MethodApi.create_order_without_auth(self, DataIngredients.ingredients)
        success = response.json()["success"]
        order = response.json()["order"]
        assert response.status_code == 200
        assert success is True
        assert "ingredients" not in order

    @allure.title('Проверка создания заказа без авторизации пользователя без ингредиентов')
    def test_create_order_user_without_auth_no_ingredients_show_error(self):
        response = MethodApi.create_order_without_auth(self, {"ingredients": ""})
        success = response.json()["success"]
        message = response.json()["message"]
        assert response.status_code == 400
        assert success is False
        assert message == DataResponse.data_response_no_ingredients

    @allure.title('Проверка создания заказа без авторизации пользователя с невалидным значением ингредиента')
    def test_create_order_user_without_auth_invalid_ingredient_show_error(self):
        response = MethodApi.create_order_without_auth(self, {"ingredients": "fake"})
        assert response.status_code == 500


@allure.description('Тесты на ручку GET/api/orders')
class TestGetOrderUser:

    @allure.title('Проверка получения заказов авторизованного пользователя')
    def test_get_orders_user_with_auth_successful(self):
        email = Constants.TEST_USER_EMAIL
        password = Constants.TEST_USER_PASSWORD
        name = Constants.TEST_USER_NAME
        response = MethodApi.create_user(self, email, password, name)
        acc_token = response.json()["accessToken"]
        MethodApi.create_order_with_auth(self, DataIngredients.ingredients, acc_token)
        MethodApi.create_order_with_auth(self, DataIngredients.ingredients2, acc_token)
        MethodApi.create_order_with_auth(self, DataIngredients.ingredients3, acc_token)
        response = MethodApi.get_order_user(self, acc_token)
        success = response.json()["success"]
        orders = response.json()["orders"][1]
        assert response.status_code == 200
        assert success is True
        assert "ingredients" in orders
        MethodApi.delete_user(self, acc_token)

    @allure.title('Проверка получения заказов не авторизованного пользователя')
    def test_get_orders_user_without_auth_show_error(self):
        email = Constants.TEST_USER_EMAIL
        password = Constants.TEST_USER_PASSWORD
        name = Constants.TEST_USER_NAME
        response = MethodApi.create_user(self, email, password, name)
        acc_token = response.json()["accessToken"]
        MethodApi.create_order_with_auth(self, DataIngredients.ingredients, acc_token)
        MethodApi.create_order_with_auth(self, DataIngredients.ingredients2, acc_token)
        MethodApi.create_order_with_auth(self, DataIngredients.ingredients3, acc_token)
        response = MethodApi.get_order_user(self, "")
        success = response.json()["success"]
        message = response.json()["message"]
        assert response.status_code == 401
        assert success is False
        assert message == DataResponse.data_response_not_authorized
        MethodApi.delete_user(self, acc_token)
