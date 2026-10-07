"""
definitions of fields structs logic
"""


from dataclasses import dataclass, fields
from typing import Any, Final
from copy import deepcopy
from functools import cache


@dataclass(frozen=True, eq=False)
class DatabaseField:
    name: str
    value: Any

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.name == other
        
        elif isinstance(other, DatabaseField):
            return self.name == other.name
        
        return False


@dataclass
class SongFields:
    """
    contains all fields names and their default values as immutable fields

    contains functions to get work on these fields
    """
    link: Final[DatabaseField] = DatabaseField("url", "")
    raw_title: Final[DatabaseField] = DatabaseField("full title", "")
    song_name: Final[DatabaseField] = DatabaseField("song name", "")
    authors: Final[DatabaseField] = DatabaseField("authors", [""])
    featuring: Final[DatabaseField] = DatabaseField("featuring", [""])
    channels: Final[DatabaseField] = DatabaseField("channels", [""])
    audio_path: Final[DatabaseField] = DatabaseField("audio path", "")
    # image_path: Final[DatabaseField] = DatabaseField("image path", "")

    # TODO: this should be nested in metadata, but is in plain mixed with everything else
    # come up with some way to get nested fields
    listened: Final[DatabaseField] = DatabaseField("listened", 0)
    skiped: Final[DatabaseField] = DatabaseField("skiped", 0)
    likes: Final[DatabaseField] = DatabaseField("likes", 0)
    dislikes: Final[DatabaseField] = DatabaseField("dislikes", 0)


    def get_default_record() -> dict[str, Any]:
        """
        Returns:
            dict[str, Any]: a example of a default record with all its fields set to deep copies of default
        """
        record: dict = {}
        for field in SongFields.fields():
            record[field.name] = deepcopy(field.value)

        return record


    # cannot loop over these
    @classmethod
    @cache
    def fields(cls) -> set[DatabaseField]:
        """
        used to get a iterator over ALL possible (registered) fields
        Returns:
            set[DatabaseField]: a set of database's fields, on which you can iterate on, however you cant change it
        """

        f: set = set()
        for field in fields(SongFields):
            f.add(getattr(SongFields, field.name))

        return f


    def field_valid(field_name: str) -> bool:
        """checks if field is a registered field
        Args:
            field_name (str):
        Returns:
            bool: true if field is a field we have registered, false if it cant be found in field list
        """
        return field_name in SongFields.fields()

@dataclass
class SongRecord:
    """
    represents a record that can be added to the db, data containing the new data
    """
    def __init__(self, init_data: dict = {}):
        # TODO: make it somehow read only for outside code
        self.__data: dict = SongFields.get_default_record()

        # for no initialization data, this wont execute
        for field_name, field_data in init_data.items():
            if field_name in self.__data:
                self.__data[field_name] = field_data
            else:
                print(f"warning, no '{field_name}' in default list")


    def get_data(self):
        return self.__data


    def set_data(self, new_data: dict):
        """used to change data recorded here

        Args:
            new_data (dict): new data to be modified, invalid fieldnames are ignored
        """
        for key, value in new_data.items():
            if SongFields.field_valid(key):
                self.__data[key] = value

