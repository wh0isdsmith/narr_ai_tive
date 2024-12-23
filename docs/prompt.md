# `prompt.py` Documentation

This module provides functionality for creating detailed prompts for story generation. It incorporates various elements such as style, character profiles, world details, and context to guide the story generation process.

## Functions

### `create_prompt(style: str, character: str, situation: str, context: str, character_profiles: Dict[str, Any], world_details: Dict[str, Any], previous_attempt: str = None, feedback: Dict[str, Any] = None, style_prompt: str = None) -> str`

This function creates a detailed prompt with guidance and constraints, incorporating world details and other relevant information.

#### Parameters

- `style` (str): The style of the story (e.g., "dark fantasy").
- `character` (str): The main character of the story.
- `situation` (str): The situation or setting of the story.
- `context` (str): Additional context to be included in the prompt.
- `character_profiles` (Dict[str, Any]): A dictionary containing character profiles.
- `world_details` (Dict[str, Any]): A dictionary containing world-building details.
- `previous_attempt` (str, optional): The previous attempt at generating the story, if any.
- `feedback` (Dict[str, Any], optional): Feedback on the previous attempt, if any.
- `style_prompt` (str, optional): A specific style prompt for the story.

#### Returns

- `str`: The generated prompt.

#### Usage

```python
prompt = create_prompt(
    style="dark fantasy",
    character="Sir Roland",
    situation="A dark forest at midnight",
    context="The forest is haunted by spirits.",
    character_profiles={
        "Sir Roland": {
            "personality": "Brave and noble",
            "backstory": "A knight on a quest to save the kingdom",
            "goal": "To defeat the evil sorcerer",
            "relationships": {
                "King Arthur": "His liege",
                "Lady Guinevere": "His love interest"
            },
            "age": 35
        }
    },
    world_details={
        "locations": {
            "Dark Forest": {
                "description": "A dense and eerie forest",
                "significance": "The site of many battles",
                "places": {
                    "Haunted Clearing": {
                        "description": "A clearing haunted by spirits"
                    }
                }
            }
        },
        "themes": {
            "Bravery": {
                "subthemes": ["Courage in the face of danger", "Overcoming fear"]
            }
        },
        "motifs": {
            "Darkness": "Symbolizes the unknown and fear",
            "Light": "Represents hope and guidance"
        }
    },
    previous_attempt="The knight entered the forest but was quickly lost.",
    feedback={
        "quality_score": 0.7,
        "rouge-l": 0.6,
        "lexical_diversity": 0.5,
        "semantic_similarity": 0.8
    },
    style_prompt="Write in a poetic and descriptive style."
)
```

#### Steps

1. **Style**: Adds the style or style prompt to the prompt.
2. **Character**: Adds character details to the prompt, including personality, backstory, goal, and relationships.
3. **Situation**: Adds the situation or setting to the prompt.
4. **World Details - Themes**: Adds relevant themes and subthemes to the prompt.
5. **World Details - Motifs**: Adds relevant motifs to the prompt.
6. **World Details - Location**: Adds location details to the prompt if the situation includes a location.
7. **World Details - Styles**: Adds style guidelines if not using a style prompt.
8. **Previous Attempt and Feedback**: Adds feedback on the previous attempt to guide improvements.
9. **Context**: Adds additional context to the prompt.
10. **Final Instructions**: Adds final instructions to generate a cohesive chapter.

#### Example

```python
from prompt import create_prompt

prompt = create_prompt(
    style="dark fantasy",
    character="Sir Roland",
    situation="A dark forest at midnight",
    context="The forest is haunted by spirits.",
    character_profiles={
        "Sir Roland": {
            "personality": "Brave and noble",
            "backstory": "A knight on a quest to save the kingdom",
            "goal": "To defeat the evil sorcerer",
            "relationships": {
                "King Arthur": "His liege",
                "Lady Guinevere": "His love interest"
            },
            "age": 35
        }
    },
    world_details={
        "locations": {
            "Dark Forest": {
                "description": "A dense and eerie forest",
                "significance": "The site of many battles",
                "places": {
                    "Haunted Clearing": {
                        "description": "A clearing haunted by spirits"
                    }
                }
            }
        },
        "themes": {
            "Bravery": {
                "subthemes": ["Courage in the face of danger", "Overcoming fear"]
            }
        },
        "motifs": {
            "Darkness": "Symbolizes the unknown and fear",
            "Light": "Represents hope and guidance"
        }
    },
    previous_attempt="The knight entered the forest but was quickly lost.",
    feedback={
        "quality_score": 0.7,
        "rouge-l": 0.6,
        "lexical_diversity": 0.5,
        "semantic_similarity": 0.8
    },
    style_prompt="Write in a poetic and descriptive style."
)
```

## Dependencies

- `logging`: For logging messages and errors.
- `typing`: For type hints.

## Example Usage

To use the `create_prompt` function, simply import it and call it in your script:

```python
from prompt import create_prompt

prompt = create_prompt(
    style="dark fantasy",
    character="Sir Roland",
    situation="A dark forest at midnight",
    context="The forest is haunted by spirits.",
    character_profiles={
        "Sir Roland": {
            "personality": "Brave and noble",
            "backstory": "A knight on a quest to save the kingdom",
            "goal": "To defeat the evil sorcerer",
            "relationships": {
                "King Arthur": "His liege",
                "Lady Guinevere": "His love interest"
            },
            "age": 35
        }
    },
    world_details={
        "locations": {
            "Dark Forest": {
                "description": "A dense and eerie forest",
                "significance": "The site of many battles",
                "places": {
                    "Haunted Clearing": {
                        "description": "A clearing haunted by spirits"
                    }
                }
            }
        },
        "themes": {
            "Bravery": {
                "subthemes": ["Courage in the face of danger", "Overcoming fear"]
            }
        },
        "motifs": {
            "Darkness": "Symbolizes the unknown and fear",
            "Light": "Represents hope and guidance"
        }
    },
    previous_attempt="The knight entered the forest but was quickly lost.",
    feedback={
        "quality_score": 0.7,
        "rouge-l": 0.6,
        "lexical_diversity": 0.5,
        "semantic_similarity": 0.8
    },
    style_prompt="Write in a poetic and descriptive style."
)
```

This will generate a detailed prompt incorporating the provided elements to guide the story generation process.

## Error Handling

The function includes error handling to catch and log any exceptions that occur during the prompt creation process. Errors are logged using the `logging` module.

## Conclusion

The `prompt.py` module provides a flexible and detailed approach to creating prompts for story generation. By incorporating various elements such as style, character profiles, world details, and context, it ensures that the generated story is cohesive and aligned with the desired narrative direction.
