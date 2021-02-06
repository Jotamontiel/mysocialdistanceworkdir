import os
import sys
import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from json.decoder import JSONDecodeError
from django.conf import settings

os.environ['SPOTIPY_CLIENT_ID'] = settings.SPOTIPY_CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = settings.SPOTIPY_CLIENT_SECRET
os.environ['SPOTIPY_REDIRECT_URI'] = settings.SPOTIPY_REDIRECT_URI

load_username = settings.SPOTIPY_USERNAME
load_scope = settings.SPOTIPY_SCOPE
load_client_id = settings.SPOTIPY_CLIENT_ID
load_client_secret = settings.SPOTIPY_CLIENT_SECRET
load_redirect_uri = settings.SPOTIPY_REDIRECT_URI

def get_spotify_data_user(load_new_username):

    # Get the user token
    util.prompt_for_user_token(load_new_username,load_scope,client_id=load_client_id,client_secret=load_client_secret,redirect_uri=load_redirect_uri)
    
    # Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token(load_new_username)
    except:
        os.remove(f".cache-{load_new_username}")
        token = util.prompt_for_user_token(load_new_username)
    
    # Create our spotifyObject
    spotipyObject = spotipy.Spotify(auth=token)

    # Get from our spotifyObject, the user instance
    user = spotipyObject.current_user()

    # Get from our user instance, the user info
    displayName = user['display_name']
    followers = user['followers']['total']
    email = user['email']
    country = user['country']
    explicit_content = user['explicit_content']
    external_urls = user['external_urls']
    href = user['href']
    id_user = user['id']
    images = user['images']
    product = user['product']
    type_user = user['type']
    uri = user['uri']

    # Display the user info
    print()
    print(">>>> User Info")
    print(">>>> Welcome to Spotipy: " + displayName)
    print(">>>> You have: " + str(followers) + " followers.")
    print(">>>> Your email is: " + email)
    print(">>>> Your country is: " + country)
    print(">>>> Your explicit content is: " + str(explicit_content))
    print(">>>> Your external urls is: " + str(external_urls))
    print(">>>> Your href is: " + href)
    print(">>>> Your id user is: " + id_user)
    print(">>>> Your images are: " + str(images))
    print(">>>> Your product level is: " + product)
    print(">>>> Your type user is: " + type_user)
    print(">>>> Your uri is: " + uri)
    print()

    return user

