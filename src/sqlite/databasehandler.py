import os
import sqlite3

class DatabaseHandler:
    DATABASE_FILENAME = "data/database/database.db"
    def __init__(self):
        # Make directory of database if it does not exists.
        dirName = os.path.dirname(DatabaseHandler.DATABASE_FILENAME)
        if not os.path.exists(dirName):
            os.makedirs(dirName)

        # Open database 
        self.conn = sqlite3.connect(DatabaseHandler.DATABASE_FILENAME)
        self.cur = self.conn.cursor()

        createTableSyntax = [
            "CREATE TABLE IF NOT EXISTS songDetails (title	TEXT UNIQUE, artist	TEXT, genre	TEXT, album	TEXT, comment	TEXT, year	TEXT, songId	INTEGER, PRIMARY KEY(songId));",
            "CREATE TABLE IF NOT EXISTS songNameToSongId (songName	TEXT,songId	INTEGER,PRIMARY KEY(songName));",
            "CREATE TABLE IF NOT EXISTS playlistIdToSongId (songId	INTEGER,playlistId	INTEGER,PRIMARY KEY(playlistId,songId));",
            "CREATE TABLE IF NOT EXISTS playlistNameToPlaylistId (playlistName	TEXT,playlistId	INTEGER,PRIMARY KEY(playlistName));",
            "CREATE TABLE IF NOT EXISTS songsInHistory (songName TEXT PRIMARY KEY, playedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
            "CREATE TABLE IF NOT EXISTS columnNameToShow (columnName	TEXT, toShow	INTEGER, PRIMARY KEY(columnName));"
        ]

        for i in createTableSyntax:
            self.executeSqlQuery(i)

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def getColumnsToShow(self):
        columnNames = ["title", "artist", "album", "genre", "year", "comment"]
        toShowResult = []
        for column in columnNames:
            query = f"SELECT * from columnNameToShow WHERE columnName=\"{column}\";"
            tempResult = self.executeSqlQuery(query)
            toShowResult.append([column, 1] if len(tempResult) == 0 else tempResult[0])
        return [x[0] for x in toShowResult if x[1] == 1]

    def setColumnName(self, columnName, value):
        if columnName.lower() == "title":
            value = 1
        query = f"INSERT OR REPLACE INTO columnNameToShow(columnName, toShow) VALUES (\"{columnName.lower()}\",{value});"
        self.executeSqlQuery(query)

    def enableColumnName(self, columnName):
        self.setColumnName(columnName, 1)

    def disableColumnName(self, columnName):
        if columnName.lower() == "title":
            self.setColumnName(columnName, 1)
        else:
            self.setColumnName(columnName, 0)

    def getPlaylists(self):
        query = "SELECT playlistName FROM playlistNameToPlaylistId;"
        return [x[0] for x in self.executeSqlQuery(query)]

    def getLastSongs(self, limit = 10):
        query = f"SELECT songName FROM songsInHistory ORDER BY playedAt DESC LIMIT {limit};"
        return [x[0] for x in self.executeSqlQuery(query)]

    def deleteSongFromHistory(self, songName):
        query = f"DELETE FROM songsInHistory WHERE songName=\"{songName}\";"
        self.executeSqlQuery(query)

    def addSongToHistory(self, songName):
        query = f"INSERT INTO songsInHistory (songName) VALUES (\"{songName}\") ON CONFLICT(songName) DO UPDATE SET playedAt = CURRENT_TIMESTAMP;"
        self.executeSqlQuery(query)

    def addPlaylist(self, playlistName):
        self.getPlaylistIdFromName(playlistName)

    def deletePlaylist(self, playlistName):
        playlistName = playlistName.lower()
        playlistId = self.getPlaylistIdFromName(playlistName)
        
        query = f"DELETE FROM playlistNameToPlaylistId WHERE playlistName=\"{playlistName}\";"
        self.executeSqlQuery(query)
        query = f"DELETE FROM playlistIdToSongId WHERE playlistId={playlistId};"
        self.executeSqlQuery(query)

    def getPlaylistIdFromName(self, playlistName):
        playlistName = playlistName.lower()
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

    def getSongNameFromTitle(self, songTitle):
        query = f"SELECT sn.songName FROM songDetails sd JOIN songNameToSongId sn ON sd.songId = sn.songId WHERE sd.title = \"{songTitle}\";"
        toRet = self.executeSqlQuery(query)
        return toRet[0][0] if len(toRet) else ""

    def getSongTitle(self, songName):
        songId = self.getSongIdFromSongName(songName)
        query = f"SELECT title FROM songDetails WHERE songId={songId};"
        return self.executeSqlQuery(query)[0][0]

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

    def getSongsWithTitle(self, playlistName):
        query = ""
        if playlistName.lower() == "library":
            query = "SELECT songName FROM songNameToSongId;"
        else:
            playlistId = self.getPlaylistIdFromName(playlistName)
            query = f"SELECT sns.songName FROM playlistIdToSongId pts INNER JOIN songNameToSongId sns ON pts.songId = sns.songId WHERE pts.playlistId = {playlistId};"
        unsortedSongs = [x[0] for x in self.executeSqlQuery(query)]

        return sorted([[self.getSongTitle(song), song] for song in unsortedSongs], key=lambda x : x[0])

    def getSongs(self, playlistName):
        # Sending songs based on title.
        return [x[1] for x in self.getSongsWithTitle(playlistName)]

    def getSongData(self, songName):
        columnsToShow = [f"sd.{x}" for x in self.getColumnsToShow()]

        query = f"SELECT {', '.join(columnsToShow)} FROM songNameToSongId sns INNER JOIN songDetails sd ON sns.songId = sd.songId WHERE sns.songName=\"{songName}\";"
        return self.executeSqlQuery(query)

    def deleteSongData(self, playlistName, songName):
        playlistName = playlistName.lower()
        playlistId = self.getPlaylistIdFromName(playlistName)
        songId = self.getSongIdFromSongName(songName)
        
        # Delete song from playlist
        query = f"DELETE FROM playlistIdToSongId WHERE playlistId={playlistId} AND songId={songId};"
        self.executeSqlQuery(query)

        if playlistName.lower() == "library":
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

    print(object.getSongNameFromTitle("Happy"))