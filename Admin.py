from Account import *


class Admin(Account):
    def __init__(self, first_name, last_name, email, password, position):
        super().__init__(first_name, last_name, None, None, email, password)
        self.__position = position

    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position
