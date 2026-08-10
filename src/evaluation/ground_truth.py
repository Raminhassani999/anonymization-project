import re


def entity(text, value, entity_type, occurrence=1):

    pattern = re.compile(
        rf"(?<!\w){re.escape(value)}(?!\w)"
    )

    matches = list(
        pattern.finditer(text)
    )

    if not matches:
        raise ValueError(
            f"Entity '{value}' not found as a "
            f"whole-word match in: {text}"
        )

    if occurrence > len(matches):
        raise ValueError(
            f"Occurrence {occurrence} of '{value}' "
            f"does not exist in: {text}"
        )

    match = matches[occurrence - 1]

    return {
        "start": match.start(),
        "end": match.end(),
        "value": value,
        "entity": entity_type
    }


GROUND_TRUTH = [

    {
        "text": "Mario Rossi visited Rome.",
        "type": "free_text",
        "entities": [
            entity(
                "Mario Rossi visited Rome.",
                "Mario Rossi",
                "person"
            ),
            entity(
                "Mario Rossi visited Rome.",
                "Rome",
                "location"
            )
        ]
    },

    {
        "text": "Luigi Bianchi works for Microsoft.",
        "type": "free_text",
        "entities": [
            entity(
                "Luigi Bianchi works for Microsoft.",
                "Luigi Bianchi",
                "person"
            ),
            entity(
                "Luigi Bianchi works for Microsoft.",
                "Microsoft",
                "organization"
            )
        ]
    },

    {
        "text": "Giulia Ferraro lives in Milan.",
        "type": "free_text",
        "entities": [
            entity(
                "Giulia Ferraro lives in Milan.",
                "Giulia Ferraro",
                "person"
            ),
            entity(
                "Giulia Ferraro lives in Milan.",
                "Milan",
                "location"
            )
        ]
    },

    {
        "text": "Andrea Conti moved to London.",
        "type": "free_text",
        "entities": [
            entity(
                "Andrea Conti moved to London.",
                "Andrea Conti",
                "person"
            ),
            entity(
                "Andrea Conti moved to London.",
                "London",
                "location"
            )
        ]
    },

    {
        "text": "Marco Bianchi vive a Messina.",
        "type": "free_text",
        "entities": [
            entity(
                "Marco Bianchi vive a Messina.",
                "Marco Bianchi",
                "person"
            ),
            entity(
                "Marco Bianchi vive a Messina.",
                "Messina",
                "location"
            )
        ]
    },

    {
        "text": "Francesca Romano lavora a Roma.",
        "type": "free_text",
        "entities": [
            entity(
                "Francesca Romano lavora a Roma.",
                "Francesca Romano",
                "person"
            ),
            entity(
                "Francesca Romano lavora a Roma.",
                "Roma",
                "location"
            )
        ]
    },

    {
        "text": "Luca Ferrari è stato ricoverato a Milano.",
        "type": "free_text",
        "entities": [
            entity(
                "Luca Ferrari è stato ricoverato a Milano.",
                "Luca Ferrari",
                "person"
            ),
            entity(
                "Luca Ferrari è stato ricoverato a Milano.",
                "Milano",
                "location"
            )
        ]
    },

    {
        "text": "Anna Esposito vive in Italia.",
        "type": "free_text",
        "entities": [
            entity(
                "Anna Esposito vive in Italia.",
                "Anna Esposito",
                "person"
            ),
            entity(
                "Anna Esposito vive in Italia.",
                "Italia",
                "location"
            )
        ]
    },

    {
        "text": "Mario Rossi visited Policlinico di Messina.",
        "type": "free_text",
        "entities": [
            entity(
                "Mario Rossi visited Policlinico di Messina.",
                "Mario Rossi",
                "person"
            ),
            entity(
                "Mario Rossi visited Policlinico di Messina.",
                "Policlinico di Messina",
                "organization"
            )
        ]
    },

    {
        "text": "Luigi Bianchi works at Microsoft in Rome.",
        "type": "free_text",
        "entities": [
            entity(
                "Luigi Bianchi works at Microsoft in Rome.",
                "Luigi Bianchi",
                "person"
            ),
            entity(
                "Luigi Bianchi works at Microsoft in Rome.",
                "Microsoft",
                "organization"
            ),
            entity(
                "Luigi Bianchi works at Microsoft in Rome.",
                "Rome",
                "location"
            )
        ]
    },

    {
        "text": "Francesca Romano studies at the University of Messina.",
        "type": "free_text",
        "entities": [
            entity(
                "Francesca Romano studies at the University of Messina.",
                "Francesca Romano",
                "person"
            ),
            entity(
                "Francesca Romano studies at the University of Messina.",
                "University of Messina",
                "organization"
            ),
            entity(
                "Francesca Romano studies at the University of Messina.",
                "Messina",
                "location"
            )
        ]
    },

    {
        "text": "Mario Rossi was admitted on 15 March 2024.",
        "type": "free_text",
        "entities": [
            entity(
                "Mario Rossi was admitted on 15 March 2024.",
                "Mario Rossi",
                "person"
            ),
            entity(
                "Mario Rossi was admitted on 15 March 2024.",
                "15 March 2024",
                "date"
            )
        ]
    },

    {
        "text": "The appointment was scheduled for 2024-06-20.",
        "type": "free_text",
        "entities": [
            entity(
                "The appointment was scheduled for 2024-06-20.",
                "2024-06-20",
                "date"
            )
        ]
    },

    {
        "text": "Luigi Bianchi visited Rome on 12/05/2023.",
        "type": "free_text",
        "entities": [
            entity(
                "Luigi Bianchi visited Rome on 12/05/2023.",
                "Luigi Bianchi",
                "person"
            ),
            entity(
                "Luigi Bianchi visited Rome on 12/05/2023.",
                "Rome",
                "location"
            ),
            entity(
                "Luigi Bianchi visited Rome on 12/05/2023.",
                "12/05/2023",
                "date"
            )
        ]
    },

    {
        "text": "Il paziente Marco Bianchi è stato visitato al Policlinico di Messina il 15 marzo 2024.",
        "type": "free_text",
        "entities": [
            entity(
                "Il paziente Marco Bianchi è stato visitato al Policlinico di Messina il 15 marzo 2024.",
                "Marco Bianchi",
                "person"
            ),
            entity(
                "Il paziente Marco Bianchi è stato visitato al Policlinico di Messina il 15 marzo 2024.",
                "Policlinico di Messina",
                "organization"
            ),
            entity(
                "Il paziente Marco Bianchi è stato visitato al Policlinico di Messina il 15 marzo 2024.",
                "15 marzo 2024",
                "date"
            )
        ]
    },

    {
        "text": "Anna Esposito ha incontrato il dottor Luca Ferrari a Roma.",
        "type": "free_text",
        "entities": [
            entity(
                "Anna Esposito ha incontrato il dottor Luca Ferrari a Roma.",
                "Anna Esposito",
                "person"
            ),
            entity(
                "Anna Esposito ha incontrato il dottor Luca Ferrari a Roma.",
                "Luca Ferrari",
                "person"
            ),
            entity(
                "Anna Esposito ha incontrato il dottor Luca Ferrari a Roma.",
                "Roma",
                "location"
            )
        ]
    },

    {
        "text": "Mario Rossi and Luigi Bianchi travelled from Rome to Milan.",
        "type": "free_text",
        "entities": [
            entity(
                "Mario Rossi and Luigi Bianchi travelled from Rome to Milan.",
                "Mario Rossi",
                "person"
            ),
            entity(
                "Mario Rossi and Luigi Bianchi travelled from Rome to Milan.",
                "Luigi Bianchi",
                "person"
            ),
            entity(
                "Mario Rossi and Luigi Bianchi travelled from Rome to Milan.",
                "Rome",
                "location"
            ),
            entity(
                "Mario Rossi and Luigi Bianchi travelled from Rome to Milan.",
                "Milan",
                "location"
            )
    ]
},

{
        "text": "Giulia Ferraro met Andrea Conti in London.",
        "type": "free_text",
        "entities": [
            entity(
                "Giulia Ferraro met Andrea Conti in London.",
                "Giulia Ferraro",
                "person"
            ),
            entity(
                "Giulia Ferraro met Andrea Conti in London.",
                "Andrea Conti",
                "person"
            ),
            entity(
                "Giulia Ferraro met Andrea Conti in London.",
                "London",
                "location"
            )
        ]
    },
    {
    "text": "Name: Mario Rossi | City: Rome | Birth Date: 15 March 1985",
    "type": "structured",
    "entities": [
        entity(
            "Name: Mario Rossi | City: Rome | Birth Date: 15 March 1985",
            "Mario Rossi",
            "person"
        ),
        entity(
            "Name: Mario Rossi | City: Rome | Birth Date: 15 March 1985",
            "Rome",
            "location"
        ),
        entity(
            "Name: Mario Rossi | City: Rome | Birth Date: 15 March 1985",
            "15 March 1985",
            "date"
        )
    ]
},

{
    "text": "Patient: Luigi Bianchi | Hospital: Policlinico di Messina | City: Messina",
    "type": "structured",
    "entities": [
        entity(
            "Patient: Luigi Bianchi | Hospital: Policlinico di Messina | City: Messina",
            "Luigi Bianchi",
            "person"
        ),
        entity(
            "Patient: Luigi Bianchi | Hospital: Policlinico di Messina | City: Messina",
            "Policlinico di Messina",
            "organization"
        ),
        entity(
            "Patient: Luigi Bianchi | Hospital: Policlinico di Messina | City: Messina",
            "Messina",
            "location"
        )
    ]
},

{
    "text": "Full Name: Giulia Ferraro | Organization: Microsoft | Location: Milan",
    "type": "structured",
    "entities": [
        entity(
            "Full Name: Giulia Ferraro | Organization: Microsoft | Location: Milan",
            "Giulia Ferraro",
            "person"
        ),
        entity(
            "Full Name: Giulia Ferraro | Organization: Microsoft | Location: Milan",
            "Microsoft",
            "organization"
        ),
        entity(
            "Full Name: Giulia Ferraro | Organization: Microsoft | Location: Milan",
            "Milan",
            "location"
        )
    ]
},

{
    "text": "Patient Name: Marco Bianchi | Hospital: Policlinico di Messina | Admission Date: 15 March 2024",
    "type": "structured",
    "entities": [
        entity(
            "Patient Name: Marco Bianchi | Hospital: Policlinico di Messina | Admission Date: 15 March 2024",
            "Marco Bianchi",
            "person"
        ),
        entity(
            "Patient Name: Marco Bianchi | Hospital: Policlinico di Messina | Admission Date: 15 March 2024",
            "Policlinico di Messina",
            "organization"
        ),
        entity(
            "Patient Name: Marco Bianchi | Hospital: Policlinico di Messina | Admission Date: 15 March 2024",
            "15 March 2024",
            "date"
        )
    ]
},

{
    "text": "Name: Francesca Romano | City: Roma | Employer: University of Messina",
    "type": "structured",
    "entities": [
        entity(
            "Name: Francesca Romano | City: Roma | Employer: University of Messina",
            "Francesca Romano",
            "person"
        ),
        entity(
            "Name: Francesca Romano | City: Roma | Employer: University of Messina",
            "Roma",
            "location"
        ),
        entity(
            "Name: Francesca Romano | City: Roma | Employer: University of Messina",
            "University of Messina",
            "organization"
        )
    ]
},

{
    "text": "Name: Anna Esposito | Location: London | Appointment Date: 2024-06-20",
    "type": "structured",
    "entities": [
        entity(
            "Name: Anna Esposito | Location: London | Appointment Date: 2024-06-20",
            "Anna Esposito",
            "person"
        ),
        entity(
            "Name: Anna Esposito | Location: London | Appointment Date: 2024-06-20",
            "London",
            "location"
        ),
        entity(
            "Name: Anna Esposito | Location: London | Appointment Date: 2024-06-20",
            "2024-06-20",
            "date"
        )
    ]
},
{
    "text": "Name: Luca Ferrari | City: Milano | Employer: Microsoft",
    "type": "structured",
    "entities": [
        entity(
            "Name: Luca Ferrari | City: Milano | Employer: Microsoft",
            "Luca Ferrari",
            "person"
        ),
        entity(
            "Name: Luca Ferrari | City: Milano | Employer: Microsoft",
            "Milano",
            "location"
        ),
        entity(
            "Name: Luca Ferrari | City: Milano | Employer: Microsoft",
            "Microsoft",
            "organization"
        )
    ]
},

{
    "text": "Patient: Anna Esposito | Hospital: Policlinico di Messina | Date: 12/05/2023",
    "type": "structured",
    "entities": [
        entity(
            "Patient: Anna Esposito | Hospital: Policlinico di Messina | Date: 12/05/2023",
            "Anna Esposito",
            "person"
        ),
        entity(
            "Patient: Anna Esposito | Hospital: Policlinico di Messina | Date: 12/05/2023",
            "Policlinico di Messina",
            "organization"
        ),
        entity(
            "Patient: Anna Esposito | Hospital: Policlinico di Messina | Date: 12/05/2023",
            "12/05/2023",
            "date"
        )
    ]
},

{
    "text": "Full Name: Andrea Conti | Location: London | Company: Microsoft",
    "type": "structured",
    "entities": [
        entity(
            "Full Name: Andrea Conti | Location: London | Company: Microsoft",
            "Andrea Conti",
            "person"
        ),
        entity(
            "Full Name: Andrea Conti | Location: London | Company: Microsoft",
            "London",
            "location"
        ),
        entity(
            "Full Name: Andrea Conti | Location: London | Company: Microsoft",
            "Microsoft",
            "organization"
        )
    ]
},

{
    "text": "Patient Name: Marco Bianchi | City: Messina | Admission Date: 15 marzo 2024",
    "type": "structured",
    "entities": [
        entity(
            "Patient Name: Marco Bianchi | City: Messina | Admission Date: 15 marzo 2024",
            "Marco Bianchi",
            "person"
        ),
        entity(
            "Patient Name: Marco Bianchi | City: Messina | Admission Date: 15 marzo 2024",
            "Messina",
            "location"
        ),
        entity(
            "Patient Name: Marco Bianchi | City: Messina | Admission Date: 15 marzo 2024",
            "15 marzo 2024",
            "date"
        )
    ]
},

{
    "text": "Name: Francesca Romano | Location: Roma | Organization: University of Messina",
    "type": "structured",
    "entities": [
        entity(
            "Name: Francesca Romano | Location: Roma | Organization: University of Messina",
            "Francesca Romano",
            "person"
        ),
        entity(
            "Name: Francesca Romano | Location: Roma | Organization: University of Messina",
            "Roma",
            "location"
        ),
        entity(
            "Name: Francesca Romano | Location: Roma | Organization: University of Messina",
            "University of Messina",
            "organization"
        )
    ]
},

{
    "text": "Name: Luigi Bianchi | Location: Rome | Appointment Date: 2024-06-20",
    "type": "structured",
    "entities": [
        entity(
            "Name: Luigi Bianchi | Location: Rome | Appointment Date: 2024-06-20",
            "Luigi Bianchi",
            "person"
        ),
        entity(
            "Name: Luigi Bianchi | Location: Rome | Appointment Date: 2024-06-20",
            "Rome",
            "location"
        ),
        entity(
            "Name: Luigi Bianchi | Location: Rome | Appointment Date: 2024-06-20",
            "2024-06-20",
            "date"
        )
    ]
},

{
    "text": "Name: Giulia Ferraro | City: Milan | Birth Date: 20 June 1998",
    "type": "structured",
    "entities": [
        entity(
            "Name: Giulia Ferraro | City: Milan | Birth Date: 20 June 1998",
            "Giulia Ferraro",
            "person"
        ),
        entity(
            "Name: Giulia Ferraro | City: Milan | Birth Date: 20 June 1998",
            "Milan",
            "location"
        ),
        entity(
            "Name: Giulia Ferraro | City: Milan | Birth Date: 20 June 1998",
            "20 June 1998",
            "date"
        )
    ]
},

{
    "text": "Patient: Luca Ferrari | Clinic: Policlinico di Messina | City: Messina",
    "type": "structured",
    "entities": [
        entity(
            "Patient: Luca Ferrari | Clinic: Policlinico di Messina | City: Messina",
            "Luca Ferrari",
            "person"
        ),
        entity(
            "Patient: Luca Ferrari | Clinic: Policlinico di Messina | City: Messina",
            "Policlinico di Messina",
            "organization"
        ),
        entity(
            "Patient: Luca Ferrari | Clinic: Policlinico di Messina | City: Messina",
            "Messina",
            "location"
        )
    ]
},

{
    "text": "Name: Mario Rossi | Employer: Microsoft | Country: Italy",
    "type": "structured",
    "entities": [
        entity(
            "Name: Mario Rossi | Employer: Microsoft | Country: Italy",
            "Mario Rossi",
            "person"
        ),
        entity(
            "Name: Mario Rossi | Employer: Microsoft | Country: Italy",
            "Microsoft",
            "organization"
        ),
        entity(
            "Name: Mario Rossi | Employer: Microsoft | Country: Italy",
            "Italy",
            "location"
        )
    ]
},

{
    "text": "Patient: Francesca Romano | Hospital: University of Messina | Date: 15 March 2024",
    "type": "structured",
    "entities": [
        entity(
            "Patient: Francesca Romano | Hospital: University of Messina | Date: 15 March 2024",
            "Francesca Romano",
            "person"
        ),
        entity(
            "Patient: Francesca Romano | Hospital: University of Messina | Date: 15 March 2024",
            "University of Messina",
            "organization"
        ),
        entity(
            "Patient: Francesca Romano | Hospital: University of Messina | Date: 15 March 2024",
            "15 March 2024",
            "date"
        )
    ]
},

{
    "text": "Name: Andrea Conti | City: London | Date: 2024-06-20",
    "type": "structured",
    "entities": [
        entity(
            "Name: Andrea Conti | City: London | Date: 2024-06-20",
            "Andrea Conti",
            "person"
        ),
        entity(
            "Name: Andrea Conti | City: London | Date: 2024-06-20",
            "London",
            "location"
        ),
        entity(
            "Name: Andrea Conti | City: London | Date: 2024-06-20",
            "2024-06-20",
            "date"
        )
    ]
},

{
    "text": "Name: Anna Esposito | Organization: Microsoft | Location: Roma",
    "type": "structured",
    "entities": [
        entity(
            "Name: Anna Esposito | Organization: Microsoft | Location: Roma",
            "Anna Esposito",
            "person"
        ),
        entity(
            "Name: Anna Esposito | Organization: Microsoft | Location: Roma",
            "Microsoft",
            "organization"
        ),
        entity(
            "Name: Anna Esposito | Organization: Microsoft | Location: Roma",
            "Roma",
            "location"
        )
    ]
},



]