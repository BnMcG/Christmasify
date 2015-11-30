import spotify
import random
import logging

def get_login_details():
    file = open('.authentication', 'r')
    csv = file.read()
    details = csv.split(',')
    file.close()
    return details


logging.basicConfig(level=logging.DEBUG)

login = get_login_details()
print(login[0])
print(login[1])

session = spotify.Session()
session.login(login[0], login[1])

# Do nothing until logged in
while session.connection.state != spotify.ConnectionState.LOGGED_IN:
    session.process_events()

playlist = session.get_playlist('spotify:user:1154159617:playlist:64Dmb6PS1Rr4WT3XRF2imE')
playlist.load()

loop = spotify.EventLoop(session)
loop.start()

# Pick track
track_number = random.randint(0, (len(playlist.tracks)-1))
print(track_number)

audio = spotify.AlsaSink(session)

track = playlist.tracks[track_number]
track.load()
print(track.name)

session.player.load(track)
session.player.play()
