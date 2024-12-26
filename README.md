# CRUD Operations with SQLite

**Description Exercise 1**:  
This Python script connects to a SQLite database (using the `chinook.db` sample database) and retrieves the top 10 best-selling albums. The program uses SQL queries to join multiple tables (albums, artists, tracks, and invoice_items) to calculate the total sales of each album and display the 10 albums with the highest sales. The script outputs the album title, artist name, and total sales in a user-friendly format.

**Description Exercise 2**:  
This Python program connects to a SQLite database (using the `chinook.db` sample database) and imports a playlist of tracks from a user-provided text file. The program checks if the playlist already exists in the database and, if not, adds it. It then processes the tracks in the text file, comparing them to existing tracks in the database and adding them to the specified playlist. If there are multiple matches for a track, the user is prompted to choose the correct one.

**Features**:
- Connects to a SQLite database and queries data.
- Validates whether a playlist already exists before importing.
- Processes a text file containing track names, validates them against the database, and adds matching tracks to the playlist.
- Handles exceptions such as file not found, database connection errors, and input errors.

**Technologies**:
- Python 3.9.13.
- SQLite.
- Visual Studio Code (the final versions were initially written using Wing 101 9 IDE).

**Usage**:
- The user provides a text file with track names and the name of the playlist to import.
- The program will check if the playlist already exists in the database; if not, it will create a new playlist.
- Tracks in the text file are matched against the database, and valid matches are added to the playlist.

**Last Modified**: 09.02.2024  
**Sample Database**: [SQLite Sample Database](https://www.sqlitetutorial.net/sqlite-sample-database/)