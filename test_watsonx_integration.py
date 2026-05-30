"""
Test WatsonX Integration
Verify that your credentials and WatsonX setup is working correctly
"""
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("\n" + "="*60)
print("SubMinds - WatsonX Integration Test")
print("="*60 + "\n")

# Test 1: Verify credentials
print("1. Checking Credentials...")
api_key = os.getenv('IBM_CLOUD_API_KEY')
space_id = os.getenv('IBM_SPACE_ID')
watson_url = os.getenv('IBM_WATSON_URL', 'https://us-south.ml.cloud.ibm.com')

if api_key:
    print(f"   ✓ API Key found: {api_key[:10]}...{api_key[-10:]}")
else:
    print("   ✗ API Key NOT FOUND in .env")

if space_id:
    print(f"   ✓ Space ID found: {space_id}")
else:
    print("   ✗ Space ID NOT FOUND in .env")

print(f"   ✓ Watson URL: {watson_url}")
print()

# Test 2: Try importing WatsonX
print("2. Testing WatsonX Imports...")
try:
    from ibm_watsonx_ai import Credentials
    print("   ✓ ibm_watsonx_ai.Credentials imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import Credentials: {e}")

try:
    from ibm_watsonx_ai.foundation_models import ModelInference
    print("   ✓ ibm_watsonx_ai.foundation_models.ModelInference imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import ModelInference: {e}")

try:
    from ibm_watson_machine_learning.foundation_models import Model
    print("   ✓ ibm_watson_machine_learning.foundation_models.Model imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import Model: {e}")

print()

# Test 3: Try creating credentials
print("3. Testing Credential Creation...")
try:
    from ibm_watsonx_ai import Credentials
    credentials = Credentials(
        url=watson_url,
        api_key=api_key
    )
    print("   ✓ Credentials object created successfully")
    print(f"   ✓ URL: {credentials.url}")
except Exception as e:
    print(f"   ✗ Failed to create credentials: {e}")

print()

# Test 4: Try initializing model
print("4. Testing Model Inference...")
try:
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
    
    credentials = Credentials(
        url=watson_url,
        api_key=api_key
    )
    
    model = ModelInference(
        model_id="meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
        credentials=credentials,
        space_id=space_id,
        params={"max_new_tokens": 100}
    )
    print("   ✓ ModelInference initialized successfully")
except Exception as e:
    print(f"   ⚠ Could not initialize ModelInference: {e}")
    print("      This may be expected if there are network/API issues")

print()

# Test 5: Test with Granite Client
print("5. Testing GraniteAIClient...")
try:
    from src.ai_engine.granite_client import GraniteAIClient
    
    client = GraniteAIClient(
        api_key=api_key,
        space_id=space_id,
        url=watson_url
    )
    
    if client.model:
        print("   ✓ GraniteAIClient initialized with active model")
    else:
        print("   ⚠ GraniteAIClient in mock mode (model not available)")
        
except Exception as e:
    print(f"   ⚠ GraniteAIClient error: {e}")

print()
print("="*60)
print("Test Complete!")
print("="*60)
