from typing import Optional, Dict, Any, List
import datetime
from views.i_task_view import ITaskView
from repositories.i_task_repository import ITaskRepository
from models.task import Task 
from enums.task_enums import TaskPriority, TaskStatus

class TaskPresenter:
    def __init__(self, view: ITaskView, repository: ITaskRepository):
        self._view = view
        self._repository = repository
        self._view.set_presenter(self)
        self._editing_task_id: Optional[int] = None

    def _task_orm_to_display_dict(self, task: Task) -> Dict[str, Any]:
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description or "",
            "priority": task.priority.value,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "status": task.status.value,
            "created_at": task.created_at.isoformat() if task.created_at else None
        }

    def _view_data_to_repo_data(self, view_data: Dict[str, Any]) -> Dict[str, Any]:
        repo_data = view_data.copy()
        if "priority" in repo_data and isinstance(repo_data["priority"], str):
            try:
                repo_data["priority"] = TaskPriority(repo_data["priority"])
            except ValueError:
                repo_data["priority"] = TaskPriority.MEDIUM 
        
        if "status" in repo_data and isinstance(repo_data["status"], str):
            try:
                repo_data["status"] = TaskStatus(repo_data["status"])
            except ValueError:
                repo_data["status"] = TaskStatus.TODO
        return repo_data

    def load_initial_tasks(self):
        try:
            tasks_orm = self._repository.get_all_tasks(order_by_column="due_date", order_desc=False)
            tasks_display_data = [self._task_orm_to_display_dict(task) for task in tasks_orm]
            self._view.display_tasks(tasks_display_data)
        except Exception as e:
            self._view.show_feedback_message(f"خطا در بارگذاری وظایف: {e}", is_error=True)

    def add_or_update_task_requested(self):
        if self._editing_task_id is not None:
            task_data_from_view = self._view.get_task_update_data()
            if task_data_from_view:
                repo_data = self._view_data_to_repo_data(task_data_from_view)
                try:
                    updated_task = self._repository.update_task(self._editing_task_id, repo_data)
                    if updated_task:
                        self._view.show_feedback_message(f"وظیفه '{updated_task.title}' با موفقیت به‌روزرسانی شد.")
                        self._editing_task_id = None 
                    else:
                        self._view.show_feedback_message(f"خطا: وظیفه با شناسه {self._editing_task_id} یافت نشد.", is_error=True)
                except Exception as e:
                    self._view.show_feedback_message(f"خطا در به‌روزرسانی وظیفه: {e}", is_error=True)
        else:
            task_data_from_view = self._view.get_new_task_data()
            if task_data_from_view:
                repo_data = self._view_data_to_repo_data(task_data_from_view)
                try:
                    new_task = self._repository.add_task(repo_data)
                    self._view.show_feedback_message(f"وظیفه جدید '{new_task.title}' با موفقیت اضافه شد.")
                except Exception as e:
                    self._view.show_feedback_message(f"خطا در افزودن وظیفه: {e}", is_error=True)
        
        self._view.clear_input_fields()
        self.load_initial_tasks()

    def delete_task_requested(self):
        task_id = self._view.get_selected_task_identifier()
        if task_id is None:
            self._view.show_feedback_message("هیچ وظیفه‌ای برای حذف انتخاب نشده است.", is_error=True)
            return

        task_to_delete = self._repository.get_task_by_id(task_id)
        if task_to_delete is None:
            self._view.show_feedback_message(f"خطا: وظیفه با شناسه {task_id} یافت نشد.", is_error=True)
            return

        title_preview = task_to_delete.title
        if self._view.get_confirmation("تأیید حذف", f"آیا از حذف وظیفه '{title_preview}' (ID: {task_id}) مطمئن هستید؟"):
            try:
                if self._repository.delete_task(task_id):
                    self._view.show_feedback_message(f"وظیفه '{title_preview}' با موفقیت حذف شد.")
                    if self._editing_task_id == task_id:
                        self._editing_task_id = None
                        self._view.clear_input_fields()
                else:
                    self._view.show_feedback_message(f"خطا در حذف وظیفه با شناسه {task_id}.", is_error=True)
            except Exception as e:
                self._view.show_feedback_message(f"خطا در حذف وظیفه: {e}", is_error=True)
            self.load_initial_tasks()

    def edit_task_requested(self):
        task_id = self._view.get_selected_task_identifier()
        if task_id is None:
            self._view.show_feedback_message("هیچ وظیفه‌ای برای ویرایش انتخاب نشده است.", is_error=True)
            return
        
        try:
            task_orm = self._repository.get_task_by_id(task_id)
            if task_orm:
                self._editing_task_id = task_id
                task_display_data = self._task_orm_to_display_dict(task_orm)
                self._view.populate_edit_fields(task_display_data)
                self._view.show_feedback_message(f"در حال ویرایش وظیفه: '{task_orm.title}'. برای لغو، فیلدها را پاک کنید.", is_error=False)
            else:
                self._view.show_feedback_message(f"وظیفه با شناسه {task_id} یافت نشد.", is_error=True)
        except Exception as e:
            self._view.show_feedback_message(f"خطا در بارگذاری وظیفه برای ویرایش: {e}", is_error=True)