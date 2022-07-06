class Accessory:
    count_id = 0

    def __init__(self, image, name, description, price, quantity, date, start, end, status):
        Accessory.count_id += 1
        self.__accessory_id = Accessory.count_id
        self.__image = image
        self.__name = name
        self.__description = description
        self.__price = price
        self.__quantity = quantity
        self.__date = date
        self.__start = start
        self.__end = end
        self.__status = status

    def get_accessory_id(self):
        return self.__accessory_id

    def set_accessory_id(self, accessory_id):
        self.__accessory_id = accessory_id

    def get_image(self):
        return self.__image

    def set_image(self, image):
        self.__image = image

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_start(self):
        return self.__date

    def set_start(self, date):
        self.__date = date

    def get_date(self):
        return self.__start

    def set_date(self, start):
        self.__start = start

    def get_end(self):
        return self.__end

    def set_end(self, end):
        self.__end = end

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status
