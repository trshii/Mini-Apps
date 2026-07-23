# pyright: strict

import requests
from typing import Any, List
from dataclasses import dataclass

@dataclass
class ComponentStatus:
    name: str
    status: str
    
    @property
    def is_operational(self) -> bool:
        return self.status.lower() == 'operational'
            
            

class StatusModel:
    def get_github_status(self) -> List[ComponentStatus]: 
        
        url = "https://www.githubstatus.com/api/v2/summary.json"
        
        response = requests.get(url)
        response.raise_for_status()
        
        raw_data: dict[str, Any] = response.json()
        raw_components: list[dict[str, Any]] = raw_data.get('components', [])
        
        status_list: List[ComponentStatus] = []
        
        for item in raw_components:
            name = str(item.get('name', ''))
            status = str(item.get('status', 'Unknown'))
            
            if not name or name.startswith('Visit'):
                continue
            
            status_list.append(ComponentStatus(name=name, status=status))
            
        return status_list
        
            
            
class StatusView:
    def display_status(self, status_list: List[ComponentStatus]) -> None:
        for component in status_list:
            if component.is_operational:
                print(f"{component.name}: \033[92m{component.status.capitalize()}\033[0m")
            else:
                print(f"{component.name}: \033[91m*** {component.status.upper()} ***\033[0m") 
        
    def display_error(self, error: Exception) -> None:
        print(f"Error fetching status from GitHub: {error}")
        
    def display_raw_status(self, data: Any) -> None:
        print(data)
        
        
        
class StatusController:
    def __init__(self, model: StatusModel, view: StatusView) -> None:
        self._model = model
        self._view = view
        
    def run(self) -> None:
        model = self._model
        view = self._view
        
        try:
            data = model.get_github_status()
            view.display_status(data)
            
        except requests.exceptions.RequestException as e:
            view.display_error(e)
            
            
if __name__ == "__main__":
    model = StatusModel()
    view = StatusView()
    controller = StatusController(model, view)
    
    controller.run()