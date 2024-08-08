import sqlite3

class DatabaseHandler:
    DATABASE_FILENAME = "data/database/database.db"
    def __init__(self):
        self.conn = sqlite3.connect(DatabaseHandler.DATABASE_FILENAME)
        self.cur = self.conn.cursor()

        createTableSyntax = [
            "CREATE TABLE IF NOT EXISTS songDetails (title	TEXT, artist	TEXT, genre	TEXT, album	TEXT, comment	TEXT, year	TEXT, songId	INTEGER, PRIMARY KEY(songId));",
            "CREATE TABLE IF NOT EXISTS songNameToSongId (songName	TEXT,songId	INTEGER,PRIMARY KEY(songName));",
            "CREATE TABLE IF NOT EXISTS playlistIdToSongId (songId	INTEGER,playlistId	INTEGER,PRIMARY KEY(playlistId,songId));",
            "CREATE TABLE IF NOT EXISTS playlistNameToPlaylistId (playlistName	TEXT,playlistId	INTEGER,PRIMARY KEY(playlistName));",
            "CREATE TABLE IF NOT EXISTS songsInHistory (songName TEXT PRIMARY KEY, playedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
            "CREATE TABLE IF NOT EXISTS columnNameToShow (columnName	TEXT, toShow	INTEGER, PRIMARY KEY(columnName));"
        ]

        for i in createTableSyntax:
            self.executeSqlQuery(i)

    def getPlaylists(self):
        query = "SELECT playlistName FROM playlistNameToPlaylistId"
        return [x[0] for x in self.executeSqlQuery(query)]

    def getLastSongs(self, limit = 10):
        query = f"SELECT songName FROM songsInHistory ORDER BY playedAt DESC LIMIT {limit};"
        return [x[0] for x in self.executeSqlQuery(query)]

    def addSongToHistory(self, songName):
        query = f"INSERT INTO songsInHistory (songName) VALUES (\"{songName}\") ON CONFLICT(songName) DO UPDATE SET playedAt = CURRENT_TIMESTAMP;"
        self.executeSqlQuery(query)

    def addPlaylist(self, playlistName):
        self.getPlaylistIdFromName(playlistName)

    def deletePlaylist(self, playlistName):
        playlistId = self.getPlaylistIdFromName(playlistName)
        
        query = f"DELETE FROM playlistNameToPlaylistId WHERE playlistName=\"{playlistName}\";"
        self.executeSqlQuery(query)
        query = f"DELETE FROM playlistIdToSongId WHERE playlistId={playlistId};"
        self.executeSqlQuery(query)

    def getPlaylistIdFromName(self, playlistName):
        query = f"SELECT playlistId from playlistNameToPlaylistId WHERE playlistName=\"{playlistName}\";"
        playlistIdList = self.executeSqlQuery(query)

        if playlistIdList != None and len(playlistIdList) != 0:
            return playlistIdList[0][0]
        else:
            query=f"SELECT COUNT(playlistId) FROM playlistNameToPlaylistId;"
            playlistIdList = self.executeSqlQuery(query)

            query=f"INSERT INTO playlistNameToPlaylistId(playlistName, playlistId) VALUES (\"{playlistName}\", {playlistIdList[0][0]})"
            self.executeSqlQuery(query)
            return playlistIdList[0][0]

    def getSongIdFromSongName(self, songName):
        query=f"SELECT songId from songNameToSongId WHERE songName=\"{songName}\";"
        songIdList = self.executeSqlQuery(query)

        if songIdList != None and len(songIdList) != 0:
            return songIdList[0][0]
        else:
            query=f"SELECT COUNT(songId) FROM songNameToSongId;"
            songIdList = self.executeSqlQuery(query)

            query=f"INSERT INTO songNameToSongId(songName, songId) VALUES (\"{songName}\", {songIdList[0][0]})"
            self.executeSqlQuery(query)
            return songIdList[0][0]

    def addToPlaylist(self, playlistName, songName):
        playlistId = self.getPlaylistIdFromName(playlistName)
        songId = self.getSongIdFromSongName(songName)

        query = f"INSERT or REPLACE into playlistIdToSongId(playlistId, songId) VALUES ({playlistId}, {songId});"
        self.executeSqlQuery(query)

    def writeSongDataToTable(self, playlistName, songName, title, artist, album, year, genre, comment):
        songId = self.getSongIdFromSongName(songName)
        playlistId = self.getPlaylistIdFromName(playlistName)
        query = f"INSERT or REPLACE into songDetails(songId, title, artist, album, year, genre, comment) VALUES ({songId},\"{title}\",\"{artist}\",\"{album}\",\"{year}\",\"{genre}\",\"{comment}\");"
        self.executeSqlQuery(query)

        query = f"INSERT or REPLACE into playlistIdToSongId(playlistId, songId) VALUES ({playlistId}, {songId});"
        self.executeSqlQuery(query)

    def getSongs(self, playlistName):
        query = ""
        if playlistName.lower() == "library":
            query = "SELECT songName FROM songNameToSongId;"
        else:
            playlistId = self.getPlaylistIdFromName(playlistName)
            query = f"SELECT sns.songName FROM playlistIdToSongId pts INNER JOIN songNameToSongId sns ON pts.songId = sns.songId WHERE pts.playlistId = {playlistId};"
        return [x[0] for x in self.executeSqlQuery(query)]    
        
    def getSongData(self, songName):
        query = f"SELECT sd.title, sd.artist, sd.album, sd.year, sd.genre, sd.comment FROM songNameToSongId sns INNER JOIN songDetails sd ON sns.songId = sd.songId WHERE sns.songName=\"{songName}\";"
        return self.executeSqlQuery(query)

    def deleteSongData(self, playlistName, songName):
        playlistName = playlistName.lower()
        playlistId = self.getPlaylistIdFromName(playlistName)
        songId = self.getSongIdFromSongName(songName)
        
        # Delete song from playlist
        query = f"DELETE FROM playlistIdToSongId WHERE playlistId={playlistId} AND songId={songId};"
        self.executeSqlQuery(query)

        if playlistName == "library":
            query = f"DELETE FROM songDetails WHERE songId={songId};"
            self.executeSqlQuery(query)
            query = f"DELETE FROM songNameToSongId WHERE songName=\"{songName}\";"
            self.executeSqlQuery(query)
            query = f"DELETE FROM playlistIdToSongId WHERE songId={songId};"
            self.executeSqlQuery(query)

    def executeSqlQuery(self, query):
        """
        Execute a SQL query statement using the provided connection and cursor.

        :param conn: sqlite3.Connection object
        :param cur: sqlite3.Cursor object
        :param sql_query: SQL query string to execute
        :return: Result of the query if it is a SELECT statement, otherwise None
        """
        try:
            self.cur.execute(query)

            # Commit if it's not a SELECT statement
            if query.strip().upper().startswith("SELECT"):
                return self.cur.fetchall()
            else:
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

