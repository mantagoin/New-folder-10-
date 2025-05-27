import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget,
    QLineEdit, QPushButton, QMessageBox, QListWidget, QListWidgetItem,
    QComboBox, QDateEdit
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor
from typing import List, Optional, Dict, Any, Tuple
from .i_task_view import ITaskView
from enums.task_enums import TaskPriority, TaskStatus

class MainWindow(QMainWindow, ITaskView):
    def __init__(self):
        super().__init__()
        self._presenter = None 
        self.setWindowTitle("برنامه مدیریت وظایف (معماری MVP)")
        self.setGeometry(100, 100, 750, 650)
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        form_layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("عنوان وظیفه (مثلاً: ارائه پروژه)")
        form_layout.addWidget(QLabel("عنوان وظیفه:"))
        form_layout.addWidget(self.title_input)

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("توضیحات (مثلاً: آماده‌سازی اسلایدها)")
        form_layout.addWidget(QLabel("توضیحات (اختیاری):"))
        form_layout.addWidget(self.desc_input)

        options_h_layout = QHBoxLayout()

        priority_v_layout = QVBoxLayout()
        priority_v_layout.addWidget(QLabel("اولویت:"))
        self.priority_input = QComboBox()
        self.priority_input.addItems([p.value for p in TaskPriority])
        self.priority_input.setCurrentText(TaskPriority.MEDIUM.value)
        priority_v_layout.addWidget(self.priority_input)
        options_h_layout.addLayout(priority_v_layout)

        duedate_v_layout = QVBoxLayout()
        duedate_v_layout.addWidget(QLabel("تاریخ سررسید:"))
        self.due_date_input = QDateEdit()
        self.due_date_input.setDate(QDate.currentDate())
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDisplayFormat("yyyy-MM-dd")
        duedate_v_layout.addWidget(self.due_date_input)
        options_h_layout.addLayout(duedate_v_layout)
        
        status_v_layout = QVBoxLayout()
        status_v_layout.addWidget(QLabel("وضعیت:"))
        self.status_input = QComboBox()
        self.status_input.addItems([s.value for s in TaskStatus])
        self.status_input.setCurrentText(TaskStatus.TODO.value)
        status_v_layout.addWidget(self.status_input)
        options_h_layout.addLayout(status_v_layout)

        form_layout.addLayout(options_h_layout)

        self.add_task_button = QPushButton("افزودن/به‌روزرسانی وظیفه")
        self.add_task_button.clicked.connect(self._on_add_update_task_clicked)
        form_layout.addWidget(self.add_task_button)
        
        self.main_layout.addLayout(form_layout)

        self.main_layout.addWidget(QLabel("لیست وظایف:"))
        self.tasks_list_widget = QListWidget()
        self.tasks_list_widget.itemDoubleClicked.connect(self._on_task_item_double_clicked)
        self.main_layout.addWidget(self.tasks_list_widget)

        buttons_h_layout = QHBoxLayout()
        self.edit_task_button = QPushButton("بارگذاری وظیفه برای ویرایش")
        self.edit_task_button.clicked.connect(self._on_edit_task_clicked)
        buttons_h_layout.addWidget(self.edit_task_button)

        self.delete_task_button = QPushButton("حذف وظیفه انتخاب شده")
        self.delete_task_button.clicked.connect(self._on_delete_task_clicked)
        buttons_h_layout.addWidget(self.delete_task_button)
        self.main_layout.addLayout(buttons_h_layout)

        self.feedback_label = QLabel("آماده.")
        self.main_layout.addWidget(self.feedback_label)

    def set_presenter(self, presenter: Any):
        self._presenter = presenter

    def _on_add_update_task_clicked(self):
        if self._presenter:
            self._presenter.add_or_update_task_requested()

    def _on_delete_task_clicked(self):
        if self._presenter:
            self._presenter.delete_task_requested()
    
    def _on_edit_task_clicked(self):
        if self._presenter:
            self._presenter.edit_task_requested()

    def _on_task_item_double_clicked(self, item: QListWidgetItem):
        if self._presenter:
            self._presenter.edit_task_requested()

    def display_tasks(self, tasks_display_data: List[Dict[str, Any]]):
        self.tasks_list_widget.clear()
        if not tasks_display_data:
            self.tasks_list_widget.addItem("هیچ وظیفه‌ای برای نمایش وجود ندارد.")
            return

        for task_data in tasks_display_data:
            display_text = (
                f"'{task_data.get('title', '')}' (ID: {task_data.get('id')}) | "
                f"وضعیت: {task_data.get('status', '')} | اولویت: {task_data.get('priority', '')} | "
                f"سررسید: {task_data.get('due_date', 'نامشخص')}"
            )
            if task_data.get('description'):
                display_text += f" | توضیحات: {task_data['description'][:20]}..."
            
            list_item = QListWidgetItem(display_text)
            list_item.setData(Qt.UserRole, task_data.get('id'))

            priority_str = task_data.get('priority', TaskPriority.MEDIUM.value)
            if priority_str == TaskPriority.HIGH.value:
                list_item.setBackground(QColor("salmon"))
            elif priority_str == TaskPriority.MEDIUM.value:
                list_item.setBackground(QColor("lightyellow"))
            elif priority_str == TaskPriority.LOW.value:
                list_item.setBackground(QColor("lightgreen"))
            
            self.tasks_list_widget.addItem(list_item)

    def get_new_task_data(self) -> Optional[Dict[str, Any]]:
        title = self.title_input.text().strip()
        if not title:
            self.show_feedback_message("عنوان وظیفه نمی‌تواند خالی باشد.", is_error=True)
            QMessageBox.warning(self, "ورودی نامعتبر", "عنوان وظیفه نمی‌تواند خالی باشد.")
            return None
        
        due_date_q = self.due_date_input.date()
        return {
            "title": title,
            "description": self.desc_input.text().strip(),
            "priority": self.priority_input.currentText(),
            "due_date": due_date_q.toPython() if due_date_q.isValid() else None,
            "status": self.status_input.currentText()
        }

    def get_task_update_data(self) -> Optional[Dict[str, Any]]:
        return self.get_new_task_data()

    def get_selected_task_identifier(self) -> Optional[Any]:
        current_item = self.tasks_list_widget.currentItem()
        if current_item:
            return current_item.data(Qt.UserRole)
        return None

    def populate_edit_fields(self, task_data: Dict[str, Any]):
        self.title_input.setText(task_data.get("title", ""))
        self.desc_input.setText(task_data.get("description", ""))
        self.priority_input.setCurrentText(task_data.get("priority", TaskPriority.MEDIUM.value))
        
        due_date_obj = task_data.get("due_date")
        if isinstance(due_date_obj, str):
             q_date = QDate.fromString(due_date_obj, "yyyy-MM-dd")
             if q_date.isValid():
                 self.due_date_input.setDate(q_date)
             else:
                 self.due_date_input.setDate(QDate.currentDate())
        elif due_date_obj: 
            self.due_date_input.setDate(QDate(due_date_obj.year, due_date_obj.month, due_date_obj.day))
        else:
            self.due_date_input.setDate(QDate.currentDate())
            
        self.status_input.setCurrentText(task_data.get("status", TaskStatus.TODO.value))
        self.feedback_label.setText(f"در حال ویرایش وظیفه: '{task_data.get('title', '')}'")

    def clear_input_fields(self):
        self.title_input.clear()
        self.desc_input.clear()
        self.priority_input.setCurrentText(TaskPriority.MEDIUM.value)
        self.due_date_input.setDate(QDate.currentDate())
        self.status_input.setCurrentText(TaskStatus.TODO.value)
        self.feedback_label.setText("آماده برای افزودن وظیفه جدید.")

    def show_feedback_message(self, message: str, is_error: bool = False):
        self.feedback_label.setText(message)
        if is_error:
            self.feedback_label.setStyleSheet("color: red;")
        else:
            self.feedback_label.setStyleSheet("color: green;")

    def get_confirmation(self, title: str, message: str) -> bool:
        reply = QMessageBox.question(self, title, message,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes

    def get_filters(self) -> Optional[Dict[str, Any]]:
        return None

    def get_order_by(self) -> Optional[Tuple[str, bool]]:
        return None

    def show(self):
        super().show()
        if self._presenter:
            self._presenter.load_initial_tasks()