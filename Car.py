class Car:
    count_id = 0

    def __init__(self, car_name, car_model, car_description, car_price, car_quantity, car_availstartdate,
                 car_availability, car_image):
        Car.count_id += 1
        self.__car_id = Car.count_id
        self.__car_name = car_name
        self.__car_model = car_model
        self.__car_description = car_description
        self.__car_price = car_price
        self.__car_quantity = car_quantity
        self.__car_availability = car_availability
        self.__car_image = car_image
        self.__car_availstartdate = car_availstartdate

    def get_car_id(self):
        return self.__car_id

    def set_car_id(self, car_id):
        self.__car_id = car_id

    def get_car_name(self):
        return self.__car_name

    def set_car_name(self, car_name):
        self.__car_name = car_name

    def get_car_model(self):
        return self.__car_model

    def set_car_model(self, car_model):
        self.__car_model = car_model

    def get_car_description(self):
        return self.__car_description

    def set_car_description(self, car_description):
        self.__car_description = car_description

    def get_car_price(self):
        return self.__car_price

    def set_car_price(self, car_price):
        self.__car_price = car_price

    def get_car_quantity(self):
        return self.__car_quantity

    def set_car_quantity(self, car_quantity):
        self.__car_quantity = car_quantity

    def get_car_availstartdate(self):
        return self.__car_availstartdate

    def set_car_availstartdate(self, car_availstartdate):
        self.__car_availstartdate = car_availstartdate

    def get_car_availability(self):
        return self.__car_availability

    def set_car_availability(self, car_availability):
        self.__car_availability = car_availability

    def get_car_image(self):
        return self.__car_image

    def set_car_image(self, car_image):
        self.__car_image = car_image
