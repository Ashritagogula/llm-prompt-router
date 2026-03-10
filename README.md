# LLM-Powered Prompt Router

A service that intelligently routes user requests to specialized AI personas using a two-step LLM process: Classify intent, then Respond using an expert system prompt.

## Setup

1. Clone the repository.
2. Ensure you have Python 3.10+ installed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and configure your `OPENAI_API_KEY`.
   ```bash
   cp .env.example .env
   # Edit .env with your actual key
   ```

## Running the Application

### Locally (CLI)

Run interactively:
```bash
python app.py
```

Process a single message:
```bash
python app.py --message "how do I sort a list in python?"
```

### Via Docker

Build and run using Docker Compose:
```bash
docker-compose up --build -d
docker-compose exec router python app.py
```

## How It Works

1. **Classify**: The user's input is sent to the LLM with a brief prompt asking it to choose between `code`, `data`, `writing`, `career`, or `unclear`. The response is constrained to JSON.
2. **Route and Respond**: Based on the identified intent, the system retrieves a specialized expert prompt (from `prompts.json`) and makes a second LLM API call to generate a context-aware response. If the intent is `unclear` (or the classifier returns invalid JSON), it prompts the user for clarification without consulting an expert persona.
3. **Log**: Every request, its classification confidence, and the final response are logged sequentially into `route_log.jsonl`.
