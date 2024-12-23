# II. Deeper Character Profile Interaction

## **II. Deeper Character Profile Interaction**

* **A. Emotional State:**

    * **1. Predefined Emotion Options:**
        * **Concept:** Offer a list of common emotions for users to choose from.
        * **Implementation:**
            ```python
            from rich.prompt import Prompt

            def prompt_for_emotion(character_name: str):
                """Prompts the user to select the character's initial emotion."""
                emotion_options = [
                    "Angry",
                    "Anxious",
                    "Determined",
                    "Excited",
                    "Fearful",
                    "Hopeful",
                    "Melancholy",
                    "Neutral",
                    "Custom...",
                ]
                emotion = Prompt.ask(
                    f"[bold blue]How is {
                        character_name} feeling at the start of this chapter?",
                    choices=emotion_options,
                    default="Neutral",
                )
                if emotion == "Custom...":
                    emotion = Prompt.ask(
                        "[bold blue]Enter the character's emotion"
                    )
                return emotion

            # Example usage in generate_chapter_tui():
            if character:  # If a character is selected
                initial_emotion = prompt_for_emotion(character)
            ```
        * **Benefits:** Easy to use, provides a good starting point.
        * **Considerations:** The list might not cover all possible emotions.

    * **2. Free-Form Emotion Input:**
        * **Concept:** Allow users to type in any emotion.
        * **Implementation:**
            ```python
            # You can directly use a Prompt.ask() without pre-defined choices:
            emotion = Prompt.ask(
                f"[bold blue]How is {character_name} feeling (free-form)?"
            )
            ```
        * **Benefits:** More flexible, allows for nuanced emotions.
        * **Considerations:** Requires more processing to understand the input (see next point).

    * **3. Emotion Intensity:**
        * **Concept:** Add a way to specify the intensity of the chosen emotion (e.g., "Slightly," "Moderately," "Very").
        * **Implementation:**
            * After getting the emotion, add a follow-up prompt:
                ```python
                intensity = Prompt.ask(
                    "[bold blue]How intense is this emotion?",
                    choices=["Slightly", "Moderately", "Very", "Extremely"],
                    default="Moderately",
                )
                ```
            * Modify `create_prompt()` to incorporate intensity (e.g., "\[Character] is feeling very angry...").

    * **4. Emotion Processing:**
        * **Concept:** If using free-form input, you'll need to process the entered emotion to make it usable in the prompt.
        * **Implementation:**
            * **Simple Approach:** Use keyword matching (e.g., if the input contains "sad" or "down," consider it "Melancholy").
            * **Advanced Approach:** Use a sentiment analysis model or an emotion detection API to classify the emotion.
            * **Consider:** Store a mapping of common emotions to keywords to help with the simple approach.

* **B. Immediate Goals:**

    * **1. Goal Prompt:**
        * **Concept:** Ask the user what the character wants to achieve in this specific chapter.
        * **Implementation:**
            ```python
            from rich.prompt import Prompt

            def prompt_for_goal(character_name: str):
                """Prompts the user for the character's immediate goal."""
                goal = Prompt.ask(
                    f"[bold blue]What is {
                        character_name}'s immediate goal in this chapter?"
                )
                return goal

            # Example usage:
            if character:
                immediate_goal = prompt_for_goal(character)
            ```

    * **2. Goal Types (Optional):**
        * **Concept:** You could categorize goals (e.g., "Obtain an object," "Learn information," "Defeat an enemy," "Help someone") to provide more structure.
        * **Implementation:**
            * Offer a prompt with goal types first, then ask for the specific goal within that type.

    * **3. Relationship to Long-Term Goals:**
        * **Concept:** Consider how the immediate goal relates to the character's overall goal (from `character_profiles.json`).
        * **Implementation:**
            * In `create_prompt()`, you could add a sentence like: "This goal relates to their long-term desire to \[character's overall goal]."

* **C. Relationship Relevance:**

    * **1. Relationship Selection:**
        * **Concept:** Ask the user which of the character's relationships is most relevant to the current chapter.
        * **Implementation:**
            ```python
            from rich.prompt import Prompt

            def prompt_for_relevant_relationship(character_name: str, character_profiles):
                """Prompts the user to select the most relevant relationship."""
                if character_name not in character_profiles:
                    return None

                relationships = character_profiles[character_name].get(
                    "relationships", {}
                )
                if not relationships:
                    return None

                relationship_options = list(relationships.keys())
                relevant_relationship = Prompt.ask(
                    f"[bold blue]Which relationship is most important to {
                        character_name} in this chapter?",
                    choices=relationship_options + ["None"],
                    default="None",
                )
                return relevant_relationship

            # Example usage:
            if character:
                relevant_relationship = prompt_for_relevant_relationship(
                    character, character_profiles
                )
            ```

    * **2. Relationship Details in Prompt:**
        * **Concept:** Use the selected relationship and its description in the prompt.
        * **Implementation:**
            * In `create_prompt()`:
                ```python
                if relevant_relationship and relevant_relationship != "None":
                    relationship_desc = character_profiles[character][
                        "relationships"
                    ][relevant_relationship]
                    prompt.append(
                        f"Their relationship with {
                            relevant_relationship} ({relationship_desc}) is particularly important in this chapter."
                    )
                ```

