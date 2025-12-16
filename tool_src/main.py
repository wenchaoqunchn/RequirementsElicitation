import os
import pandas as pd
from config import (
    DATASET_ROOT,
    OUTPUT_DIR,
    FRAME_CACHE_DIR,
    OPENAI_API_KEY,
    TASK_DEFINITIONS,
    LLM_INTERACTION_MODE,
)
from data_loader import DataLoader
from anomaly_detector import AnomalyDetector
from context_builder import ContextBuilder
from llm_client import LLMClient


def main():
    # Initialize components
    loader = DataLoader(DATASET_ROOT)
    detector = AnomalyDetector()
    ctx_builder = ContextBuilder(FRAME_CACHE_DIR)
    llm = LLMClient(OPENAI_API_KEY)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    participants = loader.get_participants()

    all_requirements = []

    # For WEB_UI mode, prepare a markdown report
    web_ui_report_path = os.path.join(OUTPUT_DIR, "manual_interaction_guide.md")
    if LLM_INTERACTION_MODE == "WEB_UI":
        with open(web_ui_report_path, "w", encoding="utf-8") as f:
            f.write("# Manual Interaction Guide for ChatGPT Web UI\n\n")
            f.write(
                "This document contains the prompts and images needed to reproduce the study using the ChatGPT Web UI.\n"
            )
            f.write(
                "For each anomaly, copy the prompt and paste it into a new chat session (or continue if appropriate), and refer to the image if your model supports vision.\n\n"
            )

    for p_id in participants:
        print(f"Processing Participant: {p_id}")

        # 1. Load Data
        seq = loader.load_behavior_sequence(p_id)
        video_path = loader.get_video_path(p_id)

        if not seq:
            continue

        # 2. Detect Anomalies
        anomalies = detector.detect_anomalies(seq)
        print(f"  Found {len(anomalies)} anomalies.")

        for anomaly in anomalies:
            # 3. Build Context
            # Determine task context (Simplified logic: assume Task1 for demo)
            task_info = TASK_DEFINITIONS["Task1"]

            # Extract Frame
            timestamp = anomaly["timestamp"]
            frame_filename = f"{p_id}_{timestamp}.jpg"
            frame_path = ctx_builder.extract_frame(
                video_path, timestamp, frame_filename
            )

            # Construct Prompt
            prompt = ctx_builder.build_prompt(task_info, anomaly, frame_path)

            if LLM_INTERACTION_MODE == "API":
                # 4. LLM Inference (Automated)
                response = llm.infer_requirements(prompt)

                # 5. Store Result
                all_requirements.append(
                    {
                        "Participant": p_id,
                        "Timestamp": timestamp,
                        "Anomaly Type": anomaly["type"],
                        "LLM Response": response,
                    }
                )
            elif LLM_INTERACTION_MODE == "WEB_UI":
                # 4. Generate Manual Guide
                rel_frame_path = os.path.relpath(frame_path, OUTPUT_DIR)

                with open(web_ui_report_path, "a", encoding="utf-8") as f:
                    f.write(f"## Participant {p_id} - Anomaly: {anomaly['type']}\n")
                    f.write(f"**Timestamp**: {timestamp}ms\n\n")
                    f.write(f"![GUI Snapshot]({rel_frame_path})\n\n")
                    f.write("**Copy the following prompt:**\n")
                    f.write("```text\n")
                    f.write(prompt)
                    f.write("\n```\n\n")
                    f.write("---\n\n")
                print(f"  [WEB_UI] Saved prompt for anomaly at {timestamp}ms")

    if LLM_INTERACTION_MODE == "API":
        # 6. Save Results
        df = pd.DataFrame(all_requirements)
        output_path = os.path.join(OUTPUT_DIR, "inferred_requirements.xlsx")
        df.to_excel(output_path, index=False)
        print(f"Processing complete. Results saved to {output_path}")
    else:
        print(
            f"Processing complete. Open {web_ui_report_path} to start manual interaction."
        )


if __name__ == "__main__":
    main()
