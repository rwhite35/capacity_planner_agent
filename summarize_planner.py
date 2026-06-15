import os
import anthropic
from pathlib import Path

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def summarize_capacity_reports(*plans):
    contents = []
    for path in plans:
         with open(path) as f:
            contents.append(f"File: {path}\n{f.read()}")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"Summarize these disk capacity reports:\n\n{'---'.join(contents)}"
        }]
    )
    return response.content[0].text

cwd = Path.cwd()
print(summarize_capacity_reports(
    cwd / "../vmproj1/capacity/planner.txt", 
    cwd / "../vmproj2/capacity/planner.txt")
    )
