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


#########################

import mimetypes

def create_image_message(image_path):
    # Open the image file in "read binary" mode
    with open(image_path, "rb") as image_file:
        # Read the contents of the image as a bytes object
        binary_data = image_file.read()

    # Get the MIME type of the image based on its file extension
    mime_type, _ = mimetypes.guess_type(image_path)

    sub_type = mime_type.split("/")[-1]

    # Create the image block
    image_block = {
        "image": {
            "format": sub_type,
            "source": {
                "bytes": binary_data
            }
        }
    }

    return image_block

message = {
  "role": "user",
  "content": [
    {"text": "Identify the subject of each of these images, using a simple word for each image."},
    create_image_message("./images/test1.png"),
    create_image_message("./images/test2.png"),
  ]
}
response = bedrock_client.converse(
  modelId=modelId,
  messages=[messages],
)

print(response)



