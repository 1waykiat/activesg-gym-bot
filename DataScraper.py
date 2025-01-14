from curl_cffi import requests as cureq

class DataScraper:
    
    # Request for JSON data from the ActiveSG Gym Capacity API, and return the retrieved data in JSON
    def requestJSONData(self):
        try:
            print("Requesting JSON data from the website...")
            url = "https://activesg.gov.sg/api/trpc/pass.getFacilityCapacities?input=%7B%22json%22%3Anull%2C%22meta%22%3A%7B%22values%22%3A%5B%22undefined%22%5D%7D%7D"
            resp = cureq.get(url,impersonate="chrome")
            print(f'Status Code: {resp.status_code}')
            resp.raise_for_status()
            print("Successfully retrieved ActiveSG Gym Capacity JSON data!")
            
            return resp.json()
        except Exception as e:
            print("Error has occured while requesting for data: ", e)
            