def get_spotify_data_category(search_query, query_filter):

    ##############################################################
    ########## SPOTIFY API USING USER TOKEN ######################
    ##############################################################
    #util.prompt_for_user_token(load_username,load_scope,client_id=load_client_id,client_secret=load_client_secret,redirect_uri=load_redirect_uri)
    
    # Erase cache and prompt for user permission
    #try:
    #    token = util.prompt_for_user_token(load_username)
    #except:
    #    os.remove(f".cache-{load_username}")
    #    token = util.prompt_for_user_token(load_username)
    
    # Create our spotifyObject
    #spotipyObject = spotipy.Spotify(auth=token)

    ##############################################################
    ########## SPOTIFY API USING USER ############################
    ##############################################################
    auth_manager = SpotifyClientCredentials()

    # Create our spotifyObject
    spotipyObject = spotipy.Spotify(auth_manager=auth_manager)

    # Validate the search_query query for empty field
    if search_query == None or search_query == '':
        return 0, []

    # Validate the query_filter query for compatible field
    valid_query_filters = ['track', 'album', 'playlist', 'artist']
    if query_filter not in valid_query_filters:
        return 0, []

    # Get category search results from the spotipyObject
    if spotipyObject.search(search_query, 1, 0, query_filter):

        if query_filter == 'artist':
            
            # Get the artist object from the search result
            artistSearchResults = spotipyObject.search(search_query, 1, 0, query_filter)
            # print(json.dumps(artistSearchResults, sort_keys=True, indent=4))

            # Generate the artist plural key
            artistkey = query_filter + 's'

            # Get the artist details
            artist = artistSearchResults[artistkey]['items'][0]

            # Get from our artist instance, the artist info
            artistName = artist['name']
            artistFollowers = artist['followers']['total']
            artistExternalUrls = artist['external_urls']
            artistGenres = artist['genres']
            artistId = artist['id']
            artistHref = artist['href']
            artistImages = artist['images']
            artistPopularity = artist['popularity']
            artistType = artist['type']
            artistUri = artist['uri']

            # Display the artist info
            print()
            print(">>>> Artist Info")
            print(">>>> The artist name is: " + artistName)
            print(">>>> The artist have: " + str(artistFollowers) + " followers.")
            print(">>>> The artist external urls are: " + str(artistExternalUrls))
            print(">>>> The artist genres are: " + str(artistGenres))
            print(">>>> The artist id is: " + artistId)
            print(">>>> The artist href is: " + artistHref)
            print(">>>> The artist images are: " + str(artistImages))
            print(">>>> The artist popularity is: " + str(artistPopularity))
            print(">>>> The artist type is: " + artistType)
            print(">>>> The artist uri is: " + artistUri)
            print()

            # Get items and count results for return
            artist_return = artistSearchResults[artistkey].get('items')
            count_return = artistSearchResults[artistkey].get('total', 0)
        
            return count_return, artist_return
        
        elif query_filter == 'track':

            # Get the track object from the search result
            trackSearchResults = spotipyObject.search(search_query, 10, 0, query_filter)
            # print(json.dumps(trackSearchResults, sort_keys=True, indent=4))

            # Generate the track plural key
            trackkey = query_filter + 's'

            # Get the track details
            track = trackSearchResults[trackkey]['items'][0]

            # Get from our track instance, the track info
            trackName = track['name']
            trackArtists = track['artists']
            trackExternalUrls = track['external_urls']
            trackAlbum = track['album']
            trackId = track['id']
            trackHref = track['href']
            trackAvailableMarkets = track['available_markets']
            trackPopularity = track['popularity']
            trackType = track['type']
            trackUri = track['uri']
            trackDiscNumber = track['disc_number']
            trackDurationMS = track['duration_ms']
            trackExplicit = track['explicit']
            trackExternalIds = track['external_ids']
            #trackIsPlayable = track['is_playable']
            #trackLinkedFrom = track['linked_from']
            trackPreviewUrl = track['preview_url']
            trackTrackNumber = track['track_number']

            # Display the track info
            print()
            print(">>>> Track Info")
            print(">>>> The track name is: " + trackName)
            print(">>>> The track artists are: " + str(trackArtists))
            print(">>>> The track external urls are: " + str(trackExternalUrls))
            print(">>>> The track album is: " + str(trackAlbum))
            print(">>>> The track id is: " + trackId)
            print(">>>> The track href is: " + trackHref)
            print(">>>> The track available markets are: " + str(trackAvailableMarkets))
            print(">>>> The track popularity is: " + str(trackPopularity))
            print(">>>> The track type is: " + trackType)
            print(">>>> The track uri is: " + trackUri)
            print(">>>> The track disc number is: " + str(trackDiscNumber))
            print(">>>> The track duration ms is: " + str(trackDurationMS))
            print(">>>> The track explicit is: " + str(trackExplicit))
            print(">>>> The track external ids are: " + str(trackExternalIds))
            #print(">>>> The track is playable state: " + trackIsPlayable)
            #print(">>>> The track linked from: " + str(trackLinkedFrom))
            print(">>>> The track preview url is: " + str(trackPreviewUrl))
            print(">>>> The track number is: " + str(trackTrackNumber))
            print()

            # Get items and count results for return
            track_return = trackSearchResults[trackkey].get('items')
            count_return = trackSearchResults[trackkey].get('total', 0)

            return count_return, track_return

        elif query_filter == 'album':

            # Get the album object from the search result
            albumSearchResults = spotipyObject.search(search_query, 1, 0, query_filter)
            # print(json.dumps(albumSearchResults, sort_keys=True, indent=4))

            # Generate the album plural key
            albumkey = query_filter + 's'

            # Get the album details
            album = albumSearchResults[albumkey]['items'][0]

            # Get from our album instance, the album info
            albumAlbumType = album['album_type']
            albumArtists = album['artists']
            albumAvailableMarkets = album['available_markets']
            #albumCopyrights = album['copyrights']
            #albumExternalIds = album['external_ids']
            albumExternalUrls = album['external_urls']
            #albumGenres = album['genres']
            albumHref = album['href']
            albumId = album['id']
            albumImages = album['images']
            #albumLabel = album['label']
            albumName = album['name']
            #albumPopularity = album['popularity']
            albumReleaseDate = album['release_date']
            albumReleaseDatePrecision = album['release_date_precision']
            #albumTracks = album['tracks']
            albumType = album['type']
            albumUri = album['uri']

            # Display the album info
            print()
            print(">>>> Album Info")
            print(">>>> The album album type is: " + albumAlbumType)
            print(">>>> The album artists are: " + str(albumArtists))
            print(">>>> The album available markets are: " + str(albumAvailableMarkets))
            #print(">>>> The album copyrights are: " + str(albumCopyrights))
            #print(">>>> The album externals ids are: " + str(albumExternalIds))
            print(">>>> The album externals urls are: " + str(albumExternalUrls))
            #print(">>>> The album genres are: " + str(albumGenres))
            print(">>>> The album href is: " + albumHref)
            print(">>>> The album id is: " + albumId)
            print(">>>> The album images are: " + str(albumImages))
            #print(">>>> The album label is: " + albumLabel)
            print(">>>> The album name is: " + albumName)
            #print(">>>> The album popularity is: " + str(albumPopularity))
            print(">>>> The album release date is: " + albumReleaseDate)
            print(">>>> The album release date precision is: " + albumReleaseDatePrecision)
            #print(">>>> The album tracks are: " + str(albumTracks))
            print(">>>> The album type is: " + albumType)
            print(">>>> The album uri is: " + albumUri)
            print()

            # Get items and count results for return
            album_return = albumSearchResults[albumkey].get('items')
            count_return = albumSearchResults[albumkey].get('total', 0)

            return count_return, album_return

        else:

            # Get the playlist object from the search result
            playlistSearchResults = spotipyObject.search(search_query, 1, 0, query_filter)
            # print(json.dumps(playlistSearchResults, sort_keys=True, indent=4))

            # Generate the playlist plural key
            playlistkey = query_filter + 's'

            # Get the playlist details
            playlist = playlistSearchResults[playlistkey]['items'][0]

            # Get items and count results for return
            playlist_return = playlistSearchResults[playlistkey].get('items')
            count_return = playlistSearchResults[playlistkey].get('total', 0)

            return count_return, playlist_return

    else:

        return 0, []