from datetime import datetime
from sqlalchemy import Column, DateTime


class TimestamperMixin:
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def pretty_timestamp(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")


class ReprMixin:
    def __repr__(self):
        classname = self.__class__.__name__
        fields = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith('_'))
        return f"<{classname}({fields})>"


class LoggerMixin:
    def log_create(self):
        print(f"[CREATE] {self.__class__.__name__} created at {datetime.now()}")

    def log_update(self):
        print(f"[UPDATE] {self.__class__.__name__} updated at {datetime.now()}")

    def log_delete(self):
        print(f"[DELETE] {self.__class__.__name__} deleted at {datetime.now()}")
