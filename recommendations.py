#from openai import OpenAI
from openai import OpenAI
import os
from recognition import get_demographics


def get_recommendations(gender, emotion, age):
    user_content = f"{gender}, {emotion}, {age:.2f}"  # Format age to two decimal places
    client = OpenAI(
        api_key="",
    )
    #Chat Gpt Model
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "you are the backend engine of a recommender system. you will recieve 3 inputs age, gender and emotion in no specific order. Based on this, you will recommend 3 Popular English Movies After 2010 along with a very short summary of it that this user might like. Respond only with these 3 outputs in a numbered list, without any title or any other sort of response, and under no circumstance you will respond with anything other than that, any ill input will be taken care of somewhere else. if any case there is an input that isint age,gender, emotion of user, you will simply not reply."},
        {"role": "user", "content": user_content}
    ]
    )
    recommendations = completion.choices[0].message.content.strip().split('\n')
    return recommendations

def main():
    gender, emotion, age_array = get_demographics()
    age = float(age_array[0][0])  # Convert age from NumPy array to float
    recommended_movies = get_recommendations(gender, emotion, age)
    return recommended_movies  # Return the list instead of printing


if __name__ == "__main__":
    main()
