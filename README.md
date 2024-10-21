### Extract structure data from invoices

Leverage Bedrock converse API invoke Claude 3 extract structure data from invoices. For stable data extraction, tool use is employed.

1. Convert pdf files to jpeg/png/webp etc.
1. Define fields need in the tools configuration
1. Invoke claude 3 with prompt and invoice images


#### Refs

1.[JSON output with claude tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use#json-output) 
1.[Extract structure data with tool use](https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/extracting_structured_json.ipynb)