**II. Relationship Dynamics in Focus**

* **A. Significant Interaction:**

    * **1. Interaction Partner Selection:**
        * **Concept:** Ask the user who the focus character will interact with the most.
        * **Implementation:**
            ```python
            from rich.prompt import Prompt

            def prompt_for_interaction_partner(
                character_name: str, character_profiles
            ):
                """Prompts the user to select a character for significant interaction."""
                # Exclude the focus character from the options
                other_characters = [
                    c
                    for c in character_profiles.keys()
                    if c.lower() != character_name.lower()
                ]
                if not other_characters:
                    return None

                interaction_partner = Prompt.ask(
                    f"[bold blue]Who will {
                        character_name} interact with significantly in this chapter (or None)?",
                    choices=other_characters + ["None"],
                    default="None",
                )
                return interaction_partner

            # Example usage:
            if character:
                interaction_partner = prompt_for_interaction_partner(
                    character, character_profiles
                )
            ```

    * **2. Retrieving Relationship Description:**
        * You're already doing this correctly in your example. Ensure you retrieve the description from `character_profiles.json` based on the selected interaction partner.

* **B. Current State of Relationship:**

    * **1. Relationship State Prompt:**
        * **Concept:** Ask the user to describe the *current* state of the relationship (e.g., "Tense," "Friendly," "Strained," "Supportive").
        * **Implementation:**
            ```python
            from rich.prompt import Prompt

            def prompt_for_relationship_state():
                """Prompts the user to describe the current state of the relationship."""
                relationship_state = Prompt.ask(
                    f"[bold blue]Describe the current state of their relationship (e.g., Tense, Supportive)"
                )
                return relationship_state

            # Example usage:
            if interaction_partner and interaction_partner != "None":
                relationship_state = prompt_for_relationship_state()
            ```

    * **2. Predefined Relationship States (Optional):**
        * **Concept:** Offer a list of common relationship states (like with emotions).
        * **Implementation:**
            * Provide choices in `prompt_for_relationship_state()`.

    * **3. Incorporating State into Prompt:**
        * **Concept:** Use the relationship state to influence the prompt.
        * **Implementation:**
            * In `create_prompt()`:
                ```python
                if interaction_partner and interaction_partner != "None":
                    relationship_desc = character_profiles[character][
                        "relationships"
                    ][interaction_partner]
                    prompt.append(
                        f"{character} will interact significantly with {
                            interaction_partner}. Their relationship is currently {relationship_state} ({relationship_desc})."
                    )
                ```

**III. Integrating into `create_prompt()`**

Here's how you might incorporate these elements into your `create_prompt()` function:

```python
def create_prompt(
    # ... other parameters
    initial_emotion: str = None,
    immediate_goal: str = None,
    relevant_relationship: str = None,
    interaction_partner: str = None,
    relationship_state: str = None,
    # ... other parameters
):
    # ... your existing prompt creation logic ...

    # --- Character Details ---
    if character:
        if character in character_profiles:
            # ... (your existing character profile handling)

            if initial_emotion:
                prompt.append(
                    f"{character} is feeling {initial_emotion} at the beginning of this chapter."
                )

            if immediate_goal:
                prompt.append(f"Their immediate goal in this chapter is to {immediate_goal}.")

            if relevant_relationship and relevant_relationship != "None":
                # ... (handle relevant relationship as shown above)

    # --- Relationship Dynamics ---
    if interaction_partner and interaction_partner != "None":
        # ... (handle interaction partner and relationship state as shown above)

    # ... rest of your prompt creation logic ...
```

**IV. Further Considerations**

* **Character Development:** Consider how these interactions might lead to changes in the character's long-term goals, personality, or relationships over time.
* **Relationship Arcs:** Think about how relationships evolve throughout the story. You could potentially add prompts to adjust relationship descriptions in `character_profiles.json` as the story progresses.
* **Memory:** You might want to store the character's emotional state, goals, and relationship states from previous chapters to maintain consistency.

---
