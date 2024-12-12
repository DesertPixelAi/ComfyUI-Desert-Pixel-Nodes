# Crazy Random Prompt Generator
<img src="https://github.com/user-attachments/assets/d5d970b6-0db3-4f02-9769-194807547d52" alt="DP_Crazy_Prompt" style="float: left; margin-right: 10px;"/>

The **Crazy Random Prompt Generator** creates unique and imaginative prompts by combining multiple carefully curated categories. Each generated prompt follows a structured format that combines the following elements:

## Prompt Structure

1. **Base Style** (Selected from styles.txt)
   - Determines the fundamental artistic approach
   - Examples: "chalk art", "ink art", "photorealism", "low poly"
   - Sets the primary visual style of the image

2. **Subject** (Selected from subject.txt)
   - The main focus or character of the image
   - Can be whimsical combinations like "a cyberpunk toaster with attitude"
   - Or complex scenarios like "a quantum physicist cat giving a TED talk"

3. **Composition** (Selected from composition.txt)
   - Defines how the scene is arranged and viewed
   - Includes perspectives like "extreme close-up with dramatic perspective"
   - Or unique viewpoints like "bird's eye view through a kaleidoscope"

4. **Lighting** (Selected from lighting.txt)
   - Specifies the lighting effects and mood
   - Examples: "volumetric godray light beams"
   - Or atmospheric effects like "crystalline prism light refraction"

5. **Color Palette** (Selected from color_palette.txt)
   - Defines the color scheme of the image
   - Ranges from vibrant like "neon cotton candy explosion"
   - To more subtle like "mystical fungal radiance"

6. **Atmosphere** (Selected from atmosphere.txt)
   - Sets the overall mood and feeling
   - Can be energetic like "chaotically euphoric"
   - Or mysterious like "interdimensionally confused"

7. **Technical Details** (Selected from technical_details.txt)
   - Adds specific rendering or processing effects
   - Examples: "rendered on a quantum abacus"
   - Or "processed through a rainbow machine"

8. **Additional Elements** (Selected from additional_elements.txt)
   - Extra details that enhance the scene
   - Like "floating in a sea of rubber ducks"
   - Or "surrounded by dancing mathematical equations"

9. **Style Combinations** (Multiple selections from styles.txt)
   - The number of additional styles depends on the "style_craziness" parameter:
     - Level 1: 3 additional styles
     - Level 2: 5 additional styles
     - Level 3: 7 additional styles
     - Level 4: 9 additional styles
     - Level 5: 15 additional styles

## Style Craziness Levels

The `style_craziness` parameter (1-5) controls how many additional styles are combined in the final prompt. Higher levels create more complex and eclectic combinations, while lower levels produce more focused results.

## Example Prompt Structure

```
[Base Style], [Subject], [Composition], [Lighting], [Color Palette], [Atmosphere], [Technical Details], [Additional Elements], in the style of [Style1, Style2, Style3, ...]
```

Example output:
```
chalk art, a cyberpunk toaster with attitude, extreme close-up with dramatic perspective, volumetric godray light beams, neon cotton candy explosion color palette, chaotically euphoric atmosphere, rendered on a quantum abacus, floating in a sea of rubber ducks, in the style of low poly, photorealism, ink art
```

## Customization Potential

Each category contains hundreds of unique options, allowing for millions of possible combinations. The generator ensures each prompt is unique by randomly selecting from these carefully curated lists while maintaining a coherent structure that can be interpreted by image generation systems.
