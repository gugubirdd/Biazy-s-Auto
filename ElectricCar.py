import Car


class ElectricCar(Car.Car):
    count_id = 0

    def __init__(self, car_name, car_model, car_description, car_price, car_quantity, car_availstartdate,
                 car_availability, car_battery_capacity, car_charging_duration, car_image):
        super().__init__(car_name, car_model, car_description, car_price, car_quantity, car_availstartdate,
                         car_availability, car_image)
        ElectricCar.count_id += 1
        self.__electric_car_id = ElectricCar.count_id
        self.__car_battery_capacity = car_battery_capacity
        self.__car_charging_duration = car_charging_duration

    def get_electric_car_id(self):
        return self.__electric_car_id

    def set_electric_car_id(self, electric_car_id):
        self.__electric_car_id = electric_car_id

    def get_car_battery_capacity(self):
        return self.__car_battery_capacity

    def set_car_battery_capacity(self, car_battery_capacity):
        self.__car_battery_capacity = car_battery_capacity

    def get_car_charging_duration(self):
        return self.__car_charging_duration

    def set_car_charging_duration(self, car_charging_duration):
        self.__car_charging_duration = car_charging_duration
