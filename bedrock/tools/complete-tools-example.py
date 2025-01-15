import boto3, json, math


class ToolError(Exception):
    pass


def call_bedrock(message_list, tool_list):
    session = boto3.Session()

    bedrock = session.client(service_name="bedrock-runtime")

    response = bedrock.converse(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=message_list,
        inferenceConfig={"maxTokens": 2000, "temperature": 0},
        toolConfig={"tools": tool_list},
    )
    return response


def get_tool_result(tool_use_block):
    tool_use_name = tool_use_block["name"]

    print(f"Using tool {tool_use_name}")

    if tool_use_name == "cosine":
        return math.cos(tool_use_block["input"]["x"])
    elif tool_use_name == "sine":
        return math.sin(tool_use_block["input"]["x"])
    elif tool_use_name == "divide_numbers":
        return tool_use_block["input"]["x"] / tool_use_block["input"]["y"]
    else:
        raise ToolError(f"Invalid function name: {tool_use_name}")


def handle_llm_response(response_message):
    reponse_content_blocks = response_message["content"]

    follow_up_content_blocks = []

    for content_block in reponse_content_blocks:
        if "toolUse" in content_block:
            tool_use_block = content_block["toolUse"]

            try:
                tool_result_value = get_tool_result(tool_use_block)

                if tool_result_value is not None:
                    follow_up_content_blocks.append(
                        {
                            "toolResult": {
                                "toolUseId": tool_use_block["toolUseId"],
                                "content": [{"json": {"result": tool_result_value}}],
                            }
                        }
                    )
            except ToolError as e:
                follow_up_content_blocks.append(
                    {
                        "toolResult": {
                            "toolUseId": tool_use_block["toolUseId"],
                            "content": [{"text": repr(e)}],
                            "status": "error",
                        }
                    }
                )
    if len(follow_up_content_blocks) > 0:
        follow_up_message = {
            "role": "user",
            "content": follow_up_content_blocks,
        }

        return follow_up_message
    else:
        return None


def run_loop(prompt, tool_list):
    MAX_LOOPS = 6
    loop_count = 0
    continue_loop = True

    message_list = [{"role": "user", "content": [{"text": prompt}]}]

    while continue_loop:
        response = call_bedrock(message_list, tool_list)

        response_message = response["output"]["message"]
        print(f"run_loop message: {response_message}")
        message_list.append(response_message)

        loop_count += 1

        if loop_count >= MAX_LOOPS:
            print(f"Hit loop limit: {loop_count}")
            break
        follow_up_message = handle_llm_response(response_message)

        if follow_up_message is None:
            print("No follow-up message")
            continue_loop = False
        else:
            message_list.append(follow_up_message)

    return message_list


tools = [
    {
        "toolSpec": {
            "name": "cosine",
            "description": "Calculate the cosine of x.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        }
                    },
                    "required": ["x"],
                }
            },
        }
    },
    {
        "toolSpec": {
            "name": "sine",
            "description": "Calculate the sine of x.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        }
                    },
                    "required": ["x"],
                }
            },
        }
    },
    {
        "toolSpec": {
            "name": "tangent",
            "description": "Calculate the tangent of x.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        }
                    },
                    "required": ["x"],
                }
            },
        }
    },
    {
        "toolSpec": {
            "name": "divide_numbers",
            "description": "Divide x by y.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "x": {"type": "number", "description": "The numerator."},
                        "y": {"type": "number", "description": "The denominator."},
                    },
                    "required": ["x", "y"],
                }
            },
        }
    },
]

messages = run_loop("What is the tangent of 7?", tools)

print("\nMESSAGES:\n")
print(json.dumps(messages, indent=4))
