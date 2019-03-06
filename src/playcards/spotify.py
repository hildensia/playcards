import spotify
import yaml

import threading
import re


class SpotifyId(object):
    def __init__(self, type, id):
        self.type = type
        self.id = id

    @staticmethod
    def from_string(string):
        match = re.match(r'spotify\:(.*):(.*)', string)
        type = match.group(2)
        id = match.group(3)
        return SpotifyId(type, id)

    def __str__(self):
        return "spotify:{}:{}".format(self.type, self.id)

    def __repr__(self):
        return "spotify:{}:{}".format(self.type, self.id)


class Player(object):
    def __init__(self, config_file):
        with open(config_file, 'r') as fh:
            self.config = yaml.load(fh)

        self.session = spotify.Session()
        self.session.on(spotify.SessionEvent.CONNECTION_STATE_UPDATED,
                        self.connection_state_listener)
        self.audio = spotify.AlsaSink(self.session)
        self.loop = spotify.EventLoop(self.session)

        self.logged_in = threading.Event()

    def connection_state_listener(self, session):
        if session.connection.state == spotify.ConnectionState.LOGGED_IN:
            self.logged_in.set()

    def open(self):
        self.loop.start()
        self.session.login(self.config['user'], self.config['password'])
        self.logged_in.wait()

    def close(self):
        self.session.logout()
        self.loop.stop()

    def set_track(self, track_id):
        self.track = self.session.get_track(track_id)
        self.track.load()
        self.session.player.load(self.track)

    def play(self):
        self.session.player.play()

    def pause(self):
        self.session.player.pause()

    def handle_album(self, spotify_id):
        pass

    def handle_playlist(self, spotify_id):
        pass

    def handle_track(self, spotify_id):
        pass

