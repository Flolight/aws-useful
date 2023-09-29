import boto3
import json
bedrock = boto3.client(service_name='bedrock-runtime',region_name='us-east-1')

body_cohere = json.dumps({
    "prompt": "explain generative ai to a 7 years old child",
    "max_tokens":250,
    "temperature": 0.1

})

modelId = 'cohere.command-text-v14'
accept = 'application/json'
contentType = 'application/json'

response = bedrock.invoke_model(body=body_cohere, modelId=modelId, accept=accept,contentType=contentType)

response_body = json.loads(response.get('body').read())
# text
print(response_body['generations'][0]['text'])
