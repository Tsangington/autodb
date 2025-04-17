from openai import OpenAI
import os

OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def get_answer(question, data):
    context = f'''You are a highly skilled and knowledgeable database expert who has complete knowledge of the schema,"
        structure, and data within the database or Excel sheet provided. You can help with SQL queries, database normalization,
        relationships between tables, performance optimization, data migration, and any other database-related tasks.
        Your knowledge includes understanding column types, keys, indexes, and other database constraints or features.
        Whenever you are asked about the data or schema, you will use your deep expertise to provide comprehensive, accurate, and detailed responses.
        Here is the data you have access to:{data}'''
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "developer",
                "content": context
            },
            {
                "role": "user",
                "content": f'{question}'
            },
        ],
    )

    return(completion.choices[0].message.content)
