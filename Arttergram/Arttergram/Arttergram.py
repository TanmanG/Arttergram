from oauthlib import oauth1
from os.path import exists
import pickle
import tweepy
import webbrowser
import socket, ssl, requests
import random
import string
import time

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

def CreateInstagramAPI():

    # Check if a seralized API exists to avoid re-logging in.
#    if (exists('instagramAPISerial.txt')):
#            with open("instagramAPISerial.txt", "rb") as tokenFile:
#                apiSerialized = tokenFile.read()
#                api = pickle.loads(apiSerialized)
#    else:
        # Create a new API object and sign in if an existing one is not found.
    
        response = requests.post('https://graph.facebook.com/v2.6/device/login?access_token=<TOKEN>&scope=instagram_basic,pages_show_list')
        
        #print(response.content.decode().split('"'))

        # Take and save the necessary information from the request.
        code = response.content.decode().split('"')[3]
        userCode = response.content.decode().split('"')[7]
        authuri = response.content.decode().split('"')[11]
        expiration = response.content.decode().split('"')[14]
        expirationInterval = int(response.content.decode().split('"')[16])

        print("Please navigate to the below and enter the following authorization code: " + userCode + '\n')
        print(authuri.replace("\\", ""))

        while (True):
            time.sleep(expirationInterval)
            authStatus = requests.post("https://graph.facebook.com/v2.6/device/login_status")

    
        #keyString = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(11))
        #digit = ''.join(random.choice(string.digits) for _ in range(9))
        #webbrowser.open("https://www.facebook.com/v13.0/dialog/oauth?client_id={501319271390126}&state={{st=%s,ds=%s}}" % (keyString, digit))
        
        

        # Create SSL socket
        #sslWrapper = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        #socObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #socketServer = sslWrapper.wrap_socket(socObj, server_hostname="127.0.0.1")
        #socketServer.connect(("127.0.0.1", 5656))


        # Serialize the API and write the bytes to a text file.
        #with open("instagramAPISerial.txt", "xb") as tokenFile:
        #    tokenFile.write(pickle.dumps(api)) 

# Initialize/Read the serialized API.  
#tAPI = CreateTwitterAPI('')
CreateInstagramAPI()
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