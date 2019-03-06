from playcards.nfc import read_id

class System(object):
    def on_play_pressed(self):
        spotify_id = read_id()



