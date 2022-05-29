from oauthlib import oauth1
from os.path import exists
import pickle
import tweepy
import webbrowser
import socket, ssl, requests
import time
import string
import datetime
import json
import cloudinary, cloudinary.api, cloudinary.uploader
import subprocess # Used for getting HWID to slim down size used on image hosting server.

# Upload 
def GetUUID():
    cmd = 'wmic csproduct get uuid'
    uuid = str(subprocess.check_output(cmd))
    pos1 = uuid.find("\\n")+2
    uuid = uuid[pos1:-15]
    return uuid

# Given the path to an image, upload it and return the url it will be hosted at.
def UploadImage(image):
    # Config the cloudinary API handler
    cloudinary.config( 
      cloud_name = "arttergram", 
      api_key = "885197691968175", 
      api_secret = "9rBQhRwJNz2vfYYRFvwYh3yqoXM" 
    )
    
    # Upload the image to the cloud, unique by the first 6 digits of the user PC's HWID to avoid
    # spamming my image server to high hell and back.
    uploadDetails = cloudinary.uploader.upload(
        image,
        public_id = GetUUID()[0:6])

    # Return the URL to the uploaded image.
    return uploadDetails['url']

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

def CreateInstagramAPI(clientAuth):

    # Check if a seralized API exists to avoid re-logging in.
#    if (exists('instagramAPISerial.txt')):
#            with open("instagramAPISerial.txt", "rb") as tokenFile:
#                apiSerialized = tokenFile.read()
#                api = pickle.loads(apiSerialized)
#    else:
        # Create a new API object and sign in if an existing one is not found.
    
        # Request authentication data.
        response = requests.post('https://graph.facebook.com/v2.6/device/login?access_token=%s&scope=instagram_basic,pages_show_list,pages_read_engagement' % clientAuth)
        response = json.loads(response.content.decode())

        # Take and save the necessary information from the request.
        code = response.get("code")
        userCode = response.get("user_code")
        authuri = response.get("verification_uri")
        expiration = response.get("expires_in")
        expirationInterval = response.get("interval")

        # Tell user to enter code
        # !! IMPLEMENT LOGIN METHOD?
        print("Please navigate to the below and enter the following authorization code: " + userCode + '\n')
        print(authuri.replace("\\", "") + "/")

        # Declare access token and expirary time.
        accessToken = ''
        accessTokenExpirationTime = 0

        # Poll for access granted by user, then store the token and time remaining.
        while (True):
            # Wait to avoid over-polling status.
            time.sleep(expirationInterval)

            # Make request to check status, then convert to a dictionary
            authStatus = requests.post("https://graph.facebook.com/v2.6/device/login_status?access_token=%s&code=%s" % (clientAuth, code)).content.decode()
            authStatus = json.loads(authStatus)

            print(authStatus)

            # Check if status succeeded.
            if ("access_token" in authStatus):
                accessToken = authStatus.get("access_token") # Store the access token.
                accessTokenExpirationTime = authStatus.get("expires_in") # Store the token expirary.
                break
            elif (authStatus.get(code) == 463 or authStatus.get(code) == 17): # Check if code entry expired.
                print("Code expired, reattempt authentication from step 1!")
        
        print(requests.get("https://graph.facebook.com/v2.3/me?fields=name,picture&access_token=%s" % accessToken))
        # !! IMPLEMENT TOKEN EXPIRATION CHECKING
        #print(accessTokenExpirationTime) # Seconds remaining until token expires.
        
        print(authStatus)
        token = requests.post("https://api.instagram.com/oauth/access_token?client_id=")

        # Store user profile basics for display.
        instagramProfile = requests.get("https://graph.facebook.com/v2.3/me?fieldsname=name,picture&access_token=%s" % accessToken)
        instagramProfile = json.loads(instagramProfile.content.decode())
        print(instagramProfile.get("data"))

        # Request the Facebook account profile.
        instagramProfileEndpoint = requests.get("https://graph.facebook.com/v14.0/me/accounts?access_token=%s" % accessToken)
        
        
        

        # !! IMPLEMENT GETTING CORRECT CREATOR ACCOUNT

        # Create SSL socket
        #sslWrapper = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        #socObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #socketServer = sslWrapper.wrap_socket(socObj, server_hostname="127.0.0.1")
        #socketServer.connect(("127.0.0.1", 5656))


        # Serialize the API and write the bytes to a text file.
        #with open("instagramAPISerial.txt", "xb") as tokenFile:
        #    tokenFile.write(pickle.dumps(api)) 

def main():
    # Initialize/Read the serialized API.  

    # Create instagram api object here

    # Post an image here to instagram
    #UploadImage("success.png")
    print("end")

if __name__ == "__main__":
    main()
    



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