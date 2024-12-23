import logging
from typing import Dict, Any, Optional

# Set up a logger for this module.
logger = logging.getLogger('prompt')
logger.info("Prompt module initialized")


def create_prompt(style: str, character: str, situation: str, context: str,
                  character_profiles: Dict[str, Any], world_details: Dict[str, Any],
                  previous_attempt: str = None, feedback: Dict[str, Any] = None, style_prompt: str = None) -> str:
    """
    Create a detailed prompt with guidance and constraints, incorporating world details.

    Note: The prompt can become quite verbose. Consider strategies for condensing
    information or selectively including details based on relevance or token limits.
    """
    logger.debug("Creating prompt")
    prompt = []

    # Style
    if style_prompt:
        prompt.append(f"Write a chapter in the style described by: \"{
                      style_prompt}\"")
    else:
        prompt.append(f"Write a chapter in the style of {style}.")

    # Character
    if character:
        if character in character_profiles:
            profile = character_profiles[character]
            prompt.append(f"Focus on the character of {character}:")
            prompt.append(f"- Personality: {profile['personality']}")
            prompt.append(f"- Backstory: {profile['backstory']}")
            prompt.append(f"- Goal: {profile['goal']}")
        else:
            prompt.append(f"Focus on the character of {
                          character}, ensuring their actions and thoughts align with their established personality.")

    # Situation
    if situation:
        prompt.append(f"The situation involves: {situation}")

    # World Details - Themes
    if world_details and 'themes' in world_details:
        relevant_themes = world_details['themes']
        prompt.append("\nIncorporate the following themes:")
        for theme, details in relevant_themes.items():
            prompt.append(f"- {theme}: {', '.join(details['subthemes'])}")

    # World Details - Motifs
    if world_details and 'motifs' in world_details:
        relevant_motifs = world_details['motifs']
        prompt.append("\nUse the following motifs:")
        for motif, meaning in relevant_motifs.items():
            prompt.append(f"- {motif}: {meaning}")

    # World Details - Location (if situation provides a location)
    if situation and world_details:
        for location_name, location_details in world_details['locations'].items():
            if location_name.lower() in situation.lower():
                prompt.append(f"\nSetting details for {location_name}:")
                prompt.append(
                    f"- Description: {location_details['description']}")
                prompt.append(
                    f"- Significance: {location_details['significance']}")
                if 'places' in location_details:
                    prompt.append("- Notable places within this location:")
                    for place_name, place_description in location_details['places'].items():
                        prompt.append(
                            f"  - {place_name}: {place_description}")
                if 'rooms' in location_details:
                    prompt.append("- Rooms within this location:")
                    for room_name, room_description in location_details['rooms'].items():
                        prompt.append(
                            f"  - {room_name}: {room_description}")
                break  # Stop after finding the first relevant location

    # World Details - Styles (if not using style_prompt)
    if not style_prompt and world_details and 'styles' in world_details:
        style_details = world_details['styles'].get(style)
        if style_details:
            prompt.append(f"\nStyle guidelines for {style}:")
            prompt.append(f"{style_details}")

    # Previous Attempt and Feedback
    if previous_attempt and feedback:
        prompt.extend([
            "\nBased on the previous attempt, please improve:",
            f"- Overall narrative quality (previous quality score: {
                feedback.get('quality_score', 0):.2f})",
            f"- Narrative coherence (previous ROUGE-L: {
                feedback.get('rouge-l', 0):.2f})",
            f"- Lexical diversity (previous score: {
                feedback.get('lexical_diversity', 0):.2f})",
            f"- Semantic similarity to reference chunks (previous score: {
                feedback.get('semantic_similarity', 0):.2f})",
            "While maintaining the strong elements of the original."
        ])

    # Context (if available)
    if context:
        prompt.extend([
            "\nUse this context from existing materials:",
            context
        ])

    prompt.append(
        "\nGenerate a cohesive chapter that advances the story while maintaining consistency.")

    logger.info("Prompt created")
    return "\n".join(prompt)
