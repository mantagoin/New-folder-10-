import enum

class TaskPriority(enum.Enum):
    LOW = "کم"
    MEDIUM = "متوسط"
    HIGH = "زیاد"

class TaskStatus(enum.Enum):
    TODO = "برای انجام"
    IN_PROGRESS = "در حال انجام"
    DONE = "انجام شده"