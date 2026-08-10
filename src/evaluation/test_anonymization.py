from anonymization.rule_based_anonymizer import (
    ANONYMIZATION_POLICY,
    anonymize_dataframe,
    patient_map,
    patient_counter,
)


def test_first_name_masking():
    data = {
        "First Name": ["Mario"]
    }

    import pandas as pd

    df = pd.DataFrame(data)

    detections = [
        {
            "row": 0,
            "column": "First Name"
        }
    ]

    result = anonymize_dataframe(df, detections)

    assert result.at[0, "First Name"] == "M****"


def test_surname_masking():
    import pandas as pd

    df = pd.DataFrame({
        "Surname": ["Rossi"]
    })

    detections = [
        {
            "row": 0,
            "column": "Surname"
        }
    ]

    result = anonymize_dataframe(df, detections)

    assert result.at[0, "Surname"] == "R****"


def test_patient_code_pseudonymization():
    import pandas as pd

    df = pd.DataFrame({
        "Patient Code": ["PAT123"]
    })

    detections = [
        {
            "row": 0,
            "column": "Patient Code"
        }
    ]

    result = anonymize_dataframe(df, detections)

    assert result.at[0, "Patient Code"] == "PATIENT_0001"


def test_patient_code_consistency():
    import pandas as pd

    df = pd.DataFrame({
        "Patient Code": [
            "PAT123",
            "PAT123"
        ]
    })

    detections = [
        {
            "row": 0,
            "column": "Patient Code"
        },
        {
            "row": 1,
            "column": "Patient Code"
        }
    ]

    result = anonymize_dataframe(df, detections)

    assert result.at[0, "Patient Code"] == "PATIENT_0001"
    assert result.at[1, "Patient Code"] == "PATIENT_0001"


def test_tax_code_masking():
    import pandas as pd

    df = pd.DataFrame({
        "Tax Code": ["ABCDEF12345"]
    })

    detections = [
        {
            "row": 0,
            "column": "Tax Code"
        }
    ]

    result = anonymize_dataframe(df, detections)

    assert result.at[0, "Tax Code"] == "ABC******45"


def test_birth_date_generalization():
    import pandas as pd

    df = pd.DataFrame({
        "Birth Date": ["15/03/2024"]
    })

    detections = [
        {
            "row": 0,
            "column": "Birth Date"
        }
    ]

    result = anonymize_dataframe(df, detections)

    assert result.at[0, "Birth Date"] == "2024"


def test_assessment_date_generalization():
    import pandas as pd

    df = pd.DataFrame({
        "Assessment Date": ["2024-06-20"]
    })

    detections = [
        {
            "row": 0,
            "column": "Assessment Date"
        }
    ]

    result = anonymize_dataframe(df, detections)

    assert result.at[0, "Assessment Date"] == "2024"


def test_age_generalization():
    import pandas as pd

    df = pd.DataFrame({
        "Age At Assessment": ["37"]
    })

    detections = [
        {
            "row": 0,
            "column": "Age At Assessment"
        }
    ]

    result = anonymize_dataframe(df, detections)

    assert result.at[0, "Age At Assessment"] == "30-39"


def test_non_detected_values_are_preserved():
    import pandas as pd

    df = pd.DataFrame({
        "First Name": ["Mario"],
        "Surname": ["Rossi"]
    })

    detections = [
        {
            "row": 0,
            "column": "First Name"
        }
    ]

    result = anonymize_dataframe(df, detections)

    assert result.at[0, "First Name"] == "M****"
    assert result.at[0, "Surname"] == "Rossi"


def run_tests():
    tests = [
        test_first_name_masking,
        test_surname_masking,
        test_patient_code_pseudonymization,
        test_patient_code_consistency,
        test_tax_code_masking,
        test_birth_date_generalization,
        test_assessment_date_generalization,
        test_age_generalization,
        test_non_detected_values_are_preserved,
    ]

    passed = 0
    failed = 0

    for test in tests:

        try:
            test()
            print(f"PASS: {test.__name__}")
            passed += 1

        except AssertionError:
            print(f"FAIL: {test.__name__}")
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