if __name__ == "__main__":
    import os
    import time

    object = DatabaseHandler()
    object.writeSongDataToTable("library", "song1", "title1", "artist1", "album1", "year1", "genre1", "comment1")
    object.writeSongDataToTable("library", "song2", "title2", "artist2", "album2", "year2", "genre2", "comment2")
    object.writeSongDataToTable("playlist-1", "song1", "title1", "artist1", "album1", "year1", "genre1", "comment1")
    object.writeSongDataToTable("playlist-1", "song2", "title2", "artist2", "album2", "year2", "genre2", "comment2")
    object.writeSongDataToTable("playlist-2", "song1", "title1", "artist1", "album1", "year1", "genre1", "comment1")
    object.writeSongDataToTable("playlist-2", "song2", "title2", "artist2", "album2", "year2", "genre2", "comment2")
    print(object.getSongData("song1"))
    print(object.getSongData("song2"))

    os.system("date")

    for song in os.listdir("data/mp3-files"):
        object.addSongToHistory(songName=os.path.join("data/mp3-files", song))

    print("added songs 1")
    time.sleep(10)

    os.system("date")

    for song in os.listdir("data/mp3-files"):
        object.addSongToHistory(songName=os.path.join("data/mp3-files", song))

    print("added songs 2")

    print(len(object.getLastSongs()))

