import logging

from repositories.new_track.spotify import SpotifyNewTrackRepository
from repositories.new_track.csv import CsvNewTrackRepository
from repositories.new_track.google_spreadsheet import GssNewTrackRepository
import utils.helper as helper

logger_pro = logging.getLogger('production')
logger_dev = logging.getLogger('develop')
logger_con = logging.getLogger('console')

class NewTrackService(object):
    """
    A class used to represent a spotify service.

    Attributes
    ----------
    spotify:
        A spotify new track repository.
    csv:
        A csv new track repository.
    gss:
        A google spreadsheet new track repository.

    Methods
    ------
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """
        # self.spotify = SpotifyNewTrackRepository()
        # self.csv = CsvNewTrackRepository()
        # self.gss = GssNewTrackRepository()

    @classmethod
    def extract_track_data(cls, track_json_data: dict) -> dict:
        """ Extract only tracks data from tracks json data.

        Parameters
        ----------
        tracks_json_data: dict
            A tracks json data.

        Raises
        ------
        Exception
            If it fail to extract track data.

        Return
        ------
        track: dict
            A track dict with certain keys
        """
        logger_pro.info({
            'action': 'Extract only tracks data from tracks json data.',
            'status': 'Run',
            'message': ''
        })
        try:
            track = {
                'name': track_json_data['name'],
                'artist': track_json_data['artists'][0]['name'],
                'playlist_name': None,
                'track_url': track_json_data['external_urls']['spotify'],
                'playlist_url': None,
                'release_date': None,
                'added_at': None,
                'created_at': helper.get_date(),
                'like': False
            }
            logger_pro.info({
                'action': 'Extract only tracks data from tracks json data.',
                'status': 'Success',
                'message': '',
                'data': {
                    'track': track
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Extract only tracks data from tracks json data.',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'track_json_data': track_json_data
                }
            })
        return track

    @classmethod
    def retrieve_tracks_data(cls,
                             tracks_json_data: dict,
                             playlist_name: str = None,
                             playlist_url: str = None) -> list:
        """ Retrieve only tracks data from tracks json data.

        Parameters
        ----------
        tracks_json_data: dict
            A tracks json data.
        playlist_name: str, optional
            A playlist name (default is None).
        playlist_url: str
            A playlist url (default is None).

        Raises
        ------
        Exception
            If it fail to append track data.

        Return
        ------
        tracks: list
            A track data with certain columns
        """
        
        tracks = []
    
        # Retrieve certain data from json data            
        names = [t["track"]["name"] for t in tracks_json_data]
        urls = [t["track"]["external_urls"]["spotify"] for t in tracks_json_data]
        artists = [t["track"]["artists"][0]['name'] for t in tracks_json_data]
        release_date = [t["track"]["album"]["release_date"] for t in tracks_json_data]
        added_at = [t["added_at"]for t in tracks_json_data]
        playlist_name = playlist_name
        playlist_url = playlist_url
        
        logger_pro.info({
            'action': 'Retrieve tracks data for columns from playlist',
            'status': 'Run',
            'message': '',
            'args': {
                # 'tracks_json_data': tracks_json_data,
                # 'playlist_json_data': playlist_json_data,
                'names': {
                    'length': len(names),
                    'items': names
                },
                'urls': {
                    'length': len(urls),
                    'items': urls
                },
                'artists': {
                    'length': len(artists),
                    'items': artists
                },
                'release_date': {
                    'length': len(release_date),
                    'items': release_date
                },
                'added_at': {
                    'length': len(added_at),
                    'items': added_at
                },
                'playlist_name': {
                    'items': playlist_name
                },
                'playlist_url': {
                    'items': playlist_url
                }
            }
        })

        for i, v in enumerate(names):
            try:
                track = {
                    'name': names[i],
                    'artist': artists[i],
                    'playlist_name': playlist_name,
                    'track_url': urls[i],
                    'playlist_url': playlist_url,
                    'release_date': release_date[i],
                    'added_at': added_at[i],
                    'created_at': helper.get_date(),
                    'like': False
                }
                tracks.append(track)
                logger_pro.info({
                    'action': 'Retrieve tracks data for columns from playlist',
                    'status': 'Success',
                    'message': '',
                    'data': {
                        'track': track
                    }
                })
            except Exception as e:
                logger_pro.warning({
                    'action': 'Retrieve tracks data for columns from playlist',
                    'status': 'Fail',
                    'message': '',
                    'exception': e,
                    'data': {
                        'i': i,
                        'v': v
                    }
                })
        return tracks

    # TODO: move some functions to repository
    @classmethod
    def show_track_names(cls, tracks) -> None:
        names = [track['name'] for track in tracks]
        print("\n")
        for name in names:
            print(f'\t[TRACK NAME] - {name}')
        return

    @classmethod
    def is_in_track(cls, track: dict, tracks: list) -> bool:
        track = {'name': track['name'], 'artist': track['artist']}
        tracks = [{'name': t['name'], 'artist': t['artist']} for t in tracks]
        if track in tracks:
            return True
        else:
            return False

    def add_new_tracks(self) -> None:
        """ Add new tracks to csv, gss, spotify playlist
        
        Parameters
        ----------
        None

        Raises
        ------
        None

        Return
        ------
        None
        """
        # Fetch tracks from playlists
        spotify_repo = SpotifyNewTrackRepository()
        tracks_spotify = spotify_repo.fetch_tracks_from_playlists()
        print(len(tracks_spotify))
        return

    def fetch_tracks_from_playlist(self, playlist_id: str) -> list:
        """ Fetch tracks from certain playlist.
        
        Parameters
        ----------
        playlist_id: str
            A playlist ID to fetch tracks from.

        Raises
        ------
        TypeError
            The playlist id you provided is not correct.
        Exception


        Return
        ------
        tracks: list
            A tracks data list gotten from the playlist.
        """
        tracks = []
        logger_pro.info({
            'action': f'Retrieve tracks from {playlist_id}',
            'status': 'Run',
            'message': '',
            'args': {
                'playlist_id': playlist_id
            }
        })
        try:
            playlist_json_data = self.repository.fetch_playlist_json_data(playlist_id)
            tracks_number = playlist_json_data['tracks']['total']
            playlist_name = playlist_json_data["name"]
            playlist_url = playlist_json_data['external_urls']['spotify']
            max_number = 100
            logger_con.info(f'Retrieve tracks data from playlist: {playlist_name}: {tracks_number}')

            while max_number < tracks_number:
                offset = len(tracks)
                tracks_json_data = self.repository.fetch_playlist_items_json_data(playlist_id, offset=offset)
                tracks_json_data = tracks_json_data["items"]
                tracks += SpotifyService.retrieve_tracks_data(tracks_json_data,
                                                              playlist_name = playlist_name,
                                                              playlist_url = playlist_url)
                tracks_number -= len(tracks_json_data)
            else:
                # after while loop
                offset = len(tracks)
                tracks_json_data = self.repository.fetch_playlist_items_json_data(playlist_id, offset=offset)
                tracks_json_data = tracks_json_data["items"]
                tracks += SpotifyService.retrieve_tracks_data(tracks_json_data,
                                                              playlist_name = playlist_name,
                                                              playlist_url = playlist_url)
            
            logger_pro.info({
                'action': f'Retrieve tracks from {playlist_id}',
                'status': 'Success',
                'message': '',
                'data': tracks
            })
        except TypeError as e:
            logger_pro.error({
                'action': f'Retrieve tracks from {playlist_id}',
                'status': 'Fail',
                'message': 'The playlist id you provided is not correct',
                'exception': e,
                'data': {
                    'playlist_id': playlist_id
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': f'Retrieve tracks from {playlist_id}',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'playlist_id': playlist_id
                }
            })

        return tracks

    def fetch_tracks_from_playlists(self, playlist_ids: list) -> list:
        """ Fetch tracks from playlists set up on setting file.
        If there are duplicate tracks amound the playlist ids,
        it will be removed.
        
        Parameters
        ----------
        playlist_ids: str
            playlist IDs to fetch tracks from.

        Raises
        ------
        TypeError
            The playlist id you provided is not correct.
        Exception

        Return
        ------
        all_tracks: list
            A tracks data list gotten from the playlist.
        """
        all_tracks = []
        logger_pro.info({
            'action': 'Fetch tracks from playlists set up on setting file',
            'status': 'Run',
            'message': '',
            'args': {
                'playlist_ids': playlist_ids
            }
        })

        try:
            for playlist_id in playlist_ids:
                tracks = self.fetch_tracks_from_playlist(playlist_id)
                all_tracks += self.distinct_tracks_by(tracks, all_tracks)
                logger_pro.info({
                    'action': 'Fetch tracks from playlists set up on setting file',
                    'status': 'Run',
                    'message': '',
                    'args': {
                        'playlist_ids': playlist_id,
                        'all_tracks': all_tracks
                    }
                })
        except TypeError as e:
            logger_pro.error({
                'action': 'Fetch tracks from playlists set up on setting file',
                'status': 'Fail',
                'message': 'The playlist ids you provided is not correct',
                'exception': e,
                'data': {
                    'playlist_id': playlist_id
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Fetch tracks from playlists set up on setting file',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'playlist_id': playlist_id
                }
            })

        return all_tracks

    def distinct_tracks_by(self, tracks: list, by_tracks: list) -> list:
        """ Remove duplicate tracks by 'by_tracks'

        Parameters
        ----------
        tracks: list
            A tracks list to be compared
        by_tracks: list
            A tracks list to be compared tracks with

        Raises
        ------
        TypeError
            If tracks and/or by_tracks are not list.
        Exception
            If it fails to distinc track by by_tracks.

        Return
        ------
        distincted_tracks: list
            A tracks list removed duplicate tracks
        """
        distincted_tracks = []
        logger_pro.info({
            'action': 'Remove duplicate tracks by by_tracks',
            'status': 'Run',
            'message': '',
            'args': {
                'tracks': tracks,
                'tracks_from_csv': by_tracks
            }
        })

        # If there is no track data, it regards all tracks as new tracks
        if not by_tracks:
            logger_con.info(f'The number of new tracks is {len(tracks)}')
            logger_pro.info({
                'action': 'Remove duplicate tracks by by_tracks',
                'status': 'Success',
                'message': '',
                'data': {
                    'tracks': tracks
                }
            })
            return tracks

        # Prepare a list from csv to check which tracks are new for this time
        converted_tracks = self.convert_tracks_into_name_and_artist(tracks)
        
        # Prepare a list from retrieved tracks to check which tracks are new for this time
        converted_by_tracks = self.convert_tracks_into_name_and_artist(by_tracks)

        try:        
            # Check which tracks are new
            for i, track in enumerate(converted_tracks):
                if track in converted_by_tracks:
                    continue
                distincted_tracks.append(tracks[i])

            logger_con.info(f'The number of new tracks is {len(distincted_tracks)}')
            logger_pro.info({
                'action': 'Remove duplicate tracks by by_tracks',
                'status': 'Success',
                'message': '',
                'data': {
                    'tracks': distincted_tracks
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Remove duplicate tracks by by_tracks',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'length': len(tracks),
                    'tracks': tracks
                }
            })
        return distincted_tracks

    def convert_tracks_into_name_and_artist(self, tracks: list) -> list:
        """ Convert tracks into name and artist

        Parameters
        ----------
        tracks: list
            A tracks list to be converted into a list 
            containing dict which key sare name and artist

        Raises
        ------
        Exception
            If it fails to convert them

        Return
        ------
        converted_tracks: list
            A tracks list converted into a list 
            containing dict which keys are name and artist
        """
        logger_pro.info({
            'action': 'Convert tracks into name and artist',
            'status': 'Run',
            'message': '',
            'args': {
                'length': len(tracks),
                'tracks': tracks
            }
        })
        try:
            converted_tracks = [{'name': t['name'], 'artist': t['artist']} for t in tracks]
            logger_pro.info({
                'action': 'Convert tracks into name and artist',
                'status': 'Success',
                'message': '',
                'data': {
                    'length': len(converted_tracks),
                    'converted_tracks': converted_tracks
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Retrieve tracks from playlists',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'length': len(tracks),
                    'tracks': tracks
                }
            })
        return converted_tracks

    def add_tracks_to_playlist(self, tracks: list, playlist_id: str) -> None:
        """ Add tracks to a playlist.

        Parameters
        ----------
        tracks: list
            A tracks list to add
        playlist_id: str
            A playlist id to add to 
        
        Raises
        ------
        Exception
            If you can not add tracks to the playlist

        Return
        ------
        None
        """
        if not tracks:
            message = 'There is no new tracks to add to playlist on Spotify this time.'
            logger_con.info(message)
            logger_pro.info(message)
            return

        tracks_number = len(tracks)
        max_number = 100
        logger_pro.info({
            'action': 'Add tracks between certain indexs',
            'status': 'Run',
            'message': '',
            'args': {
                'tracks_number': tracks_number
            }
        })
        while max_number < tracks_number:
            
            extracted_tracks, tracks = tracks[0:int(max_number)], tracks[int(max_number)::]
            track_urls = [t['track_url'] for t in extracted_tracks]

            logger_pro.info({
                'action': 'Add tracks between certain indexs',
                'status': 'Success',
                'message': '',
                'args': {
                    'extracted_tracks': len(extracted_tracks),
                    'remaining_track': len(tracks),
                    'track_urls': len(track_urls)
                }
            })

            self.repository.add_tracks_to_playlist(track_urls)
            tracks_number = len(tracks)
        else:
            track_urls = [t['track_url'] for t in tracks]
            logger_pro.info({
                'action': 'Add tracks between certain indexs',
                'status': 'Success',
                'message': '',
                'args': {
                    'tracks': len(tracks),
                    'track_urls': len(track_urls)
                }
            })
            self.repository.add_tracks_to_playlist(track_urls)
        return

    def fetch_current_track(self) -> list:
        """ Fetch a track data you are listening.

        if there is no track you are listening,
        return empty list.

        Parameters
        ----------
        None
        
        Raises
        ------
        Exception
            If you can not fetch current track.

        Return
        ------
        track: list
            A track you are listening.
        """
        track_json_data = self.repository.fetch_current_track_json_data()
        
        if track_json_data:
            track_json_data = track_json_data['item']
            track = SpotifyService.extract_track_data(track_json_data)
        else:
            track = []
            message = 'There is no current track you are listening on Spotify right now'
            logger_con.warning(message)
            logger_pro.warning(message)
        return track

    @staticmethod
    def remove_all_tracks_from_playlist(spotify, playlist_id) -> None:
        # TODO: Test to remove all tracks from a playlist even thought it's more than 100
        tracks = SpotifyService.retrieve_all_tracks_from_playlist(spotify,
                                                                  playlist_id)

        # TODO: if there are more than 100 tracks
        SpotifyRepository.remove_tracks_from_playlist(spotify,
                                                      playlist_id,
                                                      tracks)
        return

    def remove_tracks_from_playlist(self,
                                    playlist_id: str,
                                    tracks: list,
                                    first,
                                    last) -> None:

        # TODO Manage first and last number is proper
        """
        no:
            -1, -2,
            the number more than the number of tracks in playlist,
            first is bigger than last
        """
        tracks = tracks[first-1:last]

        self.repository.remove_tracks_from_playlist(playlist_id,
                                                            tracks)
        return

    @staticmethod
    def remove_tracks_played_recently_from_playlist(spotify,
                                                    playlist_id: str) -> None:
        tracks = []
        tracks_played_recently = []
        tracks_json_data = SpotifyRepository.get_tracks_played_recently(spotify)
        for track_json_data in tracks_json_data:
            track_json_data = track_json_data['track']
            tracks_played_recently += SpotifyService.retrieve_track_data(track_json_data)

        print('TRACKS PLAYED RECENTLY')
        SpotifyService.show_track_names(tracks_played_recently)
        playlist_tracks = SpotifyService.retrieve_all_tracks_from_playlist(spotify, playlist_id)
        for t in tracks_played_recently:
            if SpotifyService.is_in_track(t, playlist_tracks):
                tracks.append(t)

        SpotifyRepository.remove_tracks_from_playlist(spotify,
                                                      playlist_id,
                                                      tracks)

        return
