from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class Idea:
    title: str
    description: str

    def to_prompt_fragment(self) -> str:
        return f"Title: {self.title}\nDescription: {self.description}"


class IdeaStore:
    """Persistently rotates through a list of creative ideas."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._state: Dict[str, Any] = {"ideas": [], "last_index": -1}
        self._load()

    @property
    def ideas(self) -> List[Idea]:
        return [Idea(**item) for item in self._state.get("ideas", [])]

    def _load(self) -> None:
        if not self._path.exists():
            self._path.write_text(json.dumps(self._state, indent=2), encoding="utf-8")
        else:
            self._state = json.loads(self._path.read_text(encoding="utf-8"))
            if "ideas" not in self._state:
                raise ValueError(
                    "ideas.json must contain an 'ideas' array with idea objects"
                )
            self._state.setdefault("last_index", -1)

    def _save(self) -> None:
        self._path.write_text(json.dumps(self._state, indent=2, ensure_ascii=False), encoding="utf-8")

    def next_idea(self) -> Idea:
        ideas = self._state.get("ideas", [])
        if not ideas:
            raise ValueError(
                f"No ideas have been configured. Add entries to {self._path.resolve()}"
            )
        last_index = int(self._state.get("last_index", -1))
        next_index = (last_index + 1) % len(ideas)
        self._state["last_index"] = next_index
        self._save()
        idea_dict = ideas[next_index]
        return Idea(**idea_dict)


__all__ = ["Idea", "IdeaStore"]
