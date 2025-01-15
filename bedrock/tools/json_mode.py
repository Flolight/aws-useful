tools = [
  {
    "toolSpec": {
      "name": "print_sentiment_scores",
      "description": "Prints the sentiment scores of a given text.",
      "inputSchema": {
        "json": {
          "type": "object",
          "properties": {
            "positive_score": {"type": "number, "description": "The positive sentiment score, ranging from 0.0 to 1.0."},
            "negative_score": {"type": "number, "description": "The negative sentiment score, ranging from 0.0 to 1.0."},
            "neutral_score": {"type": "number, "description": "The neutral sentiment score, ranging from 0.0 to 1.0."},
          },
          "required": ["positive_score", "negative_score", "neutral_score"]
        }
      }
    }
  }
]

import json

def analyze_sentiment(content):
  query = f"""
  <text>
  {content}
  </text>

  Only use the print_sentiment_scores tool.
  """

  messages = [{
   "role": "user",
   "content": [{"text": query}]
  }]

  inference_config={"maxToken":400}
  tool_config={"tools":tools}

  response = bedrock_client.converse(
    modelId=model_id,
    messages=messages,
    inferenceConfig=inference_config,
    toolConfig=tool_config,
  )

  json_sentiment = None
  for content in response["output"]["messages"]["content"]:
    if content.get("toolUse") is not None and content["toolUse"]["name"] == "print_sentiment_scores":
      json_sentiment = content["toolUse"]["input"]
      break

  if json_sentiment:
    print("Sentiment Analysis (JSON)")
    print(json.dumps(json_sentiment, indent=2))
  else:
    print("No sentiment analysis found in the response.")
