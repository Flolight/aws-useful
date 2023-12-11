import json
import boto3

# Sample method to extract IBAN from financial document
def extract_iban_from_document(bucket_name, document_name):
    textract = boto3.client('textract', region_name='us-east-1')

    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': document_name
            }
        }
    )
    print(response)

    # Extracting the IBAN
    iban = None
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            # Perform IBAN pattern matching
            if 'IBAN' in item['Text'] or 'iban' in item['Text']:
                # You can perform more specific IBAN pattern matching here if needed
                iban = item['Text']
                break

    return iban
