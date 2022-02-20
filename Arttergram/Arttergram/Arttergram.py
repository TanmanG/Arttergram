from oauthlib import oauth1
from os.path import exists
import pickle
import tweepy
import webbrowser
import socket

# Tweepy Setup
def CreateTwitterAPI(consumerKey, consumerSecret):

    # Declare the handler.
    handler = tweepy.OAuth1UserHandler(consumerKey, consumerSecret)
    
    # Attempt to use existing token.
    if (exists('twitterAPISerial.txt')):
            with open("twitterAPISerial.txt", "rb") as tokenFile:
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
        
        # Construct a new API object using the finished handler.
        api = tweepy.API(handler)

        # Serialize and write the API to a text file.
        with open("twitterAPISerial.txt", "xb") as tokenFile:
            tokenFile.write(pickle.dumps(api))   
    return api

def CreateInstagramAPI(username, password):

    # Check if a seralized API exists to avoid re-logging in.
    if (exists('instagramAPISerial.txt')):
            with open("instagramAPISerial.txt", "rb") as tokenFile:
                apiSerialized = tokenFile.read()
                api = pickle.loads(apiSerialized)
    else:
        # Create a new API object and sign in if an existing one is not found.

        
        # Serialize the API and write the bytes to a text file.
        #with open("instagramAPISerial.txt", "xb") as tokenFile:
        #    tokenFile.write(pickle.dumps(api)) 

# Initialize/Read the serialized API. 
#tAPI = CreateTwitterAPI('', '')
# Create instagram api object here

# Post an image here to instagram
#with open("TestImage.png", "rb") as image:
#    image = image.read()
    



# Current Flow:
# Twitter:
# 1. Twitter Auth Page Redirects
# 2. Socket server catches request with parameters
# 3. Split recieved variables into independent vars
# 4. Generate a new access token
# 5. Serialize the API object for future use
# 6. Profit
# Instagram:
# 1. I got no clue yet

# CURRENTLY
# 1. Implement instagram API
# 2. Implement other APIs