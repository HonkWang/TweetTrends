
# coding: utf-8

# In[ ]:

import json
import boto3
import requests
from multiprocessing import Pool

# Before running the program, remember to 
# update the IAM of the AWS that allow access to SQS&SNS services

# Get the SQS service resource with region_name, access_key and secret_access key
sqs = boto3.resource('sqs', 
                     region_name='us-east-1', 
                     aws_access_key_id = 'AKIAILGJNSA3DGSTGNFA', 
                     aws_secret_access_key= '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')
queue = sqs.get_queue_by_name( QueueName = 'TweetTrends' )

# Same way of getting service resource on SNS
sns = boto3.resource('sns', 
                     region_name='us-east-1', 
                     aws_access_key_id = 'AKIAILGJNSA3DGSTGNFA', 
                     aws_secret_access_key= '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')

# Endpoint for elasticsearch
endpoint = 'https://search-twitt-trends-r5ndyqwtijzgth4oymeqymz6yq.us-east-1.es.amazonaws.com'

# Create topic named TwittTrends & Create subscriber
TwittTrend = sns.create_topic( Name = 'TwittTrends' )
TwittTrend.subscribe( TopicArn = TwittTrend.arn,
                      Protocol='https',
                      Endpoint= endpoint)




# Get tweet from queue and process text sentiment
# Push to amazon SNS
def worker(_):
    while True:
        for message in queue.receive_messages( MaxNumberOfMessages=10, WaitTimeSeconds=10 ):
            try:
                tweet =  json.loads( message.body )
                #Use Text-Processing as an api for sentiment analysis
                default_url = 'http://text-processing.com/api/sentiment/'
                tweet_text = tweet['text']
                defualt_data = [
                  ('text', tweet_text)
                ]
                r = requests.post( default_url, data = defualt_data)
                tweet['sentiment'] = json.loads(r.content)['label']
                print tweet['sentiment']        
                TwittTrend.publish( Message = json.dumps(tweet, ensure_ascii=False) )
                
            finally:
                message.delete()

if __name__ == '__main__':
    p = Pool(3)
    print p.map(worker, [1, 2, 3])

