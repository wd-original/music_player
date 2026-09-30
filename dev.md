

# done
- ### a string matching function assembly
- [X] add a basic string matching using levenshtein's algorithm
- [X] add checking for full titles
    - [X] strip useless stuff
    - [X] parse format defined stuff, return status for a unrecognized format
    - [X] check for author, song names return according status
- [X] in future: make exclude patterns a set, the rest need a loop for control over length


- # [ ] document dis shi

# first phase
- ## features to be implemented:
    - ### schafolding of the project done, architecture, file structure
    - ### tests schafolding, a decent test pipeline and test architecture/logic 

    - ### a string matching function assembly

    - ### a db object/the whole db logic implemented

# second phase
- ## music installer
    - just a youtube link -> .mp3 file somewhere + metadata in db, jus a song

- ## music player 
    - just 1 song playing on another thread
    - though could be expanded to a small `playing_list` object


# open issues (use github for that, though these are small)
- ## string matching
- [ ] #2 not really an issue, but make `collect_feats` in `str_match.py` return a struct not magic numbers
- [ ] #3 make a webcrawler+claude and expand your testing dataset to 10k songs
- [ ] !!!#4 in future: refactor the title->data functions in `str_match.py` to be more proffesional, reusable, efficient, and return more specific error codes
    - [ ] in future: think of a better way to check for featurings in ()
    - [ ] add more return err_codes in `SongTitleData`

- ## db object
- [ ] #7 add overloads with ints to db apis


- [ ] #5 make a env parcer and put paths and shi in env vars

