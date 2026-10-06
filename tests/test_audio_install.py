"""
testing only the installation
"""

from pytest import raises
from includes.audio_installer import fetch_url
from includes.db_fields import SongRecord, SongFields
from utils.json_crud import file_exists
from shutil import rmtree

sample_url: str = "https://youtu.be/dQw4w9WgXcQ?si=vUUQ5musEXnYegH4"

output_dir: str = "/tmp/music_utility_tests"
tempfiles_output_dir: str = f"{output_dir}/tmp"

sample_expacted_result: SongRecord = SongRecord({
    SongFields.raw_title.name: "Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster)",
    SongFields.link.name: sample_url
})


def test_fetch_of_metadata():
    res = fetch_url(url=sample_url, download=False)
    for stuff in res:
        print(stuff)

    assert [sample_expacted_result] == res


def test_simple_download():
    output_name = "test_audio"
    output_codec = "mp3"
    expected_output_path = f"{output_dir}/{output_name}.{output_codec}"
    sample_expacted_result.set_data({SongFields.audio_path.name: expected_output_path})

    assert [sample_expacted_result] == fetch_url(
        url=sample_url, download=True, 
        out_dir=output_dir, 
        output_name=output_name,
        temp_out_dir=tempfiles_output_dir,
        codec=output_codec
    )

    assert file_exists(expected_output_path)

    # cleanup after the tests
    rmtree(output_dir)


def test_invalid_url():
    with raises(RuntimeError):
        fetch_url("download uhh cool music")


def test_download_on_slow_wifi():
    # implement slowing of wifi, and check for speed/optimise for cases
    pass


def test_playlist_download():
    # to be implemented in future the feature of downloading a playlist
    pass






