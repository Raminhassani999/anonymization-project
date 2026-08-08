def entity(text, value, entity_type):
    start = text.index(value)
    end = start + len(value)

    return {
        "start": start,
        "end": end,
        "value": value,
        "entity": entity_type
    }


GROUND_TRUTH = [

    {
        "text": "Mario Rossi visited Rome.",
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
    }
]