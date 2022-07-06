class Account:
    count_id = 0

    def __init__(self, first_name, last_name, title, phone, email, password):
        Account.count_id += 1
        self.__account_id = Account.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__title = title
        self.__phone = phone
        self.__email = email
        self.__password = password
        self.__image = 'profile.png'
        self.__status = 'Active'

    def get_account_id(self):
        return self.__account_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_title(self):
        return self.__title

    def get_phone(self):
        return self.__phone

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_image(self):
        return self.__image

    def get_status(self):
        return self.__status

    def set_account_id(self, account_id):
        self.__account_id = account_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_title(self, title):
        self.__title = title

    def set_phone(self, phone):
        self.__phone = phone

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_image(self, image):
        self.__image = image

    def set_status(self, status):
        if status == "Locked":
            self.__status = 'Locked'
        elif status:
            self.__status = 'Active'
        else:
            self.__status = 'Inactive'
