# Prompt Manager & Mode Controller

## Description

These nodes work together to manage prompts and control prompt modes. The Prompt Manager provides comprehensive prompt management with subject cycling, scene description integration, and multiple prompt modes, while the Mode Controller helps manage and route different prompt modes.

## Prompt Manager

### Inputs

#### Required:
- **prompt_mode**: (`COMBO`) - Operation mode:
  - "Prompt_Manager_Prompt" - Use subject and scene
  - "Random_Prompt" - Use random prompt input
  - "Other_Prompt" - Use other prompt input
- **subject**: (`STRING`, multiline) - Subject list to cycle through
- **subject_index_control**: (`COMBO`) - Subject cycling mode:
  - "increment" - Move to next subject
  - "decrement" - Move to previous subject
  - "randomize" - Select random subject
  - "fixed" - Use specified index
- **index**: (`INT`, default: 0) - Subject selection for fixed mode
- **find_replace_subject**: (`STRING`, default: "#sub") - Subject replacement token
- **scene_description**: (`STRING`, multiline) - Scene context or additional prompt text
- **weight**: (`FLOAT`, default: 1.0, range: 0.0-10.0) - Weight to apply to final prompt

#### Optional:
- **random_prompt**: (`STRING`) - Input for Random_Prompt mode
- **other_prompt**: (`STRING`) - Input for Other_Prompt mode

### Outputs

- **Main_Prompt**: (`STRING`) - Final processed prompt
- **filename**: (`STRING`) - Generated filename from prompt
- **subject**: (`STRING`) - Selected subject
- **scene**: (`STRING`) - Processed scene description

## Prompt Mode Controller

### Inputs

#### Required:
- **prompt_mode**: (`COMBO`) - Operation mode to control:
  - "Prompt_Manager_Prompt"
  - "Random_Prompt"
  - "Other_Prompt"

### Outputs

- **prompt_mode**: (`COMBO`) - Selected prompt mode for routing

### Important Note
When the Mode Controller is connected to a Prompt Manager, it will override the Prompt Manager's widget mode settings. This allows for dynamic control of prompt modes through node connections rather than widget settings.

## Features

- **Operation Modes**:
  - Subject-based prompting
  - Random prompt handling
  - Alternative prompt input
  - Dynamic subject cycling
  - Mode control and routing

- **Text Processing**:
  - Subject replacement
  - Weight application
  - Filename generation
  - Scene integration

- **UI Integration**:
  - Real-time updates
  - Visual feedback
  - Index tracking
  - State persistence

## Example Usage

Subject Mode:
```python
subject: """person
landscape
portrait"""
scene_description: "A detailed #sub in morning light"
subject_index_control: "increment"
# Cycles through subjects, replacing #sub in scene
```

Weight Application:
```python
prompt_mode: "Other_Prompt"
other_prompt: "detailed portrait"
weight: 1.2
# Returns: "(detailed portrait:1.2)"
```

Mode Control:
```python
# Mode Controller
prompt_mode: "Random_Prompt"
# Routes to random prompt processing
```

## Notes

- Maintains cycling state
- Handles empty inputs
- Automatic index wrapping
- Memory-efficient processing
- Real-time UI updates
- Error handling
- WebSocket integration 
