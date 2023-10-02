To call a Bedrock model, using a Python Lambda Function, follow the steps below:

1. Prerequisites:
    1. From the Bedrock console [get access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) to the specific model in the same region that you are deploying your Lambda function in.
    2. Provide an IAM role to access Bedrock models

```yaml
PolicyDocument:
Version: "2012-10-17"
Statement: 
- Effect: Allow
Action:
- bedrock:InvokeModel
Resource: !Sub arn:aws:bedrock:${AWS::Region}::foundation-model/*
```
2. Ensure your Lambda Function time-out is set to 60 secs (can be lower or higher depending on your prompt)
3. Lambda Runtime should be Python 3.9 or higher
4. Have a `requirements.txt` file with the following included:

`boto3==1.28.57`  

5. Lambda code (to call `anthropic.claude-v2 foe example)` is as follows:

```python
import os
import json
import boto3

region = os.environ.get('AWS_DEFAULT_REGION')
bedrock = boto3.client(service_name='bedrock-runtime',
                       region_name=region)

model_kwargs = {
                "max_tokens_to_sample": 300,
                "temperature": 1,
                "top_p": 0.9 
               }
               
accept = '*/*'
contentType = 'application/json'

def lambda_handler(event, context):
    prompt = "\n\nHuman:explain black holes to 8th graders in 3 sentences\n\nAssistant:"

    model_kwargs["prompt"] = prompt
    body = json.dumps(model_kwargs)

    print(body)
    modelId = 'anthropic.claude-v2'
    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept,
                                    contentType=contentType)

    response_body = json.loads(response.get('body').read())
    print(response_body)
    print(response_body.get('completion'))
    return_message = response_body.get('completion')

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": return_message
        }),
    }
```
