from enum import StrEnum
from typing import Any


class ContestStatus(StrEnum):
    PENDING = "Pending"
    RUNNING = "Running"
    FINISHED = "Finished"
    CANCELLED = "Cancelled"

    def validate_contest_status(status) -> Any:
        if not isinstance(status, str):
            raise ValueError("O status do concurso deve ser uma string.")

        try:
            _ = ContestStatus(status)
        except ValueError:
            valid_values = ", ".join(e.value for e in ContestStatus)
            error_message = (
                f"Status do concurso inválido: {status}. "
                f"Deve ser um dos valores: {valid_values}"
            )
            raise ValueError(error_message)
