import sys
import os


print(f"Current Working Directory: {os.getcwd()}")
print(f"Python sys.path: {sys.path}")
print("-" * 50) 


from PySide6.QtWidgets import QApplication

from core.database import SessionLocal, create_database_tables
from repositories.task_repository import SqlAlchemyTaskRepository
from views.main_window import MainWindow
from presenters.task_presenter import TaskPresenter

def run_application():
    print("MAIN.PY - تابع run_application شروع شد.") # ردیابی
    
    print("MAIN.PY - تلاش برای ایجاد جداول پایگاه داده...")
    create_database_tables()
    print("MAIN.PY - مرحله ایجاد جداول پایگاه داده انجام شد.")

    print("MAIN.PY - تلاش برای گرفتن session از پایگاه داده...")
    db_session = SessionLocal()
    print("MAIN.PY - Session پایگاه داده گرفته شد.")
    
    try:
        print("MAIN.PY - در حال تنظیم QApplication...")
        app = QApplication(sys.argv)
        print("MAIN.PY - QApplication ایجاد شد.")
        
        print("MAIN.PY - در حال ایجاد MainWindow (View)...")
        task_view = MainWindow()
        print("MAIN.PY - MainWindow (View) ایجاد شد.")
        
        print("MAIN.PY - در حال ایجاد SqlAlchemyTaskRepository...")
        task_repository = SqlAlchemyTaskRepository(db_session=db_session)
        print("MAIN.PY - SqlAlchemyTaskRepository ایجاد شد.")
        
        print("MAIN.PY - در حال ایجاد TaskPresenter...")
        task_presenter = TaskPresenter(view=task_view, repository=task_repository)
        print("MAIN.PY - TaskPresenter ایجاد شد، View و Presenter باید به هم متصل شده باشند.")
        
        print("MAIN.PY - تلاش برای نمایش پنجره اصلی...")
        task_view.show() 
        print("MAIN.PY - متد show() پنجره اصلی فراخوانی شد.")
        
        print("MAIN.PY - شروع حلقه رویداد Qt (app.exec)...")
        exit_code = app.exec()
        print(f"MAIN.PY - حلقه رویداد Qt پایان یافت با کد خروج: {exit_code}")
        sys.exit(exit_code)
    
    finally:
        print("MAIN.PY - در حال بستن session پایگاه داده...")
        db_session.close()
        print("MAIN.PY - Session پایگاه داده بسته شد.")

if __name__ == "__main__":
    print("MAIN.PY - برنامه شروع می‌شود...")
    run_application()
    print("MAIN.PY - برنامه به پایان رسید.")