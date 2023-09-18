###
# Find Jumpstart model_package_arn (for Llama2 like models)
###
from sagemaker.jumpstart.model import JumpStartModel

# Define model id and region to pull from
model_id = "meta-textgeneration-llama-2-70b-f"
region = "us-east-1"

# Create a jumpstart model object
model = JumpStartModel(model_id=model_id, region="us-west-2")

# Get the model package arn for the model/region combination
model.model_package_arn
