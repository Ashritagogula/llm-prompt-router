import unittest
from unittest.mock import patch, MagicMock
import json
import os

from app import classify_intent, route_and_respond, process_request, log_route, PROMPTS, ALLOWED_INTENTS

class TestRequirements(unittest.TestCase):

    def test_req_1_prompts_configured(self):
        # 1. Four system prompts present and keyed
        self.assertGreaterEqual(len(PROMPTS), 4)
        for intent in ["code", "data", "writing", "career"]:
            self.assertIn(intent, PROMPTS)
            self.assertIsInstance(PROMPTS[intent], str)
            self.assertGreater(len(PROMPTS[intent]), 20)

    @patch('app.client.chat.completions.create')
    def test_req_2_classify_intent_json(self, mock_create):
        # 2. Returns JSON with intent and confidence
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"intent": "code", "confidence": 0.95}'
        mock_create.return_value = mock_response

        result = classify_intent("Fix this bug")
        
        self.assertIn("intent", result)
        self.assertIn("confidence", result)
        self.assertEqual(result["intent"], "code")
        self.assertEqual(result["confidence"], 0.95)

    @patch('app.client.chat.completions.create')
    def test_req_3_route_and_respond(self, mock_create):
        # 3. Maps intent to prompt and generates text
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Here is your code."
        mock_create.return_value = mock_response
        
        result = route_and_respond("Fix this bug", {"intent": "code", "confidence": 0.95})
        
        # Verify it passed the right system prompt
        call_args = mock_create.call_args[1]["messages"]
        self.assertEqual(call_args[0]["role"], "system")
        self.assertEqual(call_args[0]["content"], PROMPTS["code"])
        
        self.assertEqual(result, "Here is your code.")

    def test_req_4_unclear_intent(self):
        # 4. Unclear intent returns clarification without LLM
        result = route_and_respond("idk man", {"intent": "unclear", "confidence": 0.4})
        
        self.assertIn("Are you asking for help", result)
        self.assertIn("coding, data analysis, writing, or career", result)

    def test_req_5_logging(self):
        # 5. Logging writes to JSON lines correctly
        log_file = "route_log.jsonl"
        if os.path.exists(log_file):
            os.remove(log_file)
            
        log_route("code", 0.99, "my query", "my response")
        
        with open(log_file, "r") as f:
            lines = f.readlines()
            
        self.assertEqual(len(lines), 1)
        data = json.loads(lines[0])
        self.assertEqual(data["intent"], "code")
        self.assertEqual(data["confidence"], 0.99)
        self.assertEqual(data["user_message"], "my query")
        self.assertEqual(data["final_response"], "my response")

    @patch('app.client.chat.completions.create')
    def test_req_6_malformed_json_resilience(self, mock_create):
        # 6. Graceful handling of bad JSON
        mock_response = MagicMock()
        # Invalid JSON
        mock_response.choices[0].message.content = "I think the intent is code."
        mock_create.return_value = mock_response
        
        # Should not crash and should return unclear with confidence 0.0
        result = classify_intent("Find the intent")
        
        self.assertEqual(result["intent"], "unclear")
        self.assertEqual(result["confidence"], 0.0)

if __name__ == "__main__":
    unittest.main()
