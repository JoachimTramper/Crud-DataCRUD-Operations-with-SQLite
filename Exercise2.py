# Naam: Joachim Tramper

# Bestand naam: EindopdrachtOpgave2.py

# Opdracht 2, Toetsen, Gebruik van SQLite

# Functie: Programma dat een database raadpleegd en eventueel bewerkt met text bestand als invoer

# Python versie: 3.9.13

# IDLE: Wing 101 9 

# Bestand laatst geweizigd: 09.02.2024

# Sample database: https://www.sqlitetutorial.net/sqlite-sample-database/

import sqlite3                                                          #Importeren benodigde modules
import sys

def create_connection(db_file): 
    
    """Functie om connectie te realiseren met exception."""
    
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return None

database = 'D:\\Programs\\Python\\DBSQLite\\chinook.db'                    #Database locatie

conn = create_connection(database)                                      #Connectie maken via functie

cur = conn.cursor()                                                     #Cursor genereren

bestand = input('Geef de naam van het te importeren bestand: ')         #Gebruiker om bestandnaam vragen

def open_bestand():
    
    """Functie om text bestand te checken met exceptions."""
    
    try:
        file = open(bestand, 'rt')
    except FileNotFoundError:                                           #FileNotFoundError met bericht en exit
        print('Bestand niet gevonden.')
        sys.exit()
    except OSError:                                                     #OSError met bericht en exit
        print('Kan bestand niet openen.')
        sys.exit()
    except Exception:                                                   #Algemene exception om overige exceptions af te vangen en exit
        print('Er is iets verkeerd gegaan.')
        sys.exit()
    file.close()                                                        #Bestand sluiten

def check_playlist_exist():
    
    """Functie die checked of ingevoerde playlist al bestaat in de database."""
    
    plnaam = input('Geef de naam van de playlist: ')                    #Vraag gebruiker om naam van de playlist
    cur.execute("""SELECT Name FROM playlists WHERE Name = ?""", (plnaam,)) #Database raadplegen om naam te selecteren mocht deze gelijk zijn aan invoer
    plnaam_check = cur.fetchall()                                       #Resultaat binnenhalen van database 
    if plnaam_check == []:                                              #Als plnaam_check een lege lijst is betekent dit dat er geen playlist in de database bestaat met dezelfde naam
        cur.execute("""INSERT INTO playlists (Name) VALUES (?)""", (plnaam,))   #Naam van ingevoerde playlist in database invoeren
        conn.commit()                                                   #Veranderingen in database gelijk realiseren
        print('--- Start import van playlist ---')                      #Alles is ingevoerd en goedgekeurd, het importeren van de tracks mag beginnen
    else:
        print('Deze playlist bestaat al.')                              #Als plnaam_check niet gelijk is aan een lege list komt de naam al voor in de database, bericht en exit
        sys.exit()

def split_playlist(file1):
    
    """ Functie die ingevoerd text bestand omzet in een list, zonder lege items"""
    
    with open(file1, 'rt') as f:                                        #Bestand openen zonder exceptions, dit is eerder al gedaan
        regel = f.read().split('\n')                                    #Text bestand regels splitten
        bewerkt_bestand = list(filter(None, regel))                     #Lege list items verwijderen
        return bewerkt_bestand                                          #Output functie, list zonder lege items

def check_tracks():
    
    """ Functie die list items afzonderlijk vergelijkt met de database en deze toevoegd, 
        een foutmelding geeft wanneer niet gevonden of een keuzemenu geeft wanneer de invoer 
        overeen komt met een deel van verschillende tracks in de database. Waar 
        vervolgens een keuze uit gemaakt moet worden en vervolgens wordt toevoegd."""
    
    tracklist = split_playlist(bestand)                                 #Tracklist genereren via split_playlist functie 
    cur.execute(""" SELECT PlaylistId FROM playlists """)               #PlaylistID van playlist tabel selecteren
    playlist_id = cur.lastrowid                                         #Playlist ID verkrijgen via ingevoerde playlist, eerst volgend nummer in de linker kolom van de tabel 
    for track in tracklist:                                             #'For' loop om regel voor regel te vergelijken
        cur.execute(""" SELECT tracks.TrackId, tracks.Name, artists.Name
                FROM tracks INNER JOIN albums ON tracks.AlbumId = albums.AlbumId       
                INNER JOIN artists ON albums.ArtistId = artists.ArtistId      
                WHERE tracks.name LIKE(?||'%%')""", (track,))           #Database raadplegen voor (gedeeltelijke) overeenkomende tracks
        results = cur.fetchall()                                        #Resultaat binnenhalen van database
        if len(results) == 1:                                           #Als lengte 1 is, is de juiste track gevonden
            track_id = results[0][0]                                    #Gewenst track_id is het eerste onderdeel van de eerste tuple in list                         
            cur.execute("""INSERT INTO playlist_track (PlaylistId, TrackId) VALUES (?, ?)""", (playlist_id, track_id))  #Track ID invoeren met playlist ID
            conn.commit()                                               #Veranderingen in database gelijk realiseren                                 
        if len(results) == 0:                                           #Als lengte list gelijk is aan 0, zijn er geen tracks gevonden
            print('--- Geen tracks gevonden voor',(track),'---')        #Bericht naar gebruiker met invoer
        if len(results) > 1:                                            #Als lengte groter dan 1 is zijn er meerdere opties voor de gebruiker om uit te kiezen
            print('Maak een keuze uit de volgende tracks')
            for x, result in enumerate(results):                        #Enumerate build-in gebruiken om rijnummers te genereren
                print(x + 1, str(result[1]), str(result[2]), sep='\t')  #Print de benodigdheden in de juiste vorm voor de gebruiker, rijnummer start is 1 
            while True:                                                 #While loop starten, zodat gebruiker juiste invoer geeft
                try:
                    keuze = int(input('Uw keuze: '))                    #Try except block starten om exceptions af te vangen
                    if  keuze < 1:                                      #Negatieven en 0 invoer afvangen
                        raise ValueError('Invoer moet een integer binnen het keuzemenu zijn.')  
                    track_keuze = results[keuze-1]
                except (ValueError, IndexError):                        #ValueError en IndexError afvangen
                    print('Invoer moet een integer binnen het keuzemenu zijn.')                                  
                except Exception:
                    print('Er is iets verkeerd gegaan.')                #Overige exceptions afvangen
                else:                                                   #Else keyword om loop te verlaten
                    break
            track_id = track_keuze[0]                                   #Track ID is het eerste onderdeel van de track keuze list 
            cur.execute("""INSERT INTO playlist_track (PlaylistId, TrackId) VALUES (?, ?)""", (playlist_id, track_id))  #Track toevoegen aan playlist
            conn.commit()                                               #Veranderingen in database gelijk realiseren
            
    conn.close()                                                        #Connectie met database afsluiten
    print('--- Import van playlist gereed ---')                         #Importeren is gereed       
    
def main():   
    
    """ Main functie met de uit te voeren functies voor overzicht.""" 
    
    open_bestand()
    check_playlist_exist()
    check_tracks()  

if __name__ == '__main__':                                              #Main functie uitvoeren
    main()

