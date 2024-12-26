# Naam: Joachim Tramper.

# Bestand naam: EindopdrachtOpgave1.py

# Opdracht 1, Toetsen, Gebruik van SQLite.

# Functie: Programma dat een database raadpleegd en een album top 10 als output heeft. 

# Python versie: 3.9.13

# IDLE: Wing 101 9 

# Bestand laatst geweizigd: 09.02.2024.

# Sample database: https://www.sqlitetutorial.net/sqlite-sample-database/

import sqlite3                                                                  #Sqlite3 importeren voor gebruik databases. 

def create_connection(db_file):
    
    """ Functie om connectie te realiseren met exception. """
    
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return None

database = 'D:\\Programs\Python\DBSQLite\chinook.db'                            #Database locatie. 

conn = create_connection(database)                                              #Connectie maken via functie.

cur = conn.cursor()                                                             #Cursor genereren. 

def top_tien_albums():
    
    """ Functie die database raadpleegt en tien meest verkochte albums als output geeft."""
    
    cur.execute(""" SELECT artists.Name, albums.AlbumId, albums.Title, COUNT(albums.AlbumId) AS TotaalAlbsVerkocht FROM albums
    INNER JOIN artists ON albums.ArtistId = artists.ArtistId 
    INNER JOIN tracks ON albums.AlbumId = tracks.AlbumId
    INNER JOIN invoice_items ON tracks.TrackId = invoice_items.TrackId
    GROUP BY albums.AlbumId
    ORDER BY TotaalAlbsVerkocht desc
    limit 10; """)                                                              #Query waar via primary keys (ArtistId, AlbumId en TrackId tabellen worden  
                                                                                #gelinkt en vervolgens de top 10 best verkochte albums worden geselecteerd.
    results = cur.fetchall()                                                    #Resultaat binnen halen van database.                                                  
         
    for x, result in enumerate(results):                                        #Enumerate build-in gebruiken om rijnummers te genereren. 
        print(x + 1, str(result[0]), str(result[2]), str(result[3]), sep='\t')  #Print de benodigdheden in de juiste vorm, rijnummer start is 1.  

top_tien_albums()                                                               #Functie uitvoeren. 
