# pyright: strict

import requests
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Callable, List
from utils import View, ComponentStatus
            
            
class StatusModel:
    def get_github_status(self) -> List[ComponentStatus]: 
        
        url = "https://www.githubstatus.com/api/v2/summary.json"
        
        response = requests.get(url)
        response.raise_for_status()
        
        raw_data: dict[str, Any] = response.json()
        raw_components: List[dict[str, Any]] = raw_data.get('components', [])
        
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

    def display_raw_status(self, data: dict[str, Any]) -> None:
        print(data)
        
class TkinterStatusView:
    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._root.title("Github System Status")
        self._root.geometry("450x500")
        self._root.minsize(300, 300)
        
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)
        
        top_frame = ttk.Frame(self._root, padding=10)
        top_frame.grid(row=0, column=0, sticky="ew")
        
        title_label = ttk.Label(
            top_frame,
            text="Current Component Status",
            font=("Helvetica", 14, "bold")
        )
        title_label.pack(side="left")
        
        self._refresh_button = ttk.Button(top_frame, text="Refresh")
        self._refresh_button.pack(side="right")
        
        table_frame = ttk.Frame(self._root, padding=10)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        columns = ("name", "status")
        self._tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self._tree.heading("name", text="Component")
        self._tree.heading("status", text="Status")
        
        self._tree.column("name", width=250, anchor="w")
        self._tree.column("status", width=150, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self._tree.yview) #pyright: ignore
        self._tree.configure(yscrollcommand=scrollbar.set)
        
        self._tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self._tree.tag_configure("operational", foreground="#2e7d32")
        self._tree.tag_configure("outage", foreground="#d32f2f", font=("Helvetica", 10, "bold"))
             
    def bind_refresh_action(self, callback: Callable[[], None]) -> None:
        self._refresh_button.config(command=callback)
        
    def display_status(self, status_list: List[ComponentStatus]) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)
            
        for component in status_list:
            tag = "operational" if component.is_operational else "outage"
            display_status = component.status.replace("_", " ").title()
            
            self._tree.insert(
                "", 
                "end", 
                values=(component.name, display_status), 
                tags=(tag,)
            )
            
    def display_error(self, error: Exception) -> None:
        messagebox.showerror("Connection Error", f"Failed to fetch status:\n\n{error}")
            
    def display_raw_status(self, data: dict[str, Any]) -> None:
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
            
class TkinterStatusController:
    def __init__(self, model: StatusModel, view: TkinterStatusView) -> None:
        self._model = model
        self._view = view
        
        self._view.bind_refresh_action(self.fetch_and_update)
        
    def fetch_and_update(self) -> None:
        try:
            data = self._model.get_github_status()
            self._view.display_status(data)
        except requests.exceptions.RequestException as e:
            self._view.display_error(e)
            
    def run(self) -> None:
        self.fetch_and_update()
            
            
if __name__ == "__main__":
    
    root = tk.Tk()
    
    model = StatusModel()
    view: View = TkinterStatusView(root)
    
    controller = TkinterStatusController(model, view)
    
    controller.run()
    root.mainloop()