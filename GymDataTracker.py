from GymDataManager import GymDataManager
from TimeManager import TimeManager
from DataScraper import DataScraper
from JsonHandler import JsonHandler


class GymDataTracker:
    def __init__(self) -> None:
        self.tm = TimeManager()
        self.ds = DataScraper()
        self.jsh = JsonHandler()
        self.gdm = GymDataManager()
        
    def run(self):
        # Time Check
        self.tm.printCurrentTime()
        if not self.tm.checkValidTime():
            # Run clearing of old data at the end of the day
            if self.tm.getHourAMPM() == "10 PM":
                print("Reached end of the day, begin clearing of old data")
                self.gdm.clear_old_data()
                print("- DONE - Clearing of old data completed!")
                
            print("Process ran during gym closed hours, stopping further tasks...")
            self.clean_up()
            return
        
        # Request Json data from API
        json_data = self.ds.requestJSONData()
        # Processing JSON data, converting to Dict 
        gym_data = self.jsh.extractGymCapacityData(json_data)
        
        if not self.jsh.isOpen(json_data):
            print("Gyms closed during usual hours, stopping further tasks...")
            self.clean_up()
            
        # Adding new data to the db
        self.saveGymDataToSupabase(gym_data, self.tm.getHourAMPM(), self.tm.getCurrentDay())
        
        self.clean_up()
        
        print("- DONE - Tracker finished running")
        
    def saveGymDataToSupabase(self, gym_data, time_hr_pm, day):
        print("Saving extracted gym data to Supabase...")
        entries = []
        for gym_name, capacity in gym_data.items():
            entries.append({"gym_name": gym_name, "day": day, "hour": time_hr_pm, "capacity": capacity})
        self.gdm.add_bulk_entry_to_supabase(entries)
        print("Save Completed!")
        
    # Closes various sessions before terminating process
    def clean_up(self):
        self.gdm.sign_out_of_supabase()
