import json
import os
import argparse
from typing import Dict, Any, Tuple
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Load system prompts
with open("prompts.json", "r", encoding="utf-8") as f:
    PROMPTS = json.load(f)

# The list of allowed intents
ALLOWED_INTENTS = list(PROMPTS.keys()) + ["unclear"]

def classify_intent(message: str) -> dict:
    """
    Classifies the user message into an intent and confidence score.
    Returns: {"intent": "str", "confidence": float}
    """
    system_prompt = (
        "Your task is to classify the user's intent. Based on the user message below, "
        "choose one of the following labels: code, data, writing, career, unclear. "
        "Respond with a single JSON object containing two keys: 'intent' (the label you chose) "
        "and 'confidence' (a float from 0.0 to 1.0, representing your certainty). "
        "Do not provide any other text or explanation."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.0
        )
        content = response.choices[0].message.content
        result = json.loads(content)
        
        # Basic validation
        intent = result.get("intent", "unclear")
        confidence = float(result.get("confidence", 0.0))
        
        if intent not in ALLOWED_INTENTS:
            intent = "unclear"
            confidence = 0.0
            
        return {"intent": intent, "confidence": confidence}
        
    except Exception as e:
        # Fallback for malformed JSON or API errors
        return {"intent": "unclear", "confidence": 0.0}

def route_and_respond(message: str, intent_data: dict) -> str:
    """
    Routes the request based on the intent and generates a final response.
    """
    intent = intent_data.get("intent", "unclear")
    
    if intent == "unclear":
        return "I'm not exactly sure how to help. Are you asking for help with coding, data analysis, writing, or career advice?"
        
    system_prompt = PROMPTS.get(intent)
    if not system_prompt:
        return "I'm not exactly sure how to help. Are you asking for help with coding, data analysis, writing, or career advice?"
        
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while generating a response: {str(e)}"

def log_route(intent: str, confidence: float, user_message: str, final_response: str):
    """Logs the routing decision and final response to a JSON Lines file."""
    log_entry = {
        "intent": intent,
        "confidence": confidence,
        "user_message": user_message,
        "final_response": final_response
    }
    with open("route_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

def process_request(message: str) -> str:
    """End-to-end processing of a user request."""
    # Step 1: Classify intent
    intent_data = classify_intent(message)
    intent = intent_data.get("intent", "unclear")
    confidence = intent_data.get("confidence", 0.0)
    
    # Optional threshold stretch goal
    if confidence < 0.7:
        intent = "unclear"
        intent_data["intent"] = "unclear"
    
    # Step 2: Route and respond
    final_response = route_and_respond(message, intent_data)
    
    # Step 3: Log decision
    log_route(intent, confidence, message, final_response)
    
    return final_response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM-Powered Prompt Router")
    parser.add_argument("--message", type=str, help="The user message to process")
    args = parser.parse_args()
    
    if args.message:
        print(f"User: {args.message}")
        print("...")
        response = process_request(args.message)
        print(f"Assistant: {response}")
    else:
        print("Interactive mode (Type 'exit' to quit)")
        while True:
            try:
                user_msg = input("\nYou: ")
                if user_msg.lower() in ["exit", "quit"]:
                    break
                
                print("Processing...")
                response = process_request(user_msg)
                print(f"Assistant:\n{response}")
            except (KeyboardInterrupt, EOFError):
                break
