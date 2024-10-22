### Extract structure data from invoices

Leverage Bedrock converse API invoke Claude 3 extract structure data from invoices. For stable data extraction, tool use is employed.

1. Convert pdf files to jpeg/png/webp etc.
1. Define fields need in the tools configuration
1. Invoke claude 3 with prompt and invoice images


#### Results

* Pros
    * can extract desired data from well formatted documents

* Cons
    * Can not handle sum up operation for invoice without total amount
    * Can not infer the transaction date
    * Can not handle large invoice, claude image input is limited to 8000x8000 pixel

#### Refs

1. [JSON output with claude tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use#json-output) 
1. [Extract structure data with tool use](https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/extracting_structured_json.ipynb)
1. [Forcing JSON with tool use](https://github.com/aws-samples/prompt-engineering-with-anthropic-claude-v-3/blob/main/10_2_2_Tool_Use_for_Structured_Outputs.ipynb)