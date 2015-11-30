import spotify

config = spotify.Config()
config.user_agent = "Christmasify"

session = spotify.Session(config)
session.login()