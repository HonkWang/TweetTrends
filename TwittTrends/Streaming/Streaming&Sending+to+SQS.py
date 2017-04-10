
# coding: utf-8

# In[ ]:

#Import the necessary methods from tweepy library,elasticsearch & certifi
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import certifi
import json
import boto3
# Before running the program, remember to update the IAM of the AWS that allow access to SQS services
# Get the service resource with region_name, access_key and secret_access key
sqs = boto3.resource('sqs', 
                     region_name='us-east-1', 
                     aws_access_key_id = 'AKIAILGJNSA3DGSTGNFA', 
                     aws_secret_access_key= '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')
# Create the queue. This returns an SQS.Queue instance
queue = sqs.create_queue( QueueName = 'TweetTrends', Attributes = {'DelaySeconds': '5'} )


#Variables that contains the user credentials to access Twitter API 
access_token = "837190810621906944-FJj2YqU1tRyDiS2S4WDPeKJfmN6XhUB"
access_token_secret = "91fP560AMqSJIeTm4UlZFMA2YTvNcKRMVqZwLj0UDHeLy"
consumer_key = "HQIPvIVR26ehH9GibMzOY5zbX"
consumer_secret = "ES5WepQeeM10eikswEvH1vdiq6kBIOMdWFxfoDKwc5553xFMqz"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    
    def on_data(self, data):        
        tweet = json.loads(data)
        if tweet.get('id_str', None) != None:
            tweet_time = tweet['created_at']
            tweet_text = tweet['text']
            tweet_user = tweet['user']['screen_name']
            latlng=[]
            
# See if tweet has geolocation info and is in English.      
            if tweet['coordinates'] and tweet['lang'] == 'en':        
                latlng = tweet['coordinates']['coordinates']
                print latlng 
                tweet_feature = {
                    'user': tweet_user,
                    'text': tweet_text,
                    'geo':  latlng,
                    'time' : tweet_time
                }
                
# Send message to aws SQS event queue            
                message = json.dumps(tweet_feature)
                print message
                queue.send_message(MessageBody = message)           
        return True

    def on_error(self, status):
        print status,'error'

if __name__ == '__main__':
    while True:
        try:
            #This handles Twitter authetification and the connection to Twitter Streaming API
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, l)
            #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
            stream.filter(track=['Trump', 'Hilary','Obama','Amazon','Google','New York','Python','Technology','Stanford','Columbia'])
        
        except KeyboardInterrupt:
            break
        except:
            continue     

