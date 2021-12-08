import tweepy
import requests
import webbrowser
import time
import sys
import socket
import json

consumerKey = ''
consumerSecret = ''
accessTokenKey = ''
accessTokenSecret = ''

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)

try:
    authRedirect = auth.get_authorization_url()
except (Tweepy.TweepError):
    print("Couldn't get authorization URL!")
    
webbrowser.open(authRedirect)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('127.0.0.1', 5656))
serverSocket.listen(5)

notVerified = True
test = []
while (notVerified):
    csock, caddr = serverSocket.accept()
    print ("Connection from: " + repr(caddr))
    data = csock.recv(4096)
    test.append(data)
    print (testData)

try:
    auth.get_access_token(authcode)
except (Tweepy.TweepError):
    print("Bad authentication attempt!")
