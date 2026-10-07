"""
a file where i write string match functions
"""


# some stuff could not of course be written nicely, so here are some patterns to warn users about
# / in video title


from enum import Enum, auto  # aparently enums in python need to be imported
from Levenshtein import distance
from collections.abc import Callable
from includes.db_fields import SongFields


# after 17 characters we warn the user about possible name invalidity
# TODO: still rethink this value, do some ai finu-tuning if needed
MAX_AUTHOR_LENGTH: int = 17

class ErrCodes(Enum):
    NONE = "none"

    SEPARATOR_MISSMATCH = "'-' missmatch"

    WARNING = "warning"

    REFUSED = "too miss-prone, will not attempt"

    # though here in future add some more logic for finding an author from channel name, see #1
    NO_AUTHOR_WARNING = "no author!"

    AUTHOR_NAME_TOO_LONG_WARNING = "too long author name!"

    AUTHOR_NAME_COULD_BE_WRONG_WARNING = "author name could be wrong!"

    TITLE_COULD_BE_WRONG_WARNING = "title could be wrong!"


class MatchStatus(Enum):
    # 1:1 match
    MATCH = auto()
    # 1-3 distance
    CLOSE = auto()
    # 4-5
    FAR_MATCH = auto()
    # a mismatch, strings are different
    MISSMATCH = auto()

# a list of patterns that could devide multiple artists names
combine_paterns: list[str] = [", ", " & ", " x ", " X ", " ❌ ", " and "]

# patterns that mean that names that follow are featuring
featuring_patterns: list[str] = ["ft. ", "ft ", "feat. ", "feat ", "featuring "]

# patterns that mean nothing good/interesting after this place
exclude_patterns: set[str] = {
    "(", "[", "|", "\\", "/", ")", "]", "~"
}

# patterns we avoid even trying to debug, letting user decide the name
refuse_patterns: set[str] = {
    "/"
}

# these rarely are in artists names, usually they mean some missmatch on our behalf
author_warn_patterns: set[str] = {
    '.'
}

# populate this with ', ", and other quotes
title_warn_patterns: set[str] = {
    '‘', '’', '\''
}

# patterns that consistently stay betwen authors and song name, mostly
title_separators = [" - ", " — ", " – "]


class SongTitleData:
    # think this makes them static
    # authors: list[str] = []
    # featuring_artists: list[str] = []
    # song_name: str = ""
    # err_code: str = ErrCodes.NONE

    # TODO: song_name is a str?
    def __init__(self, authors: list[str], feats: list[str], song_name, err_code=ErrCodes.NONE):
        self.authors = authors
        self.featuring_artists = feats
        self.song_name = song_name
        self.err_code = err_code

    def __eq__(self, other: object):
        if not isinstance(other, SongTitleData):
            return NotImplemented

        err_code_status = False if (self.err_code == ErrCodes.NONE) else (self.err_code == other.err_code)

        fields_eq = (self.authors == other.authors and 
                    self.featuring_artists == other.featuring_artists and 
                    self.song_name == other.song_name)
        
        return fields_eq or err_code_status

    def strip_spaces(self):
        self.authors = [auth.strip() for auth in self.authors]

        self.featuring_artists = [feat.strip() for feat in self.featuring_artists]

        self.song_name = self.song_name.strip()


    def has_err_code(self) -> bool:
        """checks if it has some kind of errcode

        required because the default might change + i don't like exposing class logic, i like to encapsulate logic

        Returns:
            bool: returns True if it has received an error code
        """
        return self.err_code != ErrCodes.NONE


    def get_data(self) -> dict:
        """returns all data as a dictionary that can be used in db work

        Returns:
            dict: all fields with according SOngFields names and acording values of this instance
        """
        return {
            SongFields.song_name.name: self.song_name,
            SongFields.featuring.name: self.featuring_artists,
            SongFields.authors.name: self.authors
        }


    def validate_fields(self):
        if len(self.authors) == 0:
            self.err_code = ErrCodes.NO_AUTHOR_WARNING

        else:
            for author_name in self.authors:
                if len(author_name) > MAX_AUTHOR_LENGTH:
                    self.err_code = ErrCodes.AUTHOR_NAME_TOO_LONG_WARNING
                    break

                for pattern in author_warn_patterns:
                    if pattern in author_name:
                        self.err_code = ErrCodes.AUTHOR_NAME_COULD_BE_WRONG_WARNING
                        break
    
    def print_data(self):
        print(f"author: {self.authors}")
        print(f"featuring: {self.featuring_artists}")
        print(f"name: '{self.song_name}'")
        print(f"err code: '{self.err_code}'")


def get_frequency(s: str) -> dict[str, int]:
    """gets the frequency of each character in s

    ?optimise using:
    ```
    from collections import Counter
    return Counter(s)
    ```

    Args:
        s (str)

    Returns:
        dict[str, int]: char and times it appeared
    """
    fr: dict[str, int] = {}
    
    for c in s:
        fr[c] = fr.get(c, 0) + 1

    return fr


def anagram(s1: str, s2: str) -> bool:
    """checks if s2 is anagram of s1

    Returns:
        bool: s1 is anagram of s2 or s2 is anagram of s1
    """
    return get_frequency(s1) == get_frequency(s2)


