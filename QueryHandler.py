from TimeManager import TimeManager
from JsonHandler import JsonHandler
from DataScraper import DataScraper
from JsonHandler import JsonHandler

class QueryHandler:
    def __init__(self, gdm):
        self.tm = TimeManager()
        self.jsh = JsonHandler()
        self.gdm = gdm
        self.ds = DataScraper()
        
    def start(self):
        return '''Hello, I'm GymBot! 💪🤖
        
Get the latest gym capacity updates and crowd trends for the ActiveSG gyms! 
Start off with one of the 2 commands below! For full list of commands and what they do, use the /help command to learn more.
    '''
    
    def help(self):
        return '''List of Commands ⚙️:
    
/start - Initialize bot
/help - List all commands and additional information on bot
/current - View current gym capacities for all gyms
/average - View average gym capacity data of selected gym for all hours for current day
/info - Get additional miscellaneous info on bot
    '''
    
    def info(self):
        return '''<b>Additional Information</b>
    
<u>Capacity level to Color Code:</u>
🟢 0% - 19%
🟡 20% - 39%
🟠 40% - 59%
🔴 60% - 100%
    
<u>Regarding average gym capacity data:</u>
Gym capacity averages are being calculated from historical data tracked up to 2 months ago
    
    '''
     
    def avg_cap_for_gym(self, gym_name):
        day = self.tm.getCurrentDay()
        hour = self.tm.getHourAMPM()
        avg_data = self.gdm.get_avg_cap(gym_name, day)
        avg_capacity = 0;
        
        if len(avg_data) == 0:
            return f"Sorry, unable to find any data for '{gym_name}'"
        
        # Average gym capacity data text block
        text = f"💪 Average gym capacity data of <b>{gym_name}</b> by hour on <b>{day}</b>:\n"
        for entry in avg_data:
            if hour == entry['hour']:
                avg_capacity = entry['average_capacity']
            text += f"\n{self.capacity_colour(entry['average_capacity'])} {entry['hour']}: <b>{entry['average_capacity']}</b> % {'(<b>Current Hour</b> ⏰)' if hour == entry['hour'] else ''}"
        
        # Compare current capacity with average capacity text block
        if (self.tm.checkValidTime()):
            json_data = self.ds.requestJSONData()
            gym_data = self.jsh.extractGymCapacityData(json_data)
            curr_capacity = gym_data[gym_name]
            
            text += f"\n\n 👥 Current Capacity: <b>{curr_capacity}</b> %\n"
            text += self.compare_current_cap_with_avg(curr_capacity, avg_capacity)
        
        return text
    
    def compare_current_cap_with_avg(self, curr_capacity, avg_capacity):
        # Compare curr with avg data
        percent_diff = curr_capacity - avg_capacity
        if (abs(percent_diff) >= 10):
            # Significant Difference
            return f"<b>Significantly {'more' if percent_diff > 0 else 'less'}</b> crowded than usual! {'🔴' if percent_diff > 0 else '🟢'}"
        elif (abs(percent_diff) >= 5):
            # Slight Difference
            return f"Slightly {'more' if percent_diff > 0 else 'less'} crowded than usual!"
        else:
            # Similar to usual
            return f"Seems to be as crowded as usual!"
        
    
    def current_cap(self):
        if not self.tm.checkValidTime():
            return "🚫 ActiveSG Gyms are currently closed!"

        json_data = self.ds.requestJSONData()
        gym_data = self.jsh.extractGymCapacityData(json_data)
        
        text = "🏋 Gym capacities at the current moment: 🏋\n"
        for gym_name, capacity in gym_data.items():
            text += f"\n{self.capacity_colour(capacity)} {gym_name}: <b>{capacity}</b> %"
        
        return text
    
    def capacity_colour(self, capacity):
        if capacity < 20:
            return "🟢"
        elif capacity < 40:
            return "🟡"
        elif capacity < 60:
            return "🟠"
        else: # capacity > 60
            return "🔴"
        