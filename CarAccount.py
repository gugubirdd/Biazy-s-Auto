from Account import *


class CarAccount(Account):
    def __init__(self, first_name, last_name, title, phone, email, password, make, model):
        super().__init__(first_name, last_name, title, phone, email, password, )
        self.__make = make
        self.__model = model

    def get_make(self):
        return self.__make

    def get_model(self):
        return self.__model

    def set_make(self, make):
        self.__make = make

    def set_model(self, model):
        self.__model = model