def str_match(str1: str, str2: str) -> MatchStatus:
    """checks (using Levenshteins distance algorithm) if str1 matches str2

    Args:
        str1 (str): jus a string
        str2 (str): jus a string

    Returns:
        int: the higher the number the less they match
    """

    # get levenshtein distance
    dist: int = distance(str1.lower(), str2.lower())

    # direct match
    if dist == 0:
        return MatchStatus.MATCH

    # here a check for anagrams is needed
    elif 0 < dist <= 5:
        if anagram(str1, str2):
            return MatchStatus.MISSMATCH

        # [1, 3]
        elif dist <=3:
            return MatchStatus.CLOSE

        # [4, 5]
        else:
            return MatchStatus.FAR_MATCH

    # everything else is a missmatch
    return MatchStatus.MISSMATCH


def get_artists_list(names_raw: str, song_data: SongTitleData) -> list[str]:
    """gets a list like "a, b & c x d and returns an array of names (without spaces, or commas)

    Args:
        names (str): a raw youtube string of names
        song_data (SongTitleData): song title data so far, is being ignored or set to refused

    Returns:
        list[str]: a list of names like [a, b, c, d]
    """
    # search for combine patterns, if found get the substr for the name

    names: list[str] = []

    i: int = 0
    name_start: int = 0

    while i < len(names_raw):
        if names_raw[i] in refuse_patterns:
            song_data.err_code = ErrCodes.REFUSED
            break

        if names_raw[i] in exclude_patterns:
            break

        for pattern in combine_paterns:
            pattern_splice = names_raw[i : i + len(pattern)]
            if pattern_splice == pattern:
                names.append(names_raw[name_start : i])
                # set i to end of patern 
                i += len(pattern)
                name_start = i
                break
        i += 1

    if name_start < len(names_raw):
        names.append(names_raw[name_start : i])

    return names

# @deprecated?
def check_refuse_patterns(data: SongTitleData, raw_str: str) -> bool:
    for pattern in refuse_patterns:
        if pattern in raw_str:
            data.err_code = ErrCodes.REFUSED
            return True

    return False

# TODO: we return magic numbers, make a struct here
def collect_feats(target: str, song_data: SongTitleData, found_action: Callable[[int, int, str, SongTitleData], None], 
                aditional_checks: Callable[[int], bool]=lambda x: x==x) -> int:
    """collects featurings

    Args:
        target (str): checks for patterns here
        found_action (Callable[[int, int, str]]): what it does on a found feat. ft. etc, use with get_artists_lists, second argument is match length
        aditional_checks (_type_, optional): aditional checks for feats, takes the found index of ft. Defaults to lambda x:x==x.

    Returns:
        int: the start of featuring pattern found, 
        or -1 if pattern is not found, 
        -2 if the structure contains patterns we refuse
    """

    # initial check if song was refused
    if song_data.err_code == ErrCodes.REFUSED:
        return -2

    for pattern in featuring_patterns:
        i = target.find(pattern)
        if i != -1 and aditional_checks(i):
            found_action(i, len(pattern), target, song_data)

            # check if this was refused
            if song_data.err_code == ErrCodes.REFUSED:
                return -2
            
            # quit after finding feats
            # return feat pattern start
            return i

    return -1


def process_title(title: str) -> SongTitleData:
    """processes the title and returns data from title or a errcode

    Args:
        title (str): title, not processed or modified, as on youtube

    Returns:
        SongTitleData: a bundle of songs colected data
    """

    data: SongTitleData = SongTitleData([], [], "")
    
    # TODO: title parts into a struct with 2 vars?

    title_parts: list[str] = ""

    current_separator_try: int = 0

    while len(title_parts) != 2 and current_separator_try < len(title_separators):
        title_parts = title.split(title_separators[current_separator_try])
        current_separator_try += 1

    if len(title_parts) != 2:
        data.err_code = ErrCodes.SEPARATOR_MISSMATCH
        return data

    for pattern in exclude_patterns:
        if pattern in title_parts[0]:
            data.err_code = ErrCodes.AUTHOR_NAME_COULD_BE_WRONG_WARNING

    def add_feats(idx: int, len: int, raw_s: str, song_data: SongTitleData):
        data.featuring_artists = get_artists_list(raw_s[idx+len:], song_data)

    def add_both(idx: int, len: int, raw_s: str, song_data: SongTitleData):
        data.authors = get_artists_list(raw_s[:idx], song_data)
        add_feats(idx, len, raw_s, song_data)
    
    if collect_feats(title_parts[0], data, add_both) == -2:
        return data

    # in collect_feats we search for feats, if no feats found authors is empty
    if len(data.featuring_artists) == 0:
        data.authors = get_artists_list(title_parts[0], data)


    # processing song name

    feat_start: int = -1

    for pattern in title_warn_patterns:
        if pattern in title_parts[1]:
            data.err_code = ErrCodes.TITLE_COULD_BE_WRONG_WARNING

    # if no featuring artists found until now, means they could be in the title
    if len(data.featuring_artists) == 0:
        # TODO: think of something smarter than "(f"
        # check for feats in brackets
        opening_i: int = title_parts[1].find("(f")
        closing_i: int = title_parts[1].find(")")

        if -1 < opening_i < closing_i:
            feat_start = opening_i + collect_feats(title_parts[1][opening_i:closing_i], data, add_feats, lambda i: i < closing_i)

        # check for normal feats
        else:
            feat_start = collect_feats(title_parts[1], data, add_feats)

    # aggresively strip
    # strip until feat, if found (!-1)
    if feat_start > -1:
        title_parts[1] = title_parts[1][:feat_start]
    # we refused to get feats because of some invalidity
    elif feat_start == -2:
        return data

    # check for hard excluding patterns
    for i in range(0, len(title_parts[1])):
        if title_parts[1][i] in exclude_patterns:
            data.song_name = title_parts[1][:i]
            break

    if len(data.song_name) == 0:
        data.song_name = title_parts[1]

    data.strip_spaces()

    data.validate_fields()

    return data

