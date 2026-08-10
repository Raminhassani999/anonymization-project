from evaluation.ground_truth import GROUND_TRUTH


def validate_ground_truth(dataset):

    total_entities = 0
    valid_entities = 0
    invalid_entities = 0

    print("===== Ground Truth Validation =====")

    for example in dataset:

        text = example["text"]

        for entity in example["entities"]:

            total_entities += 1

            start = entity["start"]
            end = entity["end"]
            value = entity["value"]

            errors = []

            # Check that offsets are integers
            if not isinstance(start, int):
                errors.append(
                    "start is not an integer"
                )

            if not isinstance(end, int):
                errors.append(
                    "end is not an integer"
                )

            # Only perform range checks if the
            # values are valid integers
            if isinstance(start, int) and isinstance(end, int):

                if start < 0:
                    errors.append(
                        "start is negative"
                    )

                if end > len(text):
                    errors.append(
                        "end is beyond text length"
                    )

                if start >= end:
                    errors.append(
                        "start must be smaller than end"
                    )

                # Most important validation:
                # the span must actually contain
                # the annotated entity value.
                if (
                    0 <= start < end <= len(text)
                    and text[start:end] != value
                ):
                    errors.append(
                        "span does not match entity value"
                    )

            if errors:

                invalid_entities += 1

                print("\nINVALID ENTITY")

                print(
                    f"Text: {text}"
                )

                print(
                    f"Value: {value}"
                )

                print(
                    f"Entity type: "
                    f"{entity['entity']}"
                )

                print(
                    f"Start: {start}"
                )

                print(
                    f"End: {end}"
                )

                if (
                    isinstance(start, int)
                    and isinstance(end, int)
                    and 0 <= start <= end <= len(text)
                ):
                    print(
                        f"Actual text at span: "
                        f"{text[start:end]}"
                    )

                print(
                    "Errors:"
                )

                for error in errors:
                    print(
                        f"- {error}"
                    )

            else:

                valid_entities += 1

    print("\n===== Summary =====")

    print(
        f"Total entities: "
        f"{total_entities}"
    )

    print(
        f"Valid entities: "
        f"{valid_entities}"
    )

    print(
        f"Invalid entities: "
        f"{invalid_entities}"
    )


if __name__ == "__main__":

    validate_ground_truth(
        GROUND_TRUTH
    )