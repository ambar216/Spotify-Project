import os #handling file pathing
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from Unformated_List import file_path
from ID_Information import authentication



def read_songs_file (file_path):
    with open(file_path, 'r') as file: #Opening the file in 'r'ead mode
        songs = file.readlines() #Reading all lines into a list
    return songs

def usable_list(songs):
    final_song_list = []
    for song in songs:
        stripped_songs = song.strip() #strip white space
        final_song_list.append(stripped_songs) #appending the stripped songs to the list
    return final_song_list

songs = read_songs_file(file_path) #reading songs from the file
final_song_list = usable_list(songs) #list of songs with no white space 
print(final_song_list)


#Using YoutubeAPI in order to search for a specific song request based on the top result 
#AKA searching for songs on Youtube
def song_request(youtube, query):
    request = youtube.search().list(
        part='snippet',
        type='video',
        maxResults=1, #First result ONLY
        q=query
    ).execute()

    #Extracting the video_ID from the FIRST search result
    video_ID = request['items'][0]['id']['videoId']
    return video_ID




#Creating a playlist on Youtube
def create_playlist(youtube, title):
    request = youtube.playlists().insert(
        part='snippet,status', #which parts of the playlist resources should be included ('snippet' = metadata 'status' = privacy status)
        body={
            'snippet': {
                "title":title #Setting the title of the playlist
            },
            "status":{
                "privacyStatus": "unlisted" #Setting privacy status to unlisted
            }
        }
    )
    response = request.execute()
    return response['id']





#Using the API to add videos(songs) to the playlist
def add_video_to_playlist(youtube, playlist_id, video_id):
    request = youtube.playlistItems().insert(
        part="snippet",  
        body={
            "snippet": {
                "playlistId": playlist_id,  # Specify the playlist ID where the video will be added
                "resourceId": {
                    "kind": "youtube#video",  # Specifing that the type of resource... that being a video
                    "videoId": video_id  # Specify the ID of the video to be added to the playlist
                }
            }
        }
    )
    response = request.execute()
    return response 


#putting everything together
if __name__ == "__main__":
    songs = read_songs_file(file_path) 
    youtube = authentication() #authenticating with yt API

song_ids = [] #List used to store youtube videoIDs
for song in songs:
        video_id = song_request(youtube, song) #requesting the id for each songs

        if video_id is None:
            print(f"I could not find {song}")
        else:
            song_ids.append(video_id)


# Create a new playlist
playlist_id = create_playlist(youtube, "My Playlist")

# Add each video to the playlist
for video_id in song_ids:
    added_successfully= add_video_to_playlist(youtube, playlist_id, video_id)
    if not added_successfully:
        print(f"Sorry, this video {video_id} couldn't be added to the playlist")

print(f"Playlist Link!: https://www.youtube.com/playlist?list={playlist_id}")







