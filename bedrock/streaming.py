response = bedrock_client.converse_stream(
  modelId=model_id,
  messages=messages
)

for event in response["stream"]:
    if 'messageStart' in event:
        print(f"\nRole: {event['messageStart']['role']}")

    if 'contentBlockDelta' in event:
        print(event['contentBlockDelta']['delta']['text'], end="")

    if 'messageStop' in event:
        print(f"\nStop reason: {event['messageStop']['stopReason']}")

    if 'metadata' in event:
        metadata = event['metadata']
        if 'usage' in metadata:
            print("\nToken usage")
            print(f"Input tokens: {metadata['usage']['inputTokens']}")
            print(
                f":Output tokens: {metadata['usage']['outputTokens']}")
            print(f":Total tokens: {metadata['usage']['totalTokens']}")
        if 'metrics' in event['metadata']:
            print(
                f"Latency: {metadata['metrics']['latencyMs']} milliseconds")
