import boto3

def 
import boto3

def generate_s3_presigned_post(bucket_name, file_name):
  """
  This functions generates a pre-signed curl command to upload a file to S3
  :return: curl command to be used
  """
  BUCKET_NAME = bucket_name
  KEY_NAME = file_name
  
  s3 = boto3.client('s3',
      # Use your profile or credentials
      aws_access_key_id="YOUR-ACCESS-KEY-ID",
      aws_secret_access_key="YOUR-SECRET-ACCESS-KEY")
  
  resp = s3.generate_presigned_post(
      Bucket=BUCKET_NAME,
      Key=KEY_NAME,
  )
  
  resp['fields']['file'] = '@{key}'.format(key=KEY_NAME)
  
  form_values = "\n    ".join(["-F {key}={value} \\".format(key=key, value=value)
                          for key, value in resp['fields'].items()])
  command = f"curl -v {form_values} \n    {resp['url']}"
  return command
  
def list_s3_files_using_boto3_client(bucket_name):
    """
    This functions list all files in s3 bucket.
    :return: None
    """
    print(f"Listing in bucket: {bucket_name}")
    s3_client = boto3.client("s3")
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    files = response.get("Contents")
    for file in files:
        print(f"file_name: {file['Key']}, size: {file['Size']}")
        
def load_image_from_s3(bucket, photo)
    """
    Load image from S3 bucket
    """
    s3_connection = boto3.resource('s3')
    s3_object = s3_connection.Object(bucket,photo)
    s3_response = s3_object.get()
    stream = io.BytesIO(s3_response['Body'].read())
    image=Image.open(stream)
    
def display_image(image_name, bucket_name)
    """
    Display image from S3 bucket
    """
    display(IImage(url=s3_client.generate_presigned_url('get_object', 
                                                    Params={'Bucket': bucket_name, 
                                                            'Key'   : image_name})))
