from playcards.nfc import read_id, write_id


def test_write_id_writes_id_to_smart_card():
    track_id = 'spotify:track:0tfZx9yPiDbrDuWKeHqakX'
    write_id(track_id)

    id = read_id()
    assert id == track_id
