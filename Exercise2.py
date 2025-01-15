# Program that queries and optionally edits a database using a text file as input

# Sample database: https://www.sqlitetutorial.net/sqlite-sample-database/

import sqlite3                                                          #Import required modules
import sys

def create_connection(db_file): 
    
    """Function to establish a connection with exception handling"""
    
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return None

database = 'D:\\Programs\\Python\\DBSQLite\\chinook.db'                 #Replace this with the path to your downloaded database

conn = create_connection(database)                                      #Establishing connection via function

cur = conn.cursor()                                                     #Generate cursor

file_name = input('Enter the name of the file to import: ')                  #Prompt the user for the file name

def open_file():
    
    """Function to check the text file with exception handling"""
    
    try:
        file = open(file_name, 'rt')
    except FileNotFoundError:                                           #FileNotFoundError with a message and exit
        print('File not found')
        sys.exit()
    except OSError:                                                     #OSError with a message and exit
        print('Cannot open file')
        sys.exit()
    except Exception:                                                   #General exception to catch other exceptions and exit
        print('Something went wrong')
        sys.exit()
    file.close()                                                        #Close file

def check_playlist_exist():
    
    """Function that checks if the entered playlist already exists in the database"""
    
    plname = input('Enter the name of the playlist: ')                  #Prompt the user for the name of the playlist
    cur.execute("""SELECT Name FROM playlists WHERE Name = ?""", (plname,)) #Query the database to select the name if it matches the input
    plname_check = cur.fetchall()                                       #Fetch the result from the database
    if plname_check == []:                                              #If plname_check is an empty list, it means that no playlist exists in the database with the same name
        cur.execute("""INSERT INTO playlists (Name) VALUES (?)""", (plname,))   #Insert the name of the entered playlist into the database
        conn.commit()                                                   #Apply changes to the database immediately
        print('--- Starting the import of the playlist... ---')         #Everything has been entered and approved, the import of the tracks may begin
    else:
        print('This playlist already exists')                           #If plname_check is not equal to an empty list, the name already exists in the database, display a message and exit
        sys.exit()

def split_playlist(file1):
    
    """Function that converts the entered text file into a list, excluding empty items"""
    
    with open(file1, 'rt') as f:                                        #Open the file without exceptions, as this has already been handled earlier
        line = f.read().split('\n')                                     #Split the lines of the text file
        updated_file = list(filter(None, line))                         #Remove empty list items
        return updated_file                                             #Output function, list without empty items

def check_tracks():
    
    """Function that compares list items individually with the database and adds them, 
        gives an error message when not found, or displays a menu when the input matches 
        a partial name of multiple tracks in the database. The user must then choose from 
        the options, and the selected track is added"""
    
    tracklist = split_playlist(file_name)                                    #Generate the tracklist using the split_playlist function
    cur.execute(""" SELECT PlaylistId FROM playlists """)               #Select the PlaylistID from the playlist table
    playlist_id = cur.lastrowid                                         #Obtain the Playlist ID for the entered playlist, as the next sequential number in the leftmost column of the table
    for track in tracklist:                                             #For loop to compare line by line
        cur.execute(""" SELECT tracks.TrackId, tracks.Name, artists.Name
                FROM tracks INNER JOIN albums ON tracks.AlbumId = albums.AlbumId       
                INNER JOIN artists ON albums.ArtistId = artists.ArtistId      
                WHERE tracks.name LIKE(?||'%%')""", (track,))           #Query the database for (partial) matching tracks
        results = cur.fetchall()                                        #Fetch the result from the database
        if len(results) == 1:                                           #If the length is 1, the correct track has been found
            track_id = results[0][0]                                    #The desired track_id is the first element of the first tuple in the list                         
            cur.execute("""INSERT INTO playlist_track (PlaylistId, TrackId) VALUES (?, ?)""", (playlist_id, track_id))  #Insert the Track ID with the Playlist ID
            conn.commit()                                               #Apply changes to the database                                  
        if len(results) == 0:                                           #If the length of the list is 0, no tracks were found
            print('--- No tracks found for',(track),'---')              #Message to the user with input
        if len(results) > 1:                                            #If the length is greater than 1, there are multiple options for the user to choose from
            print('Make a selection from the following tracks')
            print(f"{'Choice':<5} {'Track Name':<45} {'Artist':<25}")   #Aligned header
            print("-" * 75)                                             #Line below the header for clarity
            for x, result in enumerate(results):
                print(f"{x + 1:<5} {result[1]:<45} {result[2]:<25}")    #Ensure each row is properly aligned

            while True:                                                 #While loop to ensure the user provides the correct input
                try:
                    choice = int(input('Your choice: '))                #Start try-except block to catch exceptions
                    if  choice < 1:                                     #Handle negative and zero input
                        raise ValueError('The input must be an integer within the selection menu')  
                    track_choice = results[choice-1]
                except (ValueError, IndexError):                        #Catch ValueError and IndexError
                    print('The input must be an integer within the selection menu')                                  
                except Exception:
                    print('Something went wrong')                       #Catch other exceptions
                else:                                                   #Else keyword to exit the loop
                    break
            track_id = track_choice[0]                                  #The Track ID is the first element of the track choice list
            cur.execute("""INSERT INTO playlist_track (PlaylistId, TrackId) VALUES (?, ?)""", (playlist_id, track_id))  #Add the track to the playlist
            conn.commit()                                               #Apply changes to the database 
            
    conn.close()                                                        #Close the connection to the database
    print('--- Import of playlist complete ---')                        #Import is complete     
    
def main():   
    
    """Main function with the functions to be executed""" 
    
    open_file()
    check_playlist_exist()
    check_tracks()  

if __name__ == '__main__':                                              #Execute main function
    main()

