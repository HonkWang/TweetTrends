#Import the necessary methods from tweepy library,elasticsearch & certifi
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from elasticsearch import Elasticsearch
import certifi
import json
from random import uniform
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut


endpoint = 'search-mytestdomain-qnyhs32jjgymxujnd6h75uqwtq.us-east-1.es.amazonaws.com'
#estabilish connection
es = Elasticsearch(hosts=[endpoint], port=443, use_ssl=True, ca_certs=certifi.where())

#Variables that contains the user credentials to access Twitter API 
access_token = "837190810621906944-FJj2YqU1tRyDiS2S4WDPeKJfmN6XhUB"
access_token_secret = "91fP560AMqSJIeTm4UlZFMA2YTvNcKRMVqZwLj0UDHeLy"
consumer_key = "HQIPvIVR26ehH9GibMzOY5zbX"
consumer_secret = "ES5WepQeeM10eikswEvH1vdiq6kBIOMdWFxfoDKwc5553xFMqz"

geo = GoogleV3()
# geo.__init__(api_key='AIzaSyBCQVwa2M37bSINXVZ5ns_ZMTyb9ExaCAU', domain='maps.googleapis.com', scheme='http', client_id=None, secret_key=None, timeout=5, proxies=None, user_agent=None)
# location = geo.geocode("Kentucky, USA")
# [location.latitude,location.longitude]
# print(location.raw)

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    
    def on_data(self, data):
        
        def do_geocode(address):
            try:
                return geo.geocode(address)
            except GeocoderTimedOut: 
                return do_geocode(address)
        
        tweet = json.loads(data)
        if tweet.get('id_str', None) != None:
            tweet_id = tweet.get('id_str')
            tweet_time = tweet['created_at']
            tweet_text = tweet['text']
            tweet_user = tweet['user']['screen_name']
            
            #tweet_geo = tweet['coordinates'] 
            latlng=[]
            if tweet['place']:
                latlng = tweet['place']['bounding_box']['coordinates'][0][0]
            #if it only has location
            elif tweet['user']['location']:
                #if it's not empty then can we use .latitude method
                try:
                    location = do_geocode(tweet['user']['location'])
                    if location: 
                        latlng = [location.latitude,location.longitude]
                    else:
                        latlng=[uniform(-180,180), uniform(-90, 90)]
                except:
                    latlng=[uniform(-180,180), uniform(-90, 90)]
            else: #if it's not any of these lists,randomly generate data
                latlng = [uniform(-180,180), uniform(-90, 90)]
            print latlng           
            
            tweet_feature = {
                'user': tweet_user,
                'text': tweet_text,
                'geo':  latlng,
                'time' : tweet_time
            }
            es.index(index='twittmap',doc_type='tweets',id=tweet_id,body=tweet_feature)
        return True

    def on_error(self, status):
        print status

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



