

import requests
import json
import os


execution_path = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(execution_path, "output")


class DataModel(object):
    
    
    def __init__(self, Controller):
        self.url = None
        self.Controller = Controller

    
    @classmethod
    def set_url(self, url : str):
        self.url = url
        
        return self.url
    
    @classmethod
    def get_data(self):
        
        if self.url is not None:
            
            response = requests.get(self.url)
            
            if response.status_code == 200:
                
                data = json.loads(response.text)
                
                
                return data
            
            else:
                
                return None
    
    @classmethod
    def save_data(self, file):
        
        
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        
        json_file = os.path.join(output_path, file)
        
        with open(json_file, 'w') as output_file:
            output_file.write(json.dumps(self.get_data(), indent=4))
        output_file.close()

        

