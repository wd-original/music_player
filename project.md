### tis gonna be a file about project goals architecture n stuff

basically i need to define exactly what i want to build have (a music player is too abstract), and then decide **how** to implement those functionalities

- ## functionalities expected:
    - a json db: (though in this case we kinda rebuild the bicycle from scratch, good for a learning project though)
        - a file with each song's index, its metadata, and its path on disk
        - a file with playlists, index, metadata, song's indexes

    - a string matching assembly of functions (so different links but same songs do not match) (Levenshtein)

    - automated tests

    - a gui to control the app (no more CLI commands)
        - ofc with skip/pause/prev/next
        - organizing playlists n shi
        - installing/modifying/listening/deleting music

    - a music installer, paste the link (song audio youtube) and get the audio only
        - also a way to play stuff that's not installed by the app (eg. user installed them other way, but they are on the machine)

    - a player to display audio (on another thread)

    - (optional) in future maybe add (like in background updater) a tagging system with songs having tags

    - in future add a like disslikes skipped skipped over system

- ### a lil more complex/new ones
    - (as i said 2 threads)
    - (as i said automaded tests)

    - playlists import, handle a import playlist to playlist logic (handle intersection of songs, adding a song from an import to this playlist, now it is in both, move from imported, now its only in this one, delete from import, changes the original and all instances as well, and ordering from an imported playlist, mix this one's songs with imported ones, a button to group them by import, by custom order, alphabetically (changing in O(1)), handle logic like, import of an import of an import of ... properly)

    - multi device, run on both pc and mobile
        - synching music, installing music, deleting music, basically diffing 2 devices (reliably)

    - a installer, and update syncer 

    - some basic music editing options

- ## architectural thoughts
    - build a custom json managing db (there should be libraries for that, but repetition is mother of learning)

    - build a custom string matching assembly of functions for song name matchin
        - will consist of multiple steps, like stripping slowed/sped up/remix and other words like these
        - will run the already made by someone smart Levenshtein distance algorithm

    - delegate the GUI to AI, let it design implement, i just do backend, and expose simple interfaces to the AI

    - music installer is just 10 lines, my job will be to build the stuff around it

    - a music launcher bg daemon, that runs in bg on another thread and makes sound, when pause, out of app (and no media playing from the app) just make it make no sound (and consume 0 CPU and 0 RAM) let it stay inactive for some time, and if it passes a threshold like 1-2 hours, turn it off; its launch should be instantanious

    - i think of playing with 2 byte indexes (of according songs in json) in 2 ds array (for order preserving) which allow empty indexes (that will just be skipped) and sets for O(1) look-up, though this is questionable (i think python [especially if we're gonna optimize compile or some stuff like that] is still fast, even a look-up in a 2000 song playlist will be instantanious)

    - work with goddam indexes, no more paths as keys, ambiguity, combination, just indexes bottom to top

    - CPU efficiency: a thing to keep in mind is speed (though python here is the wrong choice obviously, rust is better+it handles threads easier, but i dont want to learn a whole new language (now)) i'm talking about instantanious open of app, instantaneous playlist shuffle/playback begin, instantanious music skip (no pauses between songs, everything is quick) that's why we need shorts to be quickly loaded in copy arrays, and in general, we work with pointers no/little copy of data (though python handles it well, apparently everything is a pointer to a object on the heap)

- ## problem with name collecting
    - we cant tell just from youtube title the name of the song authors etc. (different formats) so we need to go with:
        - fast check for something like a very common format
        - when the app does not know this format, we flag and let the user decide the song name and authors
        - also allow switching from slow (user decides metadata for every song) medium (we run the algorithm, on unknown match flag) fast (just use the youtube title, fast insert if the author name featuring artists song name and other stuff does not matter)
