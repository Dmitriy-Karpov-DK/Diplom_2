import allure
import requests
from constants import Constants


class MethodApi:

    @allure.step('Создаем пользователя')
    def create_user(self, email, password, name):
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(Constants.URL_CREATE_USER, json=payload)
        return response

    @allure.step('Удаляем пользователя')
    def delete_user(self, acc_token):
        headers = {"Authorization": acc_token}
        response = requests.delete(Constants.URL_UPDATE_USER, headers=headers)
        return response

    @allure.step('Авторизуемся')
    def login_user(self, email, password):
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(Constants.URL_LOGIN_USER, json=payload)
        return response

    @allure.step('Изменяем данные пользователя')
    def update_user(self, email, password, name, acc_token):
        headers = {"Authorization": acc_token}
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.patch(Constants.URL_UPDATE_USER, json=payload, headers=headers)
        return response

    @allure.step('Создаем заказ с авторизацией')
    def create_order_with_auth(self, ingredients, acc_token):
        headers = {"Authorization": acc_token}
        response = requests.post(Constants.URL_CREATE_AND_GET_ORDER, json=ingredients, headers=headers)
        return response

    @allure.step('Создаем заказ без авторизации')
    def create_order_without_auth(self, ingredients):
        response = requests.post(Constants.URL_CREATE_AND_GET_ORDER, json=ingredients)
        return response

    @allure.step('Получаем заказы пользователя')
    def get_order_user(self, acc_token):
        headers = {"Authorization": acc_token}
        response = requests.get(Constants.URL_CREATE_AND_GET_ORDER, headers=headers)
        return response
