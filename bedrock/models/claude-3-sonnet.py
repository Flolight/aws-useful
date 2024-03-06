import base64
import httpx

def get_claude_response(messages="", 
                        token_count=250, 
                        temp=0,
                        topP=1, 
                        topK=250, 
                        stop_sequence=["Human:"], 
                        model_id = "anthropic.claude-3-sonnet-20240229-v1:0"):
    """
    For calling Claude. 
    """
    body = create_claude_body(messages=messages, 
                              token_count=token_count, 
                              temp=temp,
                              topP=topP, 
                              topK=topK, 
                              stop_sequence=stop_sequence)
    response = bedrock_rt.invoke_model(modelId=model_id, body=json.dumps(body))
    response = json.loads(response['body'].read().decode('utf-8'))
    return response

image_url = "https://commons.wikimedia.org/wiki/File:Owoce_Jab%C5%82ko.jpg#/media/Fichier:Owoce_Jab%C5%82ko.jpg"
image_media_type = "image/jpeg"
image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")
    
prompt = [{"role": "user", "content": [
  {
    "type": "image",
    "source": {
      "type": "base64",
      "media_type": image_media_type, # png, jpeg
      "data": image_data,
    }
  },
  {"type": "text", "text": "What's in the image?"}
]}]
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
text_resp = get_claude_response(messages=prompt, 
                                system="You interpret images and give the user an idea of what they are about",
                                 token_count=250, 
                                 temp=0,
                                 topP=1, 
                                 topK=0, 
                                 stop_sequence=["Human:"], 
                                 model_id = model_id)
