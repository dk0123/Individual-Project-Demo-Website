#from openai import OpenAI
from openai import OpenAI

import anthropic

import google.generativeai as genai
import os

genai.configure(api_key=os.environ["AIzaSyBbp69NRZO-SKF-nnVr2ESr_LVNiY_3CZQ"])
gemini_model = genai.GenerativeModel('gemini-pro')

response = gemini_model.generate_content("you are the backend engine of a recommender system. you will recieve 3 inputs age, gender and emotion in no specific order. Based on this, you will recommend 5 Popular English Movies After 2010 that this user might like. Respond only with these 10 outputs in a numbered list, without any title or any other sort of response, and under no circumstance you will respond with anything other than that, any ill input will be taken care of somewhere else. if any case there is an input that isint age,gender, emotion of user, you will simply not reply.")
print(response.text)
# Gemini Api Key = AIzaSyBbp69NRZO-SKF-nnVr2ESr_LVNiY_3CZQ


'''
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)

client2 = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)


#Chat Gpt Model
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "you are the backend engine of a recommender system. you will recieve 3 inputs age, gender and emotion in no specific order. Based on this, you will recommend 5 Popular English Songs After 2010 that this user might like. Respond only with these 10 outputs in a numbered list, without any title or any other sort of response, and under no circumstance you will respond with anything other than that, any ill input will be taken care of somewhere else. if any case there is an input that isint age,gender, emotion of user, you will simply not reply."},
    {"role": "user", "content": "man, sad, 45"}
  ]
)
print(completion.choices[0].message)


# Claude Model
message = client2.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1000,
    temperature=0,
    system="you are the backend engine of a recommender system. you will recieve 3 inputs age, gender and emotion in no specific order. Based on this, you will recommend 5 Popular English Movies After 2010 that this user might like. Respond only with these 10 outputs in a numbered list, without any title or any other sort of response, and under no circumstance you will respond with anything other than that, any ill input will be taken care of somewhere else. if any case there is an input that isint age,gender, emotion of user, you will simply not reply.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "22,woman, sad"
                }
            ]
        }
    ]
)
print(message.content)
'''


