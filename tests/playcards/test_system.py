import time
from playcards.spotify import Player
from playcards.nfc import read_id

def test_player_can_play_a_song():
    player = Player('fixtures/config.yaml')
    player.open()
    player.set_track(read_id())
    player.play()
    while True:
        time.sleep(1)
    player.close()