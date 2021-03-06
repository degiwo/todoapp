"""Module to connect the CLI with the database"""

from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from todoapp.database import DatabaseHandler


class CurrentToDo(NamedTuple):
    """Class to hold the information of the current to-do"""

    todo: Dict[str, Any]
    error: str


class TodoAPI:
    """Class to connect DatabaseHandler logic with applications CLI"""

    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, description: List[str]):
        """Add a new to-do entry to the database"""
        description_text = " ".join(description)
        todo = {
            "Description": description_text,
            "Done": False,
        }
        read = self._db_handler.read_todos()
        read.todo_list.append(todo)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentToDo(todo, write.error)

    def get_todo_list(self) -> List[Dict[str, Any]]:
        """Return the current todo list"""
        read = self._db_handler.read_todos()
        return read.todo_list

    def set_done(self, todo_id: int) -> CurrentToDo:
        """Set a todo as done"""
        read = self._db_handler.read_todos()
        try:
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentToDo({}, "ID not found")
        todo["Done"] = True
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentToDo(todo, write.error)

    def remove(self, todo_id: int) -> CurrentToDo:
        """Remove a todo from the database using its id or index"""
        read = self._db_handler.read_todos()
        try:
            todo = read.todo_list.pop(todo_id - 1)
        except IndexError:
            return CurrentToDo({}, "ID not found")
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentToDo(todo, write.error)
