import sqlite3

class DatabaseHandler:
    DATABASE_FILENAME = "data/database/database.db"
    def __init__(self):
        self.conn = sqlite3.connect(DatabaseHandler.DATABASE_FILENAME)
        self.cur = self.conn.cursor()

        self.databaseTableCreateSyntax = "CREATE TABLE IF NOT EXISTS songs (title	TEXT, genre	TEXT, artist	TEXT, filename	TEXT, comment	TEXT, album	TEXT, year	TEXT, PRIMARY KEY(filename));"
        DatabaseHandler.executeSqlQuery(self.conn, self.cur, self.databaseTableCreateSyntax)

    def writeSongDataToTable(self, songName, title, artist, album, year, genre, comment):
        query = f"INSERT or REPLACE into songs(filename, title, artist, album, year, genre, comment) VALUES (\"{songName}\",\"{title}\",\"{artist}\",\"{album}\",\"{year}\",\"{genre}\",\"{comment}\");"
        self.executeSqlQuery(self.conn, self.cur, query)

    def getSongData(self, songName):
        query = f"SELECT title, artist, album, year, genre, comment FROM songs WHERE filename=\"{songName}\""
        return self.executeSqlQuery(self.conn, self.cur, query)
    
    def deleteSongData(self, songName):
        query = f"DELETE FROM songs WHERE filename=\"{songName}\";"
        self.executeSqlQuery(self.conn, self.cur, query)

    @staticmethod
    def executeSqlQuery(conn, cur, query):
        """
        Execute a SQL query statement using the provided connection and cursor.

        :param conn: sqlite3.Connection object
        :param cur: sqlite3.Cursor object
        :param sql_query: SQL query string to execute
        :return: Result of the query if it is a SELECT statement, otherwise None
        """
        try:
            cur.execute(query)

            # Commit if it's not a SELECT statement
            if query.strip().upper().startswith("SELECT"):
                return cur.fetchall()
            else:
                conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

if __name__ == "__main__":
    object = DatabaseHandler()
    object.getSongData("data/mp3-files/happy-pharell-williams.mp3")
    object.getSongData("Not exist")