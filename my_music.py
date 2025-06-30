import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from constants import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


st.set_page_config(page_title="My Music", page_icon=":musical_note:", layout="wide")
st.write("My Music Dashboard")


def get_top_artists_and_tracks(sp):
    top_artists = sp.current_user_top_artists(limit=10, time_range='medium_term')
    top_tracks = sp.current_user_top_tracks(limit=10, time_range='medium_term')
    
    artists_data = {
        'Artist': [artist['name'] for artist in top_artists['items']],
        'Followers': [artist['followers']['total'] for artist in top_artists['items']],
        'Popularity': [artist['popularity'] for artist in top_artists['items']]
    }
    
    tracks_data = {
        'Track': [track['name'] for track in top_tracks['items']],
        'Artist': [', '.join([artist['name'] for artist in track['artists']]) for track in top_tracks['items']],
        'Popularity': [track['popularity'] for track in top_tracks['items']]
    }
    
    print("Top Artists Data:", artists_data)
    print("Top Tracks Data:", tracks_data)
    return pd.DataFrame(artists_data), pd.DataFrame(tracks_data)

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Top Artists", "Top Tracks"])

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope="user-top-read"))

    if page == "Top Artists":
        st.subheader("Your Top Artists")
        artists_df, _ = get_top_artists_and_tracks(sp)
        st.dataframe(artists_df)

        fig, ax = plt.subplots()
        ax.barh(artists_df['Artist'], artists_df['Popularity'], color='skyblue')
        ax.set_xlabel('Popularity')
        ax.set_title('Top Artists by Popularity')
        st.pyplot(fig)

    elif page == "Top Tracks":
        st.subheader("Your Top Tracks")
        _, tracks_df = get_top_artists_and_tracks(sp)
        st.dataframe(tracks_df)

        fig, ax = plt.subplots()
        ax.barh(tracks_df['Track'], tracks_df['Popularity'], color='lightgreen')
        ax.set_xlabel('Popularity')
        ax.set_title('Top Tracks by Popularity')
        st.pyplot(fig)
if __name__ == "__main__":
    main()














