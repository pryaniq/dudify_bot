#!/usr/bin/env python3

import telebot
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pylast
from config import *
bot = telebot.TeleBot(token)

def spotify_translator(url):

    scc = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                   client_secret=SPOTIFY_SECRET_KEY)
    sp = spotipy.Spotify(client_credentials_manager=scc)
    lastfm_connetion = pylast.LastFMNetwork(api_key=LAST_API_KEY, api_secret=LAST_API_SECRET)

    if "album" in url:
        result = sp.album(url)
        album = result['name']
        artist = result['artists'][0]['name']
        searching = lastfm_connetion.get_album(artist=artist, title=album)

    elif "artist" in url:
        artist = sp.artist(url)['name']
        print(artist)
        searching = lastfm_connetion.get_artist(artist_name=artist)

    elif "track" in url:
        result = sp.track(url)
        artist = result['artists'][0]['name']
        track = result['name']
        searching = lastfm_connetion.get_track(artist=artist, title=track)

    print(searching.get_url())

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if "https://open.spotify.com" in message.text:
        bot.send_message(message.chat.id, spotify_translator(message.text))


if __name__ == "__main__":
    bot.polling(none_stop=True)

