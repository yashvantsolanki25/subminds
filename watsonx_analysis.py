import json
import requests
import os
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

# Load environment variables
load_dotenv()

# 1. Setup Session Context with your active token and region
credentials = Credentials(
    url=os.getenv("IBM_WATSON_URL", "https://us-south.ml.cloud.ibm.com"),
    api_key=os.getenv("IBM_CLOUD_API_KEY")
)

# 2. Define your Project Target Workspace
SPACE_ID = os.getenv("IBM_SPACE_ID")

# 3. Configure the Foundation Model (Llama 4 Maverick for text/creative processing)
model_id = os.getenv("MODEL_ID", "meta-llama/llama-4-maverick-17b-128e-instruct-fp8")
gen_params = {
    "decoding_method": "sample",
    "max_new_tokens": int(os.getenv("MAX_TOKENS", "300")),
    "temperature": float(os.getenv("TEMPERATURE", "0.7")),
    "top_p": float(os.getenv("TOP_P", "0.85"))
}

# Initialize Inference Client with Space ID
model = ModelInference(
    model_id=model_id,
    credentials=credentials,
    space_id=SPACE_ID,
    params=gen_params
)

# 4. Construct a Structured Prompt for Cognitive/Subconscious Analysis
journal_input = (
    "I keep dreaming about standing at a high crossroads in a desert. "
    "I have maps, but the ink is fading, and I feel an urgent pressure to choose a path "
    "before nightfall, even though every direction looks identical."
)

prompt = f"""
System: You are an expert cognitive psychologist specializing in archetypal analysis and subconscious thought patterns.
Analyze the following recurring dream text sample to deduce underlying subconscious themes, motivations, hidden anxieties, or core desires of the individual.

Text Sample: "{journal_input}"

Provide the analysis broken down into:
1. Core Subconscious Motivation
2. Underlying Anxieties / Stressors
3. Actionable Focus Area
"""

# 5. Execute the Generation Pipeline
try:
    print("Sending analytical processing request to watsonx.ai...")
    response = model.generate_text(prompt=prompt)
    print("\n================ ANALYSIS RESULTS ================")
    print(response)
    print("==================================================")
except Exception as e:
    print(f"\nExecution failed. Error details: {e}")
