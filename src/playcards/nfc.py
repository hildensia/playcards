import nfc
import ndef
import contextlib
from playcards.spotify import SpotifyId


class NfcError(Exception):
    NO_TAG_FOUND = 400

    def __init__(self, code):
        self.code


@contextlib.contextmanager
def nfc_open(source):
    """
    Opens a connection to the nfc reader.
    :param source: The source of the nfc reader (e.g. 'usb').
    """
    clf = nfc.ContactlessFrontend()
    clf.open(source)
    target = clf.sense(nfc.clf.RemoteTarget('106A'),
                       nfc.clf.RemoteTarget('106B'),
                       nfc.clf.RemoteTarget('212F'))
    if target is None:
        raise NfcError()

    tag = nfc.tag.activate(clf, target)

    yield tag

    clf.close()


def read_id():
    """
    Reads a SpotifyID from the NFC tag.
    :return: A SpotifyId object
    """
    try:
        with nfc_open('usb') as tag:
            for record in tag.ndef.records:
                if record.type == 'urn:nfc:wkt:T' and record.text.startswith('spotify:'):
                    return SpotifyId.from_string(record.text)
    except NfcError:
        pass
    return None


def write_id(id_):
    """
    Writes a spotify id it an NFC tag.
    :param id_: A spotifyId object to write.
    """
    with nfc_open('usb') as tag:
        record = ndef.TextRecord(str(id_))
        tag.ndef.records = [record]

