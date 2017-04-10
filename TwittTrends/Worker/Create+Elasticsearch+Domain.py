
# coding: utf-8

# In[ ]:

import boto3
# Before running the program, remember to 
# update the IAM of the AWS that allow access to Elasticsearch services

el = boto3.client('es',
                  region_name='us-east-1', 
                  aws_access_key_id = 'AKIAILGJNSA3DGSTGNFA', 
                  aws_secret_access_key= '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')

el.create_elasticsearch_domain( DomainName='twitt-trends',
                                ElasticsearchVersion = '5.1',
                                ElasticsearchClusterConfig={
                                    'InstanceType': 't2.small.elasticsearch',
                                    'InstanceCount': 1,
                                    'DedicatedMasterEnabled': False,
                                    'ZoneAwarenessEnabled': False,
                                    },
                                EBSOptions={
                                    'EBSEnabled': True,
                                    'VolumeType': 'gp2',
                                    'VolumeSize': 10,
                                    },
                                )
response = el.describe_elasticsearch_domain(
    DomainName='twitt-trends'
)
while True:
    try:
        endpoint = response['DomainStatus']['Endpoint']
#         print endpoint
        break
    except:
        continue

