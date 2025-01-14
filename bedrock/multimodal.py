import boto3

###### Simple test ######
with open("./images/test.png", "rb") as image_file:
  binary_data = image_file.read()

message = {
  "role": "user",
  "content": [
    {
      "image": {
        "format": 'png',
        "source": {
          "bytes": binary_data
        }
      }
    }
  ]
}

bedrock_client = boto3.client(service_name='bedrock-runtime', region_name="us-west-2")
model_id="anthropic.claude-3-5-sonnet-20241022-v2:0"

response = bedrock_client.converse(
  modelId=modelId,
  messages=[messages],
)

print(response)

###### Simple test with prompt ######

with open("./images/test.png", "rb") as image_file:
  binary_data = image_file.read()

message = {
  "role": "user",
  "content": [
    {"text": "Describe steps to prevent the scenario pictured in this image."},
    {
      "image": {
        "format": 'png',
        "source": {
          "bytes": binary_data
        }
      }
    }
  ]
}

bedrock_client = boto3.client(service_name='bedrock-runtime', region_name="us-west-2")
model_id="anthropic.claude-3-5-sonnet-20241022-v2:0"

response = bedrock_client.converse(
  modelId=modelId,
  messages=[messages],
)

print(response)
