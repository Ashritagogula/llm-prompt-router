# AI Prompt Router Service

## Overview

This project implements an **intent-based AI prompt routing system** that intelligently directs user queries to specialized AI personas. Instead of using a single large prompt to handle every task, the system first **classifies the user's intent** and then routes the request to an appropriate **expert prompt** designed for that specific task.

This architecture improves response quality, reduces prompt complexity, and mimics how modern production AI systems are built.

The service follows a **two-step pipeline**:

1. **Intent Classification** – A lightweight LLM call determines the user’s intent.
2. **Expert Response Generation** – The system routes the request to a specialized AI persona to produce the final response.

---

## Key Features

* Intent-based prompt routing
* Multiple specialized AI personas
* Structured JSON output from the classifier
* Fault-tolerant JSON parsing
* Logging of all routing decisions
* Support for ambiguous queries through clarification prompts
* Configurable prompt definitions

---

## System Architecture

```text
User Message
     │
     ▼
Intent Classifier (LLM)
     │
     ▼
Intent + Confidence
     │
     ▼
Routing Layer
 ├── Code Expert
 ├── Data Analyst
 ├── Writing Coach
 ├── Career Advisor
 └── Clarification Handler
     │
     ▼
Final LLM Response
     │
     ▼
User + Log Entry
```

---

## Project Structure

```text
ai-prompt-router/
│
├── app.py
├── test_15_phrases.py
├── test_requirements.py
├── prompts.json
├── route_log.jsonl
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### File Descriptions

| File               | Purpose                          |
| ------------------ | -------------------------------- |
| `app.py`           | Implements `classify_intent()`, `route_and_respond()`, and logging |
| `prompts.json`     | Stores all expert system prompts |
| `test_15_phrases.py` | Validates routing behavior with 15 test phrases |
| `test_requirements.py` | Validates project structural requirements |
| `route_log.jsonl`  | Stores routing logs              |
| `requirements.txt` | Project Python dependencies      |
| `Dockerfile` & `docker-compose.yml` | Containerization routing and dependencies |

---

# Expert Personas

The system uses specialized prompts for different domains.

### Code Expert

Provides **production-quality code solutions** with explanations and error handling.

### Data Analyst

Interprets datasets using **statistical reasoning and visualization suggestions**.

### Writing Coach

Helps users improve writing by identifying **clarity, tone, and structural issues**.

### Career Advisor

Offers **actionable career guidance** and asks clarifying questions about goals.

### Unclear Intent Handler

When intent is ambiguous, the system asks the user to clarify their request.

---

# Core Functions

## classify_intent(message: str)

This function detects the user’s intent using an LLM.

### Input

```python
message: str
```

### Output

```json
{
  "intent": "code | data | writing | career | unclear",
  "confidence": float
}
```

### Behavior

* Sends the message to the classifier prompt
* Parses the JSON output
* Handles malformed JSON safely
* Defaults to `"unclear"` if parsing fails

---

## route_and_respond(message: str, intent: dict)

This function routes the request to the appropriate expert persona.

### Workflow

1. Receive classified intent
2. Select corresponding system prompt
3. Send second LLM request
4. Generate final response
5. Log the routing decision

---

# Logging System

All requests are logged in **JSON Lines format**.

File:

```text
route_log.jsonl
```

Example entry:

```json
{
  "intent": "code",
  "confidence": 0.93,
  "user_message": "how do i sort a list in python?",
  "final_response": "Use the sorted() function or list.sort()..."
}
```

Benefits:

* Easy to parse
* Supports streaming logs
* Useful for debugging and analytics

---

# Installation

## 1 Install dependencies

Python version: **3.9+**

```bash
pip install -r requirements.txt
```

---

## 2 Set API key

Create `.env` file:

```text
OPENAI_API_KEY=your_api_key_here
```

---

## 3 Run the application

Example CLI run:

```bash
python app.py
```

---

# Example Workflow

User message:

```text
how do i sort a list of objects in python?
```

Classifier result:

```json
{
 "intent": "code",
 "confidence": 0.94
}
```

Routing:

```text
→ Code Expert prompt
```

Final output:

```text
Python solution with explanation
```

---

# Test Messages

Use these messages to verify routing behavior.

```text
how do i sort a list of objects in python?
explain this sql query for me
This paragraph sounds awkward, can you help me fix it?
I'm preparing for a job interview, any tips?
what's the average of these numbers: 12, 45, 23, 67, 34
Help me make this better.
I need to write a function that takes a user id and returns their profile
hey
Can you write me a poem about clouds?
Rewrite this sentence to be more professional.
I'm not sure what to do with my career.
what is a pivot table
fxi thsi bug pls: for i in range(10) print(i)
How do I structure a cover letter?
My boss says my writing is too verbose.
```

---

# Error Handling

The system handles several edge cases:

### Malformed JSON from LLM

If the classifier returns invalid JSON:

```json
{
 "intent": "unclear",
 "confidence": 0.0
}
```

This prevents system crashes.

---

# Optional Enhancements

## Confidence Threshold

Treat low confidence predictions as unclear.

Example:

```python
if confidence < 0.7:
    intent = "unclear"
```

## Manual Routing

Allow users to specify intent manually.

Example:

```text
@code fix this python bug
@writing review my paragraph
```

## CLI Interface

Display routing transparency:

```text
Detected intent: code
Confidence: 0.92
```

## Web Interface

You can extend this project with:

* **Flask**
* **FastAPI**
* **React frontend**

---

# Example Output

```text
Intent: writing
Confidence: 0.87

Feedback:
Your paragraph uses passive voice and several filler words.
Consider shortening sentences and replacing vague phrases.
```

---

# Why Prompt Routing Matters

Large monolithic prompts:

* Hard to maintain
* Produce generic responses
* Higher cost

Prompt routing provides:

* Better specialization
* Lower token usage
* Modular architecture
* Easier maintenance

This design pattern is widely used in **production AI systems**.

---

# Future Improvements
Possible extensions include:

* multi-intent detection
* vector search for context
* prompt versioning
* analytics dashboard
* reinforcement-based routing optimization

---
"# llm-prompt-router" 
