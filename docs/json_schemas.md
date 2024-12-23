# JSON Schemas for World-Building and Character Profiles

## Example Character and World Schemas

**Character Profile Schema** (`character_profiles.json`):

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CharacterProfile",
  "type": "object",
  "description": "Defines the structure for a character profile.",
  "properties": {
    "name": {
      "type": "string",
      "description": "The name of the character.",
      "example": "Elara"
    },
    "personality": {
      "type": "string",
      "description": "A brief description of the character's personality.",
      "example": "Brave, compassionate, but sometimes impulsive"
    },
    "backstory": {
      "type": "string",
      "description": "The character's backstory.",
      "example": "Orphaned at a young age, Elara discovered her magical abilities and trained in secret."
    },
    "goal": {
      "type": "string",
      "description": "The character's main goal or objective.",
      "example": "To master her powers and protect her homeland"
    },
    "relationships": {
      "type": "object",
      "description": "Relationships with other characters.",
      "additionalProperties": {
        "type": "string",
        "description": "The relationship description.",
        "example": {
          "mentor": "A wise old mage who guides Elara",
          "rival": "A jealous classmate vying for power"
        }
      }
    },
    "age": {
      "type": "integer",
      "description": "The age of the character.",
      "example": 18
    }
  },
  "required": [
    "name",
    "personality",
    "backstory",
    "goal",
    "relationships",
    "age"
  ]
}
```

**World Details Schema** (`world_details.json`):

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "WorldDetails",
  "type": "object",
  "description": "Defines the structure for world-building details.",
  "properties": {
    "locations": {
      "type": "object",
      "description": "A collection of locations in the story world.",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "description": {
            "type": "string",
            "description": "A brief description of the location.",
            "example": "A bustling port city known for its trade and seafaring"
          },
          "significance": {
            "type": "string",
            "description": "The significance of the location in the story.",
            "example": "The starting point of the protagonist's journey"
          },
          "places": {
            "type": "object",
            "description": "Specific places within the location.",
            "additionalProperties": {
              "type": "object",
              "properties": {
                "description": {
                  "type": "string",
                  "description": "A brief description of the place.",
                  "example": "The 'Salty Siren' tavern, a popular hangout for sailors"
                }
              },
              "required": ["description"]
            }
          },
          "rooms": {
            "type": "object",
            "description": "Specific rooms within a building (if applicable).",
            "additionalProperties": {
              "type": "object",
              "properties": {
                "description": {
                  "type": "string",
                  "description": "A brief description of the room.",
                  "example": "A secret chamber hidden behind a bookshelf"
                }
              },
              "required": ["description"]
            }
          }
        },
        "required": ["description", "significance"]
      }
    }
  },
  "required": ["locations"]
}
```

---