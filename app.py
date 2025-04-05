import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get album cover from Spotify
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        return track["album"]["images"][0]["url"]
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

# Recommendation logic
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    names, posters = [], []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        song_name = music.iloc[i[0]].song
        names.append(song_name)
        posters.append(get_song_album_cover_url(song_name, artist))
        
    return names, posters

# Page layout
st.set_page_config(page_title="Vibe - Music Recommender", layout="wide")

st.markdown("<h1 style='font-size: 3rem; color:#1DB954;'>VibeVerse</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top:-20px;'>Music Recommender System</h3>", unsafe_allow_html=True)

# Load data
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Song selection
music_list = music['song'].values
selected_song = st.selectbox("🎵 Select a song you like", music_list)

# Recommendation button
if st.button('Get Recommendations'):
    names, posters = recommend(selected_song)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], width=150)
            st.markdown(f"{names[i]}")
