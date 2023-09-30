from enum import StrEnum


class ContestStatus(StrEnum):
    PENDING = "Pending"
    RUNNING = "Running"
    FINISHED = "Finished"
    CANCELLED = "Cancelled"
