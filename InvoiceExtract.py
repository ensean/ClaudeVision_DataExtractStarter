import os
import json
import base64
import boto3

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return image_file.read()

# only one demo tool
tools = [
    {
        "toolSpec": {
            "name": "extract_invoice_info",
            "description": "Extracts key information from the invoice.",
            "inputSchema": {
                "json": {
                "type": "object",
                    "properties": {
                        "expense_type": {"type": "string", "description": "The expense types, ONLY choose in hotel, food, transportation and others"},
                        "invoice_number": {"type": "string", "description": "The invoice number."},
                        "invoice_date": {"type": "string", "description": "The date of the invoice. The date should be in yyyy-MM-dd format."},
                        "total_amount": {
                                "type": "string", 
                                "description": "The total amount on the invoice. Only include numbers."
                            },
                        "currency": {"type": "string", "description": "The symbol of the currency, such as CNY/USD/HKD/KRW etc."}
                    },
                    "required": ["expense_type", "invoice_number", "invoice_date", "total_amount", "currency"]
                }
            }
        }
    }
]

def extract_invoice_info(image_path):
    base64_image = encode_image(image_path)
    
    prompt = """
    Analyze the following invoice image and extract the following information:
    1. Invoice Number
    2. Invoice Date
    3. Total Amount
    4. Expense type
    5. Currency
  

    Use the extract_invoice_info tool to provide the extracted information.  If the image is not an invoice or data missing still return using the tool with values of null.

    Here's the invoice image:
    """
    # create bedrock runtime client and inference with bedrock converse api
    br = boto3.client('bedrock-runtime', region_name='us-west-2')
    response = br.converse(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt,
                    },
                    {
                        "image": {
                            "format": "jpeg",
                            "source": {
                                "bytes": base64_image
                            }
                        }
                    }
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 4096,
        },
        toolConfig={
            "tools": tools,
            # forece use of the tool
            "toolChoice": {
                "tool": {
                    "name": "extract_invoice_info"
                }
            }
        }
    )

    return response

def parse_claude_response(response):
    for content in response['output']['message']['content']:
        if 'toolUse' in content.keys():
            return content['toolUse']['input']
    # no msg extracted
    return None
        

def save_to_json(data, output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    image_path = './InvoiceImages/case007.jpg'
    output_file = 'invoice_extract.json'
    
    claude_response = extract_invoice_info(image_path)
    invoice_entities = parse_claude_response(claude_response)
    save_to_json(invoice_entities, output_file)
    
    print(f"Invoice has been extracted and saved to {output_file}")
    print("Extracted Invoice:")
    print(json.dumps(invoice_entities, indent=2))

if __name__ == "__main__":
    main()