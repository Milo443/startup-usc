from openai import OpenAI
import streamlit as st

st.title('')
api='sk-proj-NwPjyAsrC99apVWcPmYRT3BlbkFJaS0s3UVEBKBF9GsIhJqZ'

client = OpenAI(api_key='sk-proj-veOu2ck5OwQ2qfGhUKZxT3BlbkFJkOpcFrMLhveZ0lO9fMEq')

completion = client.chat.completions.create(
  model="gpt-3.5-turbo", 
  messages=[
    {"role": "user", "content": "Can you tell me 5 countries in Latin America?"}
  ],
)

st.write(completion.choices[0].message.content)

