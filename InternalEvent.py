import PublicEvent


class InternalEvent(PublicEvent.PublicEvent):
    count_id = 0

    def __init__(self, startDate, endDate, startTime, endTime, venue, cost, capacity, title, image, fullname, attendance):
        super().__init__(startDate, endDate, startTime, endTime, venue, cost, capacity, title, image)
        InternalEvent.count_id += 1
        self.__internaleventid = InternalEvent.count_id
        self.__fullname = fullname
        self.__attendance = attendance
        self.__image = image
        self.__startDate = startDate
        self.__endDate = endDate
        self.__startTime = startTime
        self.__endTime = endTime
        self.__venue = venue
        self.__cost = cost
        self._capacity = capacity
        self.__title = title

    def get_internaleventid(self):
        return self.__internaleventid

    def get_fullname(self):
        return self.__fullname

    def get_attendance(self):
        return self.__attendance

    def set_internalEventId(self, internaleventid):
        self.__internaleventid = internaleventid

    def set_fullname(self, fullname):
        self.__fullname = fullname

    def set_attendance(self, attendance):
        self.__attendance = attendance
