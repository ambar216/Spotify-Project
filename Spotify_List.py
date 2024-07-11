import ID_Information as ID_Information
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


#Get credentials 
from ID_Information import Spotify_Client_ID, Spotify_Client_Secret, Spotify_Redirect_URI, Playlist_ID

#Authenticate that the user has access to the Spotify playlist
sp = spotipy.Spotify(auth_manager=SpotifyOAuth
                (Spotify_Client_ID,
                 Spotify_Client_Secret,
                 Spotify_Redirect_URI,
                 #Define that the user is allowed to read private playlists
                 scope="playlist-read-private"))


Song_List = []
#Store information about the playlist/songs
Spotify_playlist= sp.playlist_tracks(Playlist_ID)

#Loop through the dictionary of items in the Spotify API 
for x in Spotify_playlist['items']:
    Track = x['track']
    Sound_track = Track['name']
    #Creating a new list in order to associate each artist with their song
    Artist = [Artists['name'] for Artists in Track['artists']]
    #Concatenate into one string
    Artist_Name = ', '.join(Artist)
    Album_Name = Track['album']['name']
    Song_List.append((Sound_track, Artist_Name, Album_Name))


#Loop through and print the songs within the playlist
v = 0
while v < len(Song_List):
    v = v +1
FINAL_LIST = " "

#Numbering each item in a playlist
for Number, (Sound_track, Artist_Name, Album_Name) in enumerate(Song_List, start=1):
    FINAL_LIST += (f"{Number}.) SONG NAME: {Sound_track.title()}\n BY: {Artist_Name.title()}\n ALBUM: {Album_Name.title()}\n\n")

print(FINAL_LIST)


#Exporting formatted list into a txt document

while True:
    question = input("Would you like to export this list into a text document? (yes/no): ").strip().lower()

    if question == "yes":
        print("Exporting the list...")
        file_path = "song_list1.txt"
        with open(file_path, 'w') as file:
                file.write(FINAL_LIST)
        print(f"List exported successfully to '{file_path}'")
        break

    elif question == "no":
        print("Goodbye!")
        break
    else:
        print("Please enter a valid input.")

