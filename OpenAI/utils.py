import asyncio

from openai import OpenAI


async def get_analysis_from_ai(text: str) -> None:
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content


async def main() -> None:
    client = OpenAI()

    string = f"""
    Ми з України. У нас час від часу відбуваються обстріли. 
    Ось інформація по моєму місцю знаходження.
    Проаналізуй обстановку, сформуй список бажаних дій для забезпечення безпеки.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "user", "content": string}
        ]
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())
