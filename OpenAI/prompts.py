def get_location_report_prompt(text: str) -> str:
    string = f"""
    Ми з України. У нас час від часу відбуваються обстріли. 
    Ось інформація по моєму місцю знаходження.

    {text}

    Проаналізуй обстановку, сформуй список бажаних дій для забезпечення безпеки.
    """

    return string
