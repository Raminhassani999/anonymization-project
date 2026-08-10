from anonymization.text_anonymizer import anonymize_text


def test_person_anonymization():

    text = "Mario Rossi visited Rome."

    detections = [
        {
            "start": 0,
            "end": 11,
            "entity": "person"
        }
    ]

    result = anonymize_text(
        text,
        detections
    )

    assert result == "[PERSON] visited Rome."


def test_multiple_entities():

    text = "Mario Rossi visited Rome."

    detections = [
        {
            "start": 0,
            "end": 11,
            "entity": "person"
        },
        {
            "start": 20,
            "end": 24,
            "entity": "location"
        }
    ]

    result = anonymize_text(
        text,
        detections
    )

    assert result == "[PERSON] visited [LOCATION]."


def test_date_anonymization():

    text = "Mario Rossi was admitted on 15 March 2024."

    detections = [
        {
            "start": 0,
            "end": 11,
            "entity": "person"
        },
        {
            "start": 28,
            "end": 41,
            "entity": "date"
        }
    ]

    result = anonymize_text(
        text,
        detections
    )

    assert result == "[PERSON] was admitted on [DATE]."


def test_organization_anonymization():

    text = "Luigi Bianchi works for Microsoft."

    detections = [
        {
            "start": 0,
            "end": 13,
            "entity": "person"
        },
        {
            "start": 24,
            "end": 33,
            "entity": "organization"
        }
    ]

    result = anonymize_text(
        text,
        detections
    )

    assert result == "[PERSON] works for [ORGANIZATION]."


def test_non_pii_text_is_preserved():

    text = "Mario Rossi visited Rome yesterday."

    detections = [
        {
            "start": 0,
            "end": 11,
            "entity": "person"
        }
    ]

    result = anonymize_text(
        text,
        detections
    )

    assert result == "[PERSON] visited Rome yesterday."


def run_tests():

    tests = [
        test_person_anonymization,
        test_multiple_entities,
        test_date_anonymization,
        test_organization_anonymization,
        test_non_pii_text_is_preserved
    ]

    passed = 0
    failed = 0

    for test in tests:

        try:
            test()

            print(
                f"PASS: {test.__name__}"
            )

            passed += 1

        except AssertionError:

            print(
                f"FAIL: {test.__name__}"
            )

            failed += 1

        except Exception as error:

            print(
                f"ERROR: {test.__name__} -> {error}"
            )

            failed += 1

    print("\n===== Summary =====")
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    run_tests()