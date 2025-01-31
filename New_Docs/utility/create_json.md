# DP Create JSON
<img src="https://github.com/user-attachments/assets/e3c210b5-d718-4b8b-8e9b-c0963497b22b" alt="DP_Create_JSON" style="float: left; margin-right: 10px;"/>

## Description
The DP Create JSON node allows users to create a JSON file from structured data provided in a specific format. Users can specify the file name, save path, line separator, and the data to be converted into JSON format. The node also supports options for saving the file and handling naming conflicts.

## Inputs
- **STRING** - `file_name` - The name of the JSON file to be created (default: "my_json_file").
- **STRING** - `save_path` - The directory where the JSON file will be saved (default: "output\\json").
- **STRING** - `line_separator` - The character used to separate values in the input data (default: "|").
- **STRING** - `json_data` - The structured data to be converted into JSON format.
- **BOOLEAN** - `save_file` - Whether to save the JSON file (default: True).
- **BOOLEAN** - `overwrite` - Whether to overwrite an existing file with the same name (default: False).

## Outputs
- **STRING** - `json_text` - The generated JSON string.
- **STRING** - `log_info` - Information about the file creation process.

## Example Usage
To use the DP Create JSON node, connect the required inputs with the desired values. The node will output the generated JSON string and log information about the file creation process. If `save_file` is set to True, the JSON file will be saved to the specified path.
