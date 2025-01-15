# Script that queries a database and outputs a top 10 albums list.

# Sample database: https://www.sqlitetutorial.net/sqlite-sample-database/

import sqlite3                                                                  #Importing Sqlite3 for database usage
                                              
def create_connection(db_file):
    
    """ Function to establish a connection with exception handling """
    
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return None

database = 'D:\\Programs\\Python\\DBSQLite\\chinook.db'                         #Replace this with the path to your downloaded database

conn = create_connection(database)                                              #Establishing a connection via function

cur = conn.cursor()                                                             #Generate cursor

def top_ten_albums():
    
    """ Function that queries the database and outputs the ten best-selling albums"""
    
    cur.execute(""" SELECT artists.Name, albums.AlbumId, albums.Title, COUNT(albums.AlbumId) AS TotalAlbumsSold FROM albums
    INNER JOIN artists ON albums.ArtistId = artists.ArtistId 
    INNER JOIN tracks ON albums.AlbumId = tracks.AlbumId
    INNER JOIN invoice_items ON tracks.TrackId = invoice_items.TrackId
    GROUP BY albums.AlbumId
    ORDER BY TotalAlbumsSold desc
    limit 10; """)                                                              #Query where primary keys (ArtistId, AlbumId, and TrackId tables) are linked, and the top 10 best-selling albums are selected 
                                                                                
    results = cur.fetchall()                                                    #Fetch result from database                                                 
         
    print(f"{'Rank':<5} {'Artist':<25} {'Album':<35} {'Total Sold':<10}")       #Print header
    print("-" * 80)
     
    for i, result in enumerate(results):                                        #Print rows with adjusted column width
        artist = result[0]
        album = result[2]
        total_sold = result[3]
             
        if len(artist) > 25:                                                    #Limit artist and album titles to fixed widths, add ellipsis if truncated
            artist = artist[:22] + "..."
        if len(album) > 35:
            album = album[:32] + "..."
        
        print(f"{i + 1:<5} {artist:<25} {album:<35} {total_sold:<10}")

top_ten_albums()                                                                #Excecute function
