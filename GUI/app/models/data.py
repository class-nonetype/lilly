

import requests
import json
import os


execution_path = os.path.dirname(os.path.abspath(__file__))


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
    def save_data(self, file, data):
        
        with open(file, 'w') as json_file:
            json_file.write(data)
        json_file.close()


    @classmethod
    def convert_path_to_windows(self, path : str):
        path = path.replace('/', '\\')
        
        if os.path.exists(path):
            return path

        

