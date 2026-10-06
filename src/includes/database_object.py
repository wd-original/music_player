"""

"""


import utils.json_crud as j_crud

from includes.db_fields import SongRecord, SongFields

from functools import cache

# TODO: path is hardcoded, as said in #5, make it in .env or in some other dynamic format
DB_PATH = "/home/wd/projects/my-utils/music_utility/db/data_test.json"


class DatabaseObject:
    """
    manages the database CRUD, the endpoint that serves as a querry

    every function calls has_song, so no need to check that beforehand, only if there is some separate logic to it
    """
    # stores the database
    __dataset: dict

    # stores the index of the new to add song
    # it does not go down, only up, and cannot be changed
    __global_index: int

    def __init__(self, data_path: str = DB_PATH):
        self.read_data(data_path)


    def read_data(self, data_path: str = DB_PATH):
        """initiates the internal data varibles

        Args:
            data_path (str, optional): path of the data file. Defaults to DB_PATH.
        """
        self.__dataset = j_crud.read_data(data_path)

        # index after last index is the size
        self.__global_index = self.get_size()


    def save_data(self, data_file_path: str = DB_PATH):
        """saves database data into data_file

        raises an error if it cant save

        Args:
            data_file_path (str, optional): file where to save state. Defaults to DB_PATH.
        """
        j_crud.write_data(data_file_path, self.__dataset)


    def add_song(self, song_data: dict = {}):
        """add a song to dataset

        Args:
            song_data (dict): default empty, data to add record to dataset, if empty add with default
        """

        self.__dataset[f"{self.__global_index}"] = SongRecord(song_data).get_data()

        self.__global_index += 1


    def has_song(self, song_id: str) -> bool:
        """checks if song id is in database

        Args:
            song_id (str): 

        Returns:
            bool: true song is in dataset, false no such song_id registered
        """
        return song_id in self.__dataset


    def remove_song(self, song_id: str):
        """safely deletes a song by id

        if song is not in dataset does nothing

        Args:
            song_id (str): jus an id bruh
        """
        if self.has_song(song_id):
            self.__dataset.pop(song_id, None)
            self.__global_index -= 1


    def update_song(self, song_id: str, new_data: dict):
        """calls update_action on according song_id

        Args:
            song_id (str): song id
            new_data (dict): old data is merged with the new data
        """
        if self.has_song(song_id):
            for field_name, field_data in new_data.items():
                if SongFields.field_valid(field_name):
                    self.__dataset[song_id][field_name] = field_data
                else: 
                    print(f"WARNING, db has no field {field_name}")


    def get_song_data(self, song_id: str) -> dict:
        """returns the song's data, or empty
        """
        if self.has_song(song_id):
            return self.__dataset[song_id]

        return {}


    def get_size(self):
        return len(self.__dataset)


    @cache
    def get_indexes(self) -> list:
        """
        used to iterate over the database
        Returns:
            list: a list of all indexes, as strings
        """
        return list(self.__dataset)

    # def update_fields_data(self, field_name: str, field_new_data, lambda_func=None):
    #     pass

    # def add_fields(self, fields_values: dict):
    #     pass

