# Open AI API version
from fastapi import FastAPI
from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Load mock tasks


def load_tasks():
    with open("tasks.json") as f:
        return json.load(f)

# Create a prompt


def create_prompt(task):
    return f"""
You are a productivity assistant. Given the task below, generate a suggested plan of action with steps:

Task: {task['title']}
Description: {task['description']}

Plan:
"""

# Generate plan from OpenAI


def get_plan_from_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# API endpoint


@app.get("/generate-plans")
def generate_plans():
    tasks = load_tasks()
    results = []

    for task in tasks:
        prompt = create_prompt(task)
        plan = get_plan_from_gpt(prompt)
        results.append({
            "task_id": task["id"],
            "plan": plan
        })

    return {"plans": results}
