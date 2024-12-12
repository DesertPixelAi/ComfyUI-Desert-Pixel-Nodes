# DP Broken Token
<img src="https://github.com/user-attachments/assets/f9bfacd1-1b87-4225-ab67-12d5804ef2aa" alt="DP_Broken_Token" style="float: left; margin-right: 10px;"/>

## Description
The DP Broken Token node analyzes and splits Flux prompts based on user-defined token counts. It allows users to specify the maximum number of tokens for each part of the output, effectively breaking down a prompt into manageable segments.

## Inputs
- **STRING** - `prompt` - The input prompt to be analyzed and split. (Multiline input)
- **INT** - `max_tokens_part_1` - The maximum number of tokens for the first part of the output. (Default: 77, Min: 0, Max: 2000)
- **INT** - `max_tokens_part_2` - The maximum number of tokens for the second part of the output. (Default: 0, Min: 0, Max: 2000)

## Outputs
- **INT** - `total_tokens` - The total number of tokens in the input prompt.
- **STRING** - `info` - Information about the token analysis.
- **STRING** - `Text part 1` - The first part of the split text.
- **STRING** - `Text part 2` - The second part of the split text.
- **STRING** - `Text part 3` - The third part of the split text.

## Example Usage
To use the DP Broken Token node, connect a prompt to the `prompt` input and specify the maximum token counts for the parts. The node will output the total token count and the split text parts based on the specified limits. 
