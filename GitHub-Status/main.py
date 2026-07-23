# pyright: strict

import requests
from typing import Any

class Status_Model:
    def get_github_status(self): 
        
        url = "https://www.githubstatus.com/api/v2/summary.json"
        
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        return data
            
            
class Status_View:
    def display_status(self, data: Any):
        for component in data.get('components', []):
            name = component.get('name')
            status = component.get('status')
            
            if name.startswith('Visit'):
                continue
            
            if status == 'operational':
                print(f"{name}: \033[92m{status.capitalize()}\033[0m")
            else:
                print(f"{name}: \033[91m*** {status.upper()} ***\033[0m") 
        
    def display_error(self, error: Exception):
        print(f"Error fetching status from GitHub: {e}")
        
    def display_raw_status(self, data: Any):
        print(data)
        
        
class Status_Controller:
    def __init__(self, model: Status_Model, view: Status_View):
        self._model = model
        self._view = view
        
    def run(self):
        model = self._model
        view = self._view
        
        try:
            data = model.get_github_status()
            view.display_status(data)
            
        except requests.exceptions.RequestException as e:
            view.display_error(e)
            
            
if __name__ == "__main__":
    model = Status_Model()
    view = Status_View()
    controller = Status_Controller(model, view)
    
    controller.run()