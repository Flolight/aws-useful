import json
import boto3

#############################################
# Call an Amazon SageMaker Jumpstart endpoint
#############################################

endpoint_name = 'your-endpoint'

prompt = "I believe the meaning of life is"

payload = {
  "inputs": prompt,
  "parameters": {"max_new_tokens": 64, "top_p": 0.9, "temperature": 0.6, "return_full_text": False}
}
def query_endpoint(payload):
    client = boto3.client("sagemaker-runtime")
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload),
        # Needed for Llama 2 model
        CustomAttributes="accept_eula=true",
    )
    response = response["Body"].read().decode("utf8")
    response = json.loads(response)
    return response
  
#############################################
