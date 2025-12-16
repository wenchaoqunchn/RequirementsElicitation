import openai
import os


class LLMClient:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        # openai.api_key = self.api_key # Uncomment for real usage

    def infer_requirements(self, prompt):
        """
        Sends the prompt to the LLM and returns the response.
        """
        print(f"--- Sending Prompt to {self.model} ---")
        print(prompt)
        print("---------------------------------------")

        # Mock response for reproduction without actual API key
        mock_response = """
1. Requirement: Add a clear visual cue or tooltip to the widget.
   - Target UI Element: Widget 'X' on Page 'Y'
   - Rationale: The user clicked repeatedly, suggesting they expected a response or the button state was unclear.

2. Requirement: Optimize the response time or add a loading spinner.
   - Target UI Element: System Feedback Mechanism
   - Rationale: The user's repetitive clicking indicates frustration with lack of immediate feedback.
"""
        return mock_response

        # Real implementation:
        # response = openai.ChatCompletion.create(
        #     model=self.model,
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # return response.choices[0].message.content
