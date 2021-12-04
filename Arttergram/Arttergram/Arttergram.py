import twitter

consumerKey = ''
consumerSecret = ''
accessTokenKey = ''
accessTokenSecret = ''

# Generate an API from given keys.
api = twitter.Api(consumer_key = consumerKey, 
                  consumer_secret = consumerSecret, 
                  access_token_key = accessTokenKey, 
                  access_token_secret = accessTokenSecret);

print(api.VerifyCredentials())

api.PostUpdate(caption)

mediaID = api.UploadMediaChunked(artName)