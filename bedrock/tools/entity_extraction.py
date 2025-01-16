tools = [
  {
    "toolSpec": {
      "name": "print_entities",
      "description": "Prints extract named entities.",
      "inputSchema": {
        "json": {
          "type": "object",
          "properties": {
            "entities": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "name": {"type": "string", "description": "The extracted entity name."},
                  "type": {"type": "string", "description": "The entity type 'e.g., PERSON, ORGANIZATION, LOCATION)."},
                  "context": {"type": "string", "description": "The context in which the entity appears in the text."}
                },
                "required": ["name", "type", "context"]
              }
            }
          },
          "required": ["entities"]
        }
      }
    }
  }
]

import json


text = "James works at MA Lighting in Frankfort. He met with Jane, the CEO of Chamsys Inc., last week in San Francisco."
query = f"""
<document>
{content}
</document>

Use the print_entities tool.
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

print(response["output"])
print(response["output"]["messages"]["content"])
