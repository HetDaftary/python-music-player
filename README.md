# PYTHON-MUSIC-PLAYER

* A simple easy to use music player made in python using PyQt5, pygame and mutagen

## Running the project

### Ubuntu or another Debian base distro

* Install pip for python3

```bash
sudo apt install -y python3-pip
```

* Go to the folder of music player and install the requirements of the project

```bash
pip install -r requirements.txt
```

![Installing requirements through pip](data/images/installing-requirements.png)

* Run the project

```bash
python3 src/main.py
```

## App features

* Current look

![alt text](data/images/application.png)

* Select and use play selected to play song of choice or play in normal way using play button.
* Can edit meta data by just editing in the application.
* Currently, I have not added the feature to add/remove any song to the application but it can be simply done by adding or removing mp3 files from "data/mp3-files" folder.

## TODO

| Task | Status |
|------|--------|
| Make feature to open a playlist in new window | currently stalled |
| Make a feature to play any of last 10 songs from history stored in database | done |
| Make a feature to hide or show certain columns | done |
| Make control menu | done |
| Make song position slider | done |
| Make table ui pretty | Not started |
| Make a feature to sort songs based on column | not started |

### Make song position slider

* Implemented backend for the same
* Making ui and slots for this feature

### Make control menu

* Completed the following functionalities:
  * Play selected
  * Next
  * Shuffle
  * Previous
  * Increase volume
  * Decrease volume
  * Repeat
* To make keyboard shortcuts as per requirement

### Make feature to open a playlist in new window

* Made the ui for this
* To clear certain doubts on how to play songs
* To implement draMake a feature to sort songs based on columng and drop feature between windows
* To ensure that if 1 playlist open then other playlists are not opened

### Make a feature to play any of last 10 songs from history stored in database

* To make a table in database which gives last 10 songs played and we can give a play recent feature based on it

### Make a feature to hide or show certain columns

* Make a table which contains info on which columns to hide
* Give a context menu on column headers to show or hide the columns
* Select which columns to show or hide, show columns
* Update these entries in the database to make things consistent and show columns as per the selection

### Make a song position slider

* Make song slider ui
* Implemented a QThread which gets position of the song and duration using pygame and mutagen api

### Make table ui pretty

* To make the ui pretty by getting designs of some good ui applications

### Make a feature to sort songs based on column

* Sort the songs based on title or other column
