import spotify
import random
import logging
import threading
from datetime import datetime
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_login_details():
    file = open(os.path.join(__location__, '.authentication'), 'r')
    csv = file.read()
    details = csv.split(',')
    file.close()
    return details


#logging.basicConfig(level=logging.DEBUG)

login = get_login_details()

logged_in_event = threading.Event()
end_of_track = threading.Event()

def connection_state_listener(session):
    if session.connection.state is spotify.ConnectionState.LOGGED_IN:
        logged_in_event.set()


def on_end_of_track(self):
    end_of_track.set()

time = int(datetime.now().strftime('%H%M%S'))

if (time < 230500) and (time > 93000):
    config = spotify.Config()
    config.load_application_key_file(os.path.join(__location__, 'spotify_appkey.key'))

    session = spotify.Session(config)
    loop = spotify.EventLoop(session)
    loop.start()

    session.on(spotify.SessionEvent.CONNECTION_STATE_UPDATED, connection_state_listener)
    session.on(spotify.SessionEvent.END_OF_TRACK, on_end_of_track)

    session.login(login[0], login[1])
    logged_in_event.wait()

    audio = spotify.AlsaSink(session)

    playlist = session.get_playlist('spotify:user:1154159617:playlist:64Dmb6PS1Rr4WT3XRF2imE')
    playlist.load()

    # Pick track
    track_number = random.randint(0, (len(playlist.tracks)-1))

    track = playlist.tracks[track_number]
    track.load()
    print(str(track_number) + ": " + track.name)

    session.player.load(track)
    session.player.play()

    try:
        while not end_of_track.wait(0.1):
            pass
    except KeyboardInterrupt:
        pass