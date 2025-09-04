# Amazon Bedrock Token Counter

A simple Python tool to count tokens for models using AWS Bedrock's CountTokens API.

## Features

- Count tokens for text strings or files
- Uses AWS Bedrock (no separate API keys needed)
- Simple command-line interface
- Works with your existing AWS credentials

## Prerequisites

- Python 3.11+
- AWS CLI configured with credentials
- Access to AWS Bedrock with models enabled

## Installation

1. Clone or download the script:
```bash
curl -O https://raw.githubusercontent.com/aws-useful/bedrock/bedrock-token-counter/main/bedrock_token_counter.py
chmod +x bedrock_token_counter.py
```

2. Install dependencies:
```bash
pip install boto3
```

3. Ensure your AWS credentials are configured:
```bash
aws configure
```

## Usage

### Count tokens in text strings

```bash
python bedrock_token_counter.py "Hello, Claude! How are you today?"
```

### Count tokens in files

```bash
python bedrock_token_counter.py -f document.txt
```

### Use a specific Claude model

```bash
python bedrock_token_counter.py -m "anthropic.claude-3-haiku-20240307-v1:0" "Your text here"
```

### Command-line options

- `-f, --file`: Treat input as file path instead of text
- `-m, --model`: Specify Bedrock model ID (see supported models below)
- `-h, --help`: Show help message

## Shell Alias (Optional)

Add to your `.bashrc` or `.zshrc` for easier usage:

```bash
alias tokens='python /path/to/bedrock_token_counter.py'
```

Then use simply:
```bash
tokens "Hello, Claude"
tokens -f myfile.txt
```

## AWS Configuration

The tool uses your default AWS credentials. Ensure you have:

1. AWS CLI configured: `aws configure`
2. Appropriate IAM permissions for Bedrock
3. Access to Claude models in your AWS region

Required IAM permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:CountTokens"
            ],
            "Resource": "*"
        }
    ]
}
```

## Examples

```bash
# Basic usage
python bedrock_token_counter.py "What is the capital of France?"
# Output: Token count: 8

# Count tokens in a file
python bedrock_token_counter.py -f README.md
# Output: Token count: 1247

# Use Haiku model for faster/cheaper counting
python bedrock_token_counter.py -m "anthropic.claude-3-haiku-20240307-v1:0" "Short text"
# Output: Token count: 3
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details
