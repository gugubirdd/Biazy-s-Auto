import Accessory


class ElectronicAccessory(Accessory.Accessory):
    count_id = 0

    def __init__(self, image, name, description, price, quantity, battery_type, batteries_required, date, start, end, status):
        super().__init__(image, name, description, price, quantity, date, start, end, status)
        ElectronicAccessory.count_id += 1
        self.__electronicaccessory_id = ElectronicAccessory.count_id
        self.__image = image
        self.__name = name
        self.__description = description
        self.__price = price
        self.__quantity = quantity
        self.__date = date
        self.__start = start
        self.__end = end
        self.__status = status
        self.__battery_type = battery_type
        self.__batteries_required = batteries_required

    def get_electronicaccessory_id(self):
        return self.__electronicaccessory_id

    def set_electronicaccessory_id(self, electronicaccessory_id):
        self.__electronicaccessory_id = electronicaccessory_id

    def get_battery_type(self):
        return self.__battery_type

    def set_battery_type(self, battery_type):
        self.__battery_type = battery_type

    def get_batteries_required(self):
        return self.__batteries_required

    def set_batteries_required(self, batteries_required):
        self.__batteries_required = batteries_required
