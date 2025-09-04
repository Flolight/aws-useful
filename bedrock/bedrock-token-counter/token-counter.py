#!/usr/bin/env python3
import argparse
import sys
import os
import anthropic

def count_tokens(text, model="claude-opus-4-1-20250805"):
    """Count tokens in text using Anthropic's API"""
    client = anthropic.Anthropic()
    
    try:
        response = client.messages.count_tokens(
            model=model,
            messages=[{
                "role": "user",
                "content": text
            }]
        )
        return response.input_tokens
    except Exception as e:
        print(f"Error counting tokens: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Count tokens in text using Anthropic models")
    parser.add_argument("input", help="Text string or file path")
    parser.add_argument("-m", "--model", default="claude-opus-4-1-20250805", 
                       help="Model to use for token counting (default: claude-opus-4-1-20250805)")
    parser.add_argument("-f", "--file", action="store_true", 
                       help="Treat input as file path instead of text")
    
    args = parser.parse_args()
    
    # Check if API key is set
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        api_key = input("Enter your Anthropic API key: ").strip()
        if not api_key:
            print("Error: API key is required", file=sys.stderr)
            sys.exit(1)
        os.environ["ANTHROPIC_API_KEY"] = api_key
    
    # Get text content
    if args.file:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.input}' not found", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        text = args.input
    
    # Count tokens
    token_count = count_tokens(text, args.model)
    
    if token_count is not None:
        print(f"Token count: {token_count}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
