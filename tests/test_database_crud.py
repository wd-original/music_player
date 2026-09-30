
import src.includes.db_fields as fields
from src.includes.database_object import DatabaseObject as db_obj
import src.utils.json_crud as j_crud
from contextlib import contextmanager

TEST_DB_PATH: str = "/tmp/test_db_music_utility.json"

default_record: dict = fields.SongFields.get_default_record()

# before tests, we need a clear file
j_crud.clear_file(TEST_DB_PATH)

@contextmanager
def state_eq_schema():
    """checks if state of file has not changed
    """
    data_before = j_crud.read_data(TEST_DB_PATH)

    # return control to test function
    yield

    data_after = j_crud.read_data(TEST_DB_PATH)
    j_crud.clear_file(TEST_DB_PATH)

    assert data_before == data_after

def generate_def_dataset(records: int = 10) -> dict:
    dataset: dict = {}
    for i in range(0, records):
        dataset[f"{i}"] = fields.SongRecord().get_data()

    return dataset

# base tests

# test IO on an empty dataset
def test_reading_saving():
    with state_eq_schema():
        db: db_obj = db_obj(TEST_DB_PATH)
        db.save_data(TEST_DB_PATH)


# test IO on a dataset with at least 1 record
def test_reading_saving_with_one_record():
    with state_eq_schema():
        db: db_obj = db_obj(TEST_DB_PATH)
        db.save_data(TEST_DB_PATH)


def test_reading_saving_multiple_records():
    test_set: dict = generate_def_dataset()

    j_crud.write_data(TEST_DB_PATH, test_set)

    with state_eq_schema():
        db: db_obj = db_obj(TEST_DB_PATH)
        db.save_data(TEST_DB_PATH)


# can add to an empty
def test_add_to_empty():
    db: db_obj = db_obj(TEST_DB_PATH)
    # add a default record
    db.add_song()

    db.save_data(TEST_DB_PATH)

    assert {"0": fields.SongRecord().get_data()} == j_crud.read_data(TEST_DB_PATH)
    j_crud.clear_file(TEST_DB_PATH)


# can add to an existing
def test_add_to_existing():
    expected_size = 11
    expected: dict = generate_def_dataset(expected_size)

    j_crud.write_data(TEST_DB_PATH, expected)

    new_record: fields.SongRecord = fields.SongRecord({
        fields.SongFields.authors.name: ["attr"], 
        fields.SongFields.dislikes.name: 5
    })

    expected[f"{expected_size}"] = new_record.get_data()

    db: db_obj = db_obj(TEST_DB_PATH)
    db.add_song(new_record.get_data())
    db.save_data(TEST_DB_PATH)

    # TODO: decide whether to still check saving here, though it is tested earlier
    # check saved data as well, THOUGH we check saving earlier...
    saved_data: dict = j_crud.read_data(TEST_DB_PATH)

    # save a pointer to db's dataset, using a skewd name
    DB_DATA: dict = db._DatabaseObject__dataset

    j_crud.clear_file(TEST_DB_PATH)
    
    # check if size matches
    assert len(DB_DATA.keys()) == len(expected.keys())

    # check index math logic applied
    assert DB_DATA.keys() == expected.keys()

    # check if records match
    assert expected == DB_DATA == saved_data


# can remove 
def test_remove():
    expected: dict = generate_def_dataset()

    j_crud.write_data(TEST_DB_PATH, expected)

    keys_to_erase: list[str] = ["0", "5", "9"]

    for key in keys_to_erase:
        expected.pop(key)

    # test begginning
    db_f: db_obj = db_obj(TEST_DB_PATH)
    db_back: db_obj = db_obj(TEST_DB_PATH)

    for key in keys_to_erase:
        db_f.remove_song(key)

    for i in range(len(keys_to_erase)-1, -1, -1):
        db_back.remove_song(keys_to_erase[i])

    db_f.save_data(TEST_DB_PATH)
    res1: dict = j_crud.read_data(TEST_DB_PATH)

    db_back.save_data(TEST_DB_PATH)
    res2: dict = j_crud.read_data(TEST_DB_PATH)

    j_crud.clear_file(TEST_DB_PATH)

    for key in keys_to_erase:
        assert not db_f.has_song(key)
        assert not db_back.has_song(key)

    assert res1 == res2 == expected


# can remove to empty
def test_remove_to_empty():
    # write a single record
    j_crud.write_data(TEST_DB_PATH, {"0": fields.SongRecord().get_data()})

    db: db_obj = db_obj(TEST_DB_PATH)
    db.remove_song("0")
    db.save_data(TEST_DB_PATH)

    j_crud.clear_file(TEST_DB_PATH)

    assert len(j_crud.read_data(TEST_DB_PATH)) == 0

    assert db.get_size() == 0

    assert not db.has_song("0")


