from evaluation.ground_truth import GROUND_TRUTH


def validate_ground_truth(dataset):

    total_entities = 0
    valid_entities = 0
    invalid_entities = 0

    print("===== Ground Truth Validation =====")

    for example_index, example in enumerate(dataset):

        text = example["text"]

        for entity_index, entity in enumerate(
            example["entities"]
        ):

            total_entities += 1

            value = entity["value"]
            start = entity["start"]
            end = entity["end"]

            extracted_value = text[start:end]

            if extracted_value == value:

                valid_entities += 1

            else:

                invalid_entities += 1

                print("\nINVALID ENTITY")

                print(
                    f"Example: {example_index}"
                )

                print(
                    f"Entity: {entity_index}"
                )

                print(
                    f"Expected value: {value!r}"
                )

                print(
                    f"start: {start}"
                )

                print(
                    f"end: {end}"
                )

                print(
                    f"Text span: {extracted_value!r}"
                )

                print(
                    f"Full text: {text!r}"
                )

    print("\n===== Summary =====")

    print(
        f"Total entities: {total_entities}"
    )

    print(
        f"Valid entities: {valid_entities}"
    )

    print(
        f"Invalid entities: {invalid_entities}"
    )


if __name__ == "__main__":

    validate_ground_truth(
        GROUND_TRUTH
    )