import spotify
import random
import time

def get_login_details():
    file = open('.authentication', 'r')
    csv = file.read()
    details = csv.split(',')
    file.close()
    return details


config = spotify.Config()
config.user_agent = "Christmasify"
login = get_login_details()

session = spotify.Session(config)
session.login(login[0], login[1])
session.process_events()
time.sleep(15)  # Sleep for 5 seconds because the threading method doesn't work properly :(

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
