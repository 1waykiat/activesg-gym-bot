from datetime import datetime
import pytz

openingHour = 7
closingHour = 22

class TimeManager:      
    
    # Returns datetime.datetime object of current time in Singapore Time
    def getCurrentTime(self):
        singapore_tz = pytz.timezone('Asia/Singapore')
        utc_now = datetime.now(pytz.utc)
        sg_time = utc_now.astimezone(singapore_tz)   
        return sg_time
    
    # Returns day of the week in string (e.g. "Monday", "Saturday")
    def getCurrentDay(self):
        sg_time = self.getCurrentTime()
        return sg_time.strftime('%A')
    
    # Returns string of format "** AM/PM" where ** represents the current hour (e.g. 2 PM, 11 AM)
    def getHourAMPM(self):
        sg_time = self.getCurrentTime()
        return sg_time.strftime('%I %p').lstrip('0')
    
    # Returns true if it is currently opening hours
    def checkValidTime(self):
        sg_time = self.getCurrentTime()
        return sg_time.hour >= openingHour and sg_time.hour < closingHour
    
    # Prints the current time in Singapore Time
    def printCurrentTime(self):
        print("Current Time in Singapore: ", self.getCurrentTime())
        