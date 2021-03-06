import time
import datetime
import calendar


class DateTimeManager(object):

    # 时间戳
    @staticmethod
    def get_timestamp():
        return time.time()

    # 20200714105332 YMDhms
    @staticmethod
    def getCurrentDateTime():
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # 2020-07-14 10:53:32.882817
    @staticmethod
    def getDateTime():
        return datetime.datetime.now()

    # 20200714 YMD
    @staticmethod
    def getCurrentDate():
        return datetime.datetime.now().strftime("%Y-%m-%d")

    # 105858 hms
    @staticmethod
    def getCurrentTime():
        return datetime.datetime.now().strftime("%H%M%S")

    # 110017488766 hmsf
    @staticmethod
    def getTime():
        return datetime.datetime.now().strftime("%H%M%S%f")

    # format输出time
    @staticmethod
    def formated_time(format_time):
        '''
        :param format_time: '%Y-%m-%d %H:%M:%S'  'yyyy-MM-dd HH:mm:ss:SSS'
        '''
        return datetime.datetime.now().strftime(format_time)

    @staticmethod
    def addDaysByFormatter(adddays, dateFormat):
        afteraddtime = datetime.datetime.now() + datetime.timedelta(days=adddays)     
        return time.strftime(afteraddtime,dateFormat)

    @staticmethod
    def addMonthsByFormatter(months, dateFormat):
        d = datetime.datetime.now()
        c = calendar.Calendar()
        year = d.year
        month = d.month
        today = d.day
        if month+months > 12 :
            month = months
            year += 1
        else:
            month += months
        days = calendar.monthrange(year, month)[1]  
        
        if today > days:
            afteraddday = days
        else:
            afteraddday = today
        return datetime.datetime(year,month,afteraddday).strftime(dateFormat)

    @staticmethod
    def addYearsByFormatter(years, dateFormat):
        d = datetime.datetime.now()
        c = calendar.Calendar()
        year = d.year + years
        month = d.month
        today = d.day
        
        days = calendar.monthrange(year, month)[1]  
        
        if today > days:
            afterday = days
        else:
            afterday = today
        return datetime.datetime(year,month,afterday).strftime(dateFormat)

    @staticmethod
    def firstDayOfNextMonth(dateFormat):
        d = datetime.datetime.now()
        year = d.year
        month = d.month
        if month+1 > 12 :
            month = 1
            year += 1
        else :
            month += 1
        
        return datetime.datetime(year,month,1).strftime(dateFormat)

    @staticmethod
    def firstDayOfMonth(year, month, dateFormat):
        return datetime.datetime(year,month,1).strftime(dateFormat)

    @staticmethod
    def firstDayOfMonthThisYear(month, dateFormat):
        d = datetime.datetime.now()
        year = d.year
        return datetime.datetime(year,month,1).strftime(dateFormat)

    @staticmethod
    def getMilSecNow():
        return time.time()

if __name__ == '__main__':
    dt = DateTimeManager()
    # print(dt.getCurrentDateTime())
    # print(dt.getCurrentDate())
    print(dt.getDateTime())
    # print(dt.getCurrentTime())
    # print(dt.getTime())
    # print(dt.formated_time('%Y-%m-%d %H:%M:%S'))
    print(time.time())
    print(datetime.datetime.now())

    print(dt.getCurrentDate())

    print(dt.getMilSecNow())


    
