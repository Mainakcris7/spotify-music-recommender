import streamlit as st
import joblib
import numpy as np

album_img_urls = joblib.load('./saved_objects/image_urls.pkl')
song_dict1 = joblib.load('./saved_objects/song_dict1.pkl')
song_dict2 = joblib.load('./saved_objects/song_dict2.pkl')
similarities = joblib.load('./saved_objects/song_similarities.pkl')

st.image("https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_Green.png", width=200)

st.title("Spotify Music Recommender 🎧")
all_songs = [song.title() for song in list(song_dict1.keys())]

selected_song = st.selectbox("Select a song", all_songs)
index_of_selected_song = song_dict1[selected_song.lower()]
url_selected_song = album_img_urls[index_of_selected_song]

st.markdown(f"### :blue[{selected_song}]")
st.image(url_selected_song, width=300)


@st.cache_data
def recommend(song):
    songs = []
    urls = []
    song = song.lower()
    song_ind = song_dict1[song]
    # Last one is the song itself, so, dont take it
    top_5_matches = np.argsort(similarities[song_ind])[-6:-1]
    for i in top_5_matches:
        songs.append(song_dict2[i])
        urls.append(album_img_urls[i])
    return songs, urls


if st.button("Recommend"):
    with st.spinner(text="Loading..."):
        songs, urls = recommend(selected_song.lower())
    st.markdown("### Recommended songs")
    cols = st.columns(5)
    for col, song, url in zip(cols, songs, urls):
        with col:
            st.image(url)
            st.write(song.title())
