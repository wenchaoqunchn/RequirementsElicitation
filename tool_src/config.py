import os

# Configuration for the Requirements Elicitation Pipeline

# Paths
DATASET_ROOT = r"../anonymous_data"
OUTPUT_DIR = r"./output"
FRAME_CACHE_DIR = r"./output/frames"

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
LLM_MODEL = "gpt-3.5-turbo"

# Interaction Mode: 'API' (Automated) or 'WEB_UI' (Manual via ChatGPT Website)
# Set to 'WEB_UI' to generate a guide for manual interaction instead of calling the API.
LLM_INTERACTION_MODE = "WEB_UI"

# Anomaly Detection Thresholds
REPETITIVE_CLICK_THRESHOLD = 3  # Number of clicks to consider repetitive
LONG_DURATION_THRESHOLD = 5000  # ms

# Task Context (Simulated for the purpose of reproduction)
# In a real scenario, this might come from a task log or experiment design doc
TASK_DEFINITIONS = {
    "Task1": {
        "objective": "Upload a courseware file to the system",
        "expected_actions": "Login -> Navigate to Course -> Click Upload -> Select File -> Confirm",
    },
    "Task2": {
        "objective": "Create a new student account",
        "expected_actions": "Navigate to User Management -> Click Add User -> Fill Form -> Submit",
    },
}
