# pyright : strict

from typing import Protocol, List, Any
from dataclasses import dataclass

@dataclass
class ComponentStatus:
    name: str
    status: str
    
    @property
    def is_operational(self) -> bool:
        return self.status.lower() == 'operational'
    

class View(Protocol):
    def display_status(self, status_list: List[ComponentStatus]) -> None:
        ...
        
    def display_error(self, error: Exception) -> None:
        ...
        
    def display_raw_status(self, data: dict[str, Any]) -> None:
        ...
        
class Controller(Protocol):
    def run(self) -> None:
        ...