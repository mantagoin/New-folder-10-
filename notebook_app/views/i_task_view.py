from abc import abstractmethod 
from typing import List, Optional, Dict, Any, Tuple

class ITaskView(object): 
    @abstractmethod
    def display_tasks(self, tasks_display_data: List[Dict[str, Any]]):
        pass

    @abstractmethod
    def get_new_task_data(self) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_task_update_data(self) -> Optional[Dict[str, Any]]:
        pass
        
    @abstractmethod
    def get_selected_task_identifier(self) -> Optional[Any]:
        pass

    @abstractmethod
    def populate_edit_fields(self, task_data: Dict[str, Any]):
        pass

    @abstractmethod
    def clear_input_fields(self):
        pass

    @abstractmethod
    def show_feedback_message(self, message: str, is_error: bool = False):
        pass

    @abstractmethod
    def get_confirmation(self, title: str, message: str) -> bool:
        pass
    
    @abstractmethod
    def get_filters(self) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_order_by(self) -> Optional[Tuple[str, bool]]:
        pass

    @abstractmethod
    def set_presenter(self, presenter: Any):
        pass

    @abstractmethod
    def show(self):
        pass