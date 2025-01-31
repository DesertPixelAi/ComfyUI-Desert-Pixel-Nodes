# DP Random Character

<img src="https://github.com/user-attachments/assets/414bfb42-9cef-4aed-afa4-7938449ae6e8" alt="DP_Random_Char" style="float: left; margin-right: 10px;"/>

## Description

A utility node for generating random character strings. Features intelligent character selection that avoids similar-looking characters and recent repetitions, making it ideal for creating readable random strings and passwords.

## Inputs

- `Type`: Character set selection
  - `random_letter`: Letters only (a-z)
  - `random_number`: Numbers only (0-9)
  - `random_mixed`: Both letters and numbers

- `Case`: Letter case options
  - `lowercase`: All lowercase
  - `uppercase`: All uppercase
  - `mixed`: Random mix of upper and lowercase

- `Num_Chars`: Number of characters to generate (1-20)

## Outputs

- `Characters`: Generated string of random characters

## Features

- Avoids similar-looking characters (e.g., 'i', 'l', '1')
- Prevents recent character repetitions
- Maintains character history to ensure variety
- Automatically resets if available characters are exhausted

## Example Usage

For Passwords:
```
Type: random_mixed
Case: mixed
Num_Chars: 12
```

For Serial Numbers:
```
Type: random_number
Case: uppercase
Num_Chars: 8
```

For Random IDs:
```
Type: random_letter
Case: lowercase
Num_Chars: 6
```

Note: Each run generates a new random string, perfect for batch operations requiring unique identifiers. 