# can edit 1
def test_edit_1():
    expected: dict = {"0": fields.SongRecord().get_data()}    
    j_crud.write_data(TEST_DB_PATH, expected)

    expected["0"][fields.SongFields.likes.name] = 1 

    db: db_obj = db_obj(TEST_DB_PATH)
    db.update_song("0", {fields.SongFields.likes.name: 1})
    db.save_data(TEST_DB_PATH)

    assert j_crud.read_data(TEST_DB_PATH) == expected
    j_crud.clear_file(TEST_DB_PATH)


# can edit many
def test_edit_of_many():
    edited_mark: str = "edited"
    size: int = len(fields.SongFields.fields())
    expected: dict = {}

    for i in range(0, size):
        expected[f"{i}"] = fields.SongRecord().get_data()

    j_crud.write_data(TEST_DB_PATH, expected)

    edited_data: dict = {}
    for field in fields.SongFields.fields():
        edited_data[field.name] = edited_mark

    for i in range(0, size, 2):
        expected[f"{i}"] = edited_data

    db: db_obj = db_obj(TEST_DB_PATH)

    for id in db.get_indexes():
        if int(id) % 2 == 0:
            db.update_song(id, edited_data)

    db.save_data(TEST_DB_PATH)

    result = j_crud.read_data(TEST_DB_PATH)
    
    j_crud.clear_file(TEST_DB_PATH)

    assert expected == result


# add multiple
def test_add_multiple():
    add_count: int = 100
    expected: dict = {}
    for i in range(0, add_count):
        expected[f"{i}"] = fields.SongFields.get_default_record()

    db: db_obj = db_obj(TEST_DB_PATH)

    for i in range(0, add_count):
        db.add_song()

    db.save_data(TEST_DB_PATH)

    result: dict = j_crud.read_data(TEST_DB_PATH)

    assert result == expected
    j_crud.clear_file(TEST_DB_PATH)


# remove multiple
def test_remove_multiple():
    total_count: int = 100
    remove_count: int = 90
    expected: dict = {}
    
    for i in range(0, total_count):
        expected[f"{i}"] = fields.SongFields.get_default_record()

    j_crud.write_data(TEST_DB_PATH, expected)
    
    for i in range(0, remove_count):
        expected.pop(f"{i}")
    
    db: db_obj = db_obj(TEST_DB_PATH)

    for i in range(0, remove_count):
        db.remove_song(f"{i}")

    db.save_data(TEST_DB_PATH)

    result: dict = j_crud.read_data(TEST_DB_PATH)

    assert result == expected
    j_crud.clear_file(TEST_DB_PATH)


# can add 1 remove 2 edit 3 read of 4
def test_all_crud():
    limit: int = 3
    edit_fields = [[fields.SongFields.link, "htttps://"], [fields.SongFields.likes, 33], [fields.SongFields.featuring, ["a", "b"]]]
    
    expected: dict = {}
    
    for i in range(0, 6):
        expected[f"{i}"] = fields.SongFields.get_default_record()

    for i in range(0, 2):
        expected.pop(f"{i}")
    
    for idx, record in expected.items():
        limit -= 1
        record[edit_fields[limit][0]] = edit_fields[limit][1]
        if limit == 0: break
    limit = 3  # reset limit

    j_crud.write_data(TEST_DB_PATH, expected)

    db: db_obj = db_obj(TEST_DB_PATH)
    db.add_song()

    for i in range(0, 2):
        db.remove_song(f"{i}")

    for id in db.get_indexes():
        limit -= 1
        db.update_song(id, {edit_fields[limit][0]: edit_fields[limit][1]})
        if limit == 0: break

    db.save_data(TEST_DB_PATH)

    compare_count: int = 4
    for id in db.get_indexes():
        compare_count -= 1
        print(db.get_song_data(id))
        print(expected[id])
        print()
        assert db.get_song_data(id) == expected[id]
        if compare_count == 0: break

    result = j_crud.read_data(TEST_DB_PATH)

    assert result == expected
    j_crud.clear_file(TEST_DB_PATH)


# add & remove multiple & check indexes
def test_add_remove():
    expected: dict = {}
    for i in range(0, 7):
        expected[f"{i}"] = fields.SongFields.get_default_record()
        if i == 3: j_crud.write_data(TEST_DB_PATH, expected)

    for i in range(0, 3):
        expected.pop(f"{i}")

    db: db_obj = db_obj(TEST_DB_PATH)

    for i in range(3):
        db.add_song()

    for i in range(0, 3):
        db.remove_song(f"{i}")

    db.save_data(TEST_DB_PATH)

    assert db.get_indexes() == list(expected)

    assert j_crud.read_data(TEST_DB_PATH) == expected
    j_crud.clear_file(TEST_DB_PATH)



