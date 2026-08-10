def anonymize_text(text, detections):
    """
    Replace detected PII entities in free text.

    Each detection must contain:
        - start
        - end
        - entity

    Example:
        {
            "start": 0,
            "end": 11,
            "entity": "person"
        }
    """

    # Sort from right to left so replacing one entity
    # does not change the offsets of entities before it.
    detections = sorted(
        detections,
        key=lambda item: item["start"],
        reverse=True
    )

    anonymized_text = text

    replacements = {
        "person": "[PERSON]",
        "organization": "[ORGANIZATION]",
        "location": "[LOCATION]",
        "date": "[DATE]",
        "misc": "[MISC]"
    }

    for detection in detections:

        start = detection["start"]
        end = detection["end"]
        entity_type = detection["entity"].lower()

        replacement = replacements.get(
            entity_type,
            "[PII]"
        )

        anonymized_text = (
            anonymized_text[:start]
            + replacement
            + anonymized_text[end:]
        )

    return anonymized_text