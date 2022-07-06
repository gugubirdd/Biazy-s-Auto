class PublicEvent:
    count_id = 0

    def __init__(self, startDate, endDate, startTime, endTime, venue, cost, capacity, title, image):
        PublicEvent.count_id += 1
        self.__publiceventid = PublicEvent.count_id
        self.__startDate = startDate
        self.__endDate = endDate
        self.__startTime = startTime
        self.__endTime = endTime
        self.__venue = venue
        self.__cost = cost
        self._capacity = capacity
        self.__title = title
        self.__image = image

    def get_image(self):
        return self.__image

    def set_image(self, image):
        self.__image = image

    def get_publiceventid(self):
        return self.__publiceventid

    def get_startDate(self):
        return self.__startDate

    def get_endDate(self):
        return self.__endDate

    def get_startTime(self):
        return self.__startTime

    def get_endTime(self):
        return self.__endTime

    def get_venue(self):
        return self.__venue

    def get_cost(self):
        return self.__cost

    def get_capacity(self):
        return self._capacity

    def get_title(self):
        return self.__title

    def set_publiceventid(self, publiceventid):
        self.__publiceventid = publiceventid

    def set_startDate(self, startDate):
        self.__startDate = startDate

    def set_endDate(self, endDate):
        self.__endDate = endDate

    def set_startTime(self, startTime):
        self.__startTime = startTime

    def set_endTime(self, endTime):
        self.__endTime = endTime

    def set_venue(self, venue):
        self.__venue = venue

    def set_cost(self, cost):
        self.__cost = cost

    def set_capacity(self, capacity):
        self._capacity = capacity

    def set_title(self, title):
        self.__title = title
