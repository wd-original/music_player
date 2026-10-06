"""
temp file with how the future download of a song protocol will look
"""

from includes.audio_installer import fetch_url, DownloadReturnMetadata
from includes.database_object import DatabaseObject
from utils.str_match import process_title, SongTitleData, str_match, MatchStatus
from includes.db_fields import SongFields


# a small test example on how this should look in future
def sample_install():
    sample_url = "https://youtu.be/dQw4w9WgXcQ?si=vUUQ5musEXnYegH4"
    # get the db by the default path
    db = DatabaseObject()

    # 1. fetch url data
    data = fetch_url(url=sample_url)

    # 2. get title
    for record in data:
        title_data = process_title(record.title)

        if title_data.has_err_code():
            print(f"got err code: '{title_data.err_code}'")
            continue

        # 3. check if in db or if any errcodes
        for idx in db.get_indexes():
            match_status = str_match(title_data.song_name, db.get_song_data(idx)[SongFields.song_name])

            match match_status:
                case MatchStatus.MATCH:
                    print(f"song '{title_data.song_name}' already in library")
                    break
                case MatchStatus.CLOSE:
                    print(f"song '{title_data.song_name}' might be in db")
                case MatchStatus.FAR_MATCH:
                    print(f"song '{title_data.song_name}' should not be in db")
                case MatchStatus.MISSMATCH:
                    pass
                case _:
                    print("Error dev added a new match status but forgot to record it sample_install.py")

    # 4. get audio (add check if audio file exists already)
    data = fetch_url(url=sample_url, download=True)

    # 5. add to db with all data (author title url path)
    for song in data:
        db.add_song(song.get_as_dict())

    db.save_data()

    # make tests for dis

sample_install()

