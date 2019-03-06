from playcards.spotify import Player
import time


def test_player_can_play_a_song():
    player = Player('fixtures/config.yaml')
    player.open()
    player.set_track('spotify:track:7hVTXJLTzdFz6K28UEBLVf')
    player.play()
    time.sleep(10)
    player.close()

