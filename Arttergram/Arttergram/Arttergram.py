from oauthlib import oauth1
import tweepy
import webbrowser
import socket

host = '127.0.0.1'
port = 5656

# Key Declarations
consumerKey = 'ZqUlCOtnRjAC2fDTn3YHRxP8W'
consumerSecret = 'Z34TZxcdDL9nH0HHnNC7113YBy2WmVF6F7cck6DiakxNnATZIF'

# Tweepy Setup
auth = tweepy.OAuth1UserHandler(consumerKey, consumerSecret)

# Authorization URL Request
try:
    authRedirect = auth.get_authorization_url()
except:
    print("Couldn't get authorization URL!")
    
# Open the Authorization Page
webbrowser.open(authRedirect)

# Get OAuth Redirect using Socket
socketServer = socket.socket() # Declare the socket server.

# Binding and config.
socketServer.bind((host, port)) # Bind the server to an IP and Port
socketServer.listen(1) # Configure to listen for one client

# Connection & Transfer
connection, address = socketServer.accept() # Accept incoming connection and store variables
with connection: # Take the data and close the socket.
    print("Connection: ", address)
    data = connection.recv(1024)
    connection.send('HTTP/1.0 200 OK\n'.encode())
    connection.send('Content-Type: text/html\n'.encode())
    connection.send('\n'.encode())
    connection.send("""
        <html>
        <head>
        <meta charset="utf-8"/>
            <style>
            h1 {
                text-align: center;
                margin-top: 45vh;
                }
            </style>
        <body>
            <h1>
            You may close this page.
            </h1>
        </body>
        </html>
    """.encode()) # Send HTML to notify end-user on next step.
print(data)

# Exract the variable for user OAuth
paramRaw = data.split()[1].decode().split('=') # Decode then split the raw parameter data.
oauthToken = paramRaw[1].split('&')[0]
oauthVerifier = paramRaw[2]

# Trade OAuth tokens in for access tokens.
accessToken, accessTokenSecret = auth.get_access_token(oauthVerifier)
auth.set_access_token(accessToken, accessTokenSecret)

# Initialize the API.
api = tweepy.API(auth)
# API for v1
# Client for v2
## The API has been authenticated and is now ready for use!!!


#api.update_status("Hello world!")

print("Token: " + oauthToken)
print("Verifier: " + oauthVerifier)

# Current Flow:
# 1. Twitter Auth Page Redirects
# 2. Socket server catches request with parameters
# 3. Split recieved variables into independent
# 4. Relearn wtf I'm doing with the OAuth token stuff???

# CURRENTLY
# 1. Test Socket server functionality
# 2. Implement OAuth token hand-off