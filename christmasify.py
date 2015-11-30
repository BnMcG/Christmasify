import spotify
import threading

def get_login_details():
    file = open('.authentication', 'r')
    csv = file.read()
    details = csv.split(',')
    return details

logged_in_event = threading.Event()
def connection_state_listener(session):
    if session.connection.state is spotify.ConnectionState.LOGGED_IN:
        logged_in_event.set()

config = spotify.Config()
config.user_agent = "Christmasify"
login = get_login_details()

session = spotify.Session(config)
loop = spotify.EventLoop(session)
loop.start()

session.on(spotify.SessionEvent.CONNECTION_STATE_UPDATED,connection_state_listener)

session.login(login[0], login[1])
logged_in_event.wait()

playlist = session.get_playlist('spotify:user:1154159617:playlist:64Dmb6PS1Rr4WT3XRF2imE')
playlist.load()