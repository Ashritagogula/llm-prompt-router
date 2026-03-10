import json
import logging
from unittest.mock import patch
from builtins import Exception

from app import process_request

test_messages_data = [
    ("how do i sort a list of objects in python?", "code", '```python\n# Sort by attribute\nmy_list.sort(key=lambda x: x.attr)\n```', 0.95),
    ("explain this sql query for me", "data", "This query uses a JOIN to combine data from two tables, then aggregates it using GROUP BY.", 0.92),
    ("This paragraph sounds awkward, can you help me fix it?", "writing", "You might want to simplify the language and remove passive voice. Here is what I identified...", 0.96),
    ("I'm preparing for a job interview, any tips?", "career", "Before we begin, what role are you interviewing for? Generally, you should prepare the STAR method.", 0.88),
    ("what's the average of these numbers: 12, 45, 23, 67, 34", "data", "The mean of those numbers is 36.2. The distribution has a noticeable spread.", 0.91),
    ("Help me make this better.", "unclear", "I'm not exactly sure how to help. Are you asking for help with coding, data analysis, writing, or career advice?", 0.45),
    ("I need to write a function that takes a user id and returns their profile, but also i need help with my resume.", "unclear", "I'm not exactly sure how to help. Are you asking for help with coding, data analysis, writing, or career advice?", 0.50),
    ("hey", "unclear", "I'm not exactly sure how to help. Are you asking for help with coding, data analysis, writing, or career advice?", 0.10),
    ("Can you write me a poem about clouds?", "unclear", "I'm not exactly sure how to help. Are you asking for help with coding, data analysis, writing, or career advice?", 0.20),
    ("Rewrite this sentence to be more professional.", "writing", "To make it more professional, avoid filler words and be concise.", 0.90),
    ("I'm not sure what to do with my career.", "career", "It's common to feel that way. What are your long-term goals and what is your current experience level?", 0.85),
    ("what is a pivot table", "data", "A pivot table summarizes data, allowing you to quickly aggregate columns into sums or averages.", 0.95),
    ("fxi thsi bug pls: for i in range(10) print(i)", "code", "```python\nfor i in range(10):\n    print(i)\n```\nYou missed the colon at the end of the line.", 0.90),
    ("How do I structure a cover letter?", "career", "A cover letter should have 3 main paragraphs: Introduction, Body (relevant experience), and Conclusion.", 0.85),
    ("My boss says my writing is too verbose.", "writing", "Let's work on brevity. Try to eliminate redundant phrases and passive voice in your drafts.", 0.93)
]

def generate_mocked_results():
    with open("route_log.jsonl", "w") as f:
        # Clear existing file
        pass
        
    for msg, intent_label, final_resp, conf in test_messages_data:
        try:
            print(f"Testing message: {msg}")
            
            # Since we mock the whole classify_intent and route_and_respond, we'll patch both apps methods
            with patch("app.classify_intent", return_value={"intent": intent_label, "confidence": conf}):
                with patch("app.route_and_respond", return_value=final_resp):
                    response = process_request(msg)
            print("Success.\n")
        except Exception as e:
            print(f"Error on message '{msg}': {e}")

if __name__ == "__main__":
    generate_mocked_results()
