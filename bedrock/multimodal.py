import boto3

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
