

import requests
import json
import os
import pandas as pd

execution_path = os.path.dirname(os.path.abspath(__file__))


class DataModel(object):
    
    
    def __init__(self, logger):
        self.url = None
        self.logger = logger


    
    @classmethod
    def set_url(self, url : str):
        try:
            self.url = url
            
            return self.url
        
        
        except Exception as exception:
            return self.logger.critical(exception)




    @classmethod
    def get_data(self):
        
        try:
            if self.url is not None:
                
                response = requests.get(self.url)
                
                if response.status_code == 200:
                    
                    data = json.loads(response.text)
                    
                    
                    return data
                
                else:
                    
                    return None
        
        
        except Exception as exception:
            return self.logger.critical(exception)




    @classmethod
    def save_data(self, file, data):
        try:
            with open(file, 'w') as json_file:
                json_file.write(data)
            json_file.close()
        
        
        except Exception as exception:
            return self.logger.critical(exception)





    @classmethod
    def convert_path_to_windows(self, path : str):
        try:
            path = path.replace('/', '\\')
            
            if os.path.exists(path):
                return path
        
        
        except Exception as exception:
            return self.logger.critical(exception)




    @classmethod
    def convert_json_to_xlsx(self, json_file_path : str, xlsx_file_path : str):

        try:
            df = pd.read_json(json_file_path)
            df.to_excel(xlsx_file_path)
        
        
        except Exception as exception:
            return self.logger.critical(exception)




