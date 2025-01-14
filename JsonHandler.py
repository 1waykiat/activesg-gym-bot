import json

class JsonHandler:
    # Processes the Json file, extracts capacity data for every gym and returns it in a
    # dictionary, with a format of {gym_name: capacity}
    def extractGymCapacityData(self, json_data):
        print("Extracting gym capacity data...")
        gyms_json = json_data['result']['data']['json']['gymFacilities']
        gym_data = dict()

        for gym in gyms_json:   
            gym_data[gym['name']] = gym['capacityPercentage']
        
        print("Successfully extracted gym data!")
        print(json.dumps(gym_data, indent= 4, sort_keys=True))
            
        return gym_data
    