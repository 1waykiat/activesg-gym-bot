from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime
import asyncio

load_dotenv()

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
SUPABASE_EMAIL = os.environ.get('SUPABASE_EMAIL')
SUPABASE_PASSWORD = os.environ.get('SUPABASE_PASSWORD')

class GymDataManager:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.supabase.auth.sign_in_with_password({"email": SUPABASE_EMAIL, "password": SUPABASE_PASSWORD})
        
    # Supabase Functions
    
    def add_entry_to_supabase(self, gym_name, day, hour, capacity):
        try:
            self.supabase.rpc("add_entry", {
                "gym_name": gym_name,
                "day": day,
                "hour": hour,
                "capacity" : capacity
            }).execute()
        except Exception as e:
            print('Error: ', e)
            
    def add_bulk_entry_to_supabase(self, entries):
        try:
            self.supabase.rpc("add_gym_entries", {"entries": entries}).execute()
        except Exception as e:
            print('Error: ', e)
            
    def get_avg_cap(self, gym_name, day):
        """
            get_average_capacity_gym rpc function:
            select 
                gym_capacities.hour,
                round(avg(gym_capacities.capacity)) AS average_capacity
            from gym_capacities
            where
                gym_capacities.gym_name = $1 and
                gym_capacities.day = $2
            group by gym_capacities.hour;
        """
        try:
            data = self.supabase.rpc("get_average_capacity_gym", {
                "gym_name": gym_name,
                "day": day
            }).execute().data
            
            sorted_data = sorted(data, key=lambda x: datetime.strptime(x['hour'], '%I %p'))
            
            return sorted_data
        except Exception as e:
            print('Error: ', e)

    def get_all_gyms(self):
        try:
            data = self.supabase.rpc("get_all_gyms").execute().data
            gym_lst = []
            for entry in data:
                gym_lst.append(entry['gym_name'])
    
            return gym_lst
        except Exception as e:
            print("Error: ", e)
            
    def clear_old_data(self):
        try:
            print("Deleting old data entries...")
            deleted_count = self.supabase.rpc("count_old_entries").execute().data
            self.supabase.rpc("delete_old_entries").execute()
            print("Old entries longer than 2 months have been cleared.")
            print(f"Number of old entries deleted: {deleted_count}")
        except Exception as e:
            print("Error: ", e)
            
    # Refreshes the Supabase session every 50 mins (10 mins before session expires)
    async def refresh_session_periodically(self):
        while True:
            try:
                print("Refreshing supabase session...")
                self.supabase.auth.sign_in_with_password({"email": SUPABASE_EMAIL, "password": SUPABASE_PASSWORD})
                self.supabase.auth.refresh_session()
                print("Session refreshed sucessfully!")
            except Exception as e:
                print("Failed to refresh client: ", e)
            await asyncio.sleep(3000)

    def sign_out_of_supabase(self):
        self.supabase.auth.sign_out()
        