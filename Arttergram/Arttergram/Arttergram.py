from oauthlib import oauth1
from os.path import exists
import pickle
import tweepy
import webbrowser
import socket

# Tweepy Setup
def CreateTwitterAPI():
    # Key Declarations, keys belong to the API program on the dev side.
    consumerKey = '' # API Key here
    consumerSecret = '' # API Key Secret here

    # Declare the handler.
    handler = tweepy.OAuth1UserHandler(consumerKey, consumerSecret)
    
    # Attempt to use existing token.
    if (exists('serializedAPI.txt')):
            with open("seralizedAPI.txt", "rb") as tokenFile:
                apiSerialized = tokenFile.read()
                api = pickle.loads(apiSerialized)
    else:
        # Network Information
        host = '127.0.0.1'
        port = 5656

        # Authorization URL Request
        try:
            authRedirect = handler.get_authorization_url()
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
        accessToken, accessTokenSecret = handler.get_access_token(oauthVerifier)
        handler.set_access_token(accessToken, accessTokenSecret)
        
        api = tweepy.API(handler)

        with open("serializedAPI.txt", "xb") as tokenFile:
            tokenFile.write(pickle.dumps(api))   
    return api

# Initialize/Read the serialized API.
api = CreateTwitterAPI()


# Current Flow:
# 1. Twitter Auth Page Redirects
# 2. Socket server catches request with parameters
# 3. Split recieved variables into independent
# 4. Relearn wtf I'm doing with the OAuth token stuff???

# CURRENTLY
# 1. Implement token persistence
# 2. Implement other APIs