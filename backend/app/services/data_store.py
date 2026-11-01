import json
from collections import defaultdict
from pathlib import Path

from app.models.schemas import ProgressState


class LocalStore:
    def __init__(self) -> None:
        root = Path(__file__).resolve().parents[3]
        self.data_path = root / "data/examples/course_data.json"
        with self.data_path.open("r", encoding="utf-8") as fp:
            self.data = json.load(fp)
        self.progress: dict[str, dict[str, str]] = defaultdict(dict)
        self.practice_attempts: list[dict] = []

    def course(self) -> dict:
        return self.data

    def modules(self) -> list[dict]:
        return self.data["modules"]

    def update_progress(self, module_id: str, item_id: str, status: ProgressState) -> None:
        self.progress[module_id][item_id] = status.value

    def module_progress(self, module_id: str) -> dict[str, str]:
        return self.progress.get(module_id, {})

    def add_attempt(self, attempt: dict) -> None:
        self.practice_attempts.append(attempt)


store = LocalStore()
