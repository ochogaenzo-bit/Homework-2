import os
import argparse
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Draft Customer Support Responses with Variations")
    parser.add_argument("--complaint", type=str, help="The customer complaint text")
    parser.add_argument("--config", type=str, default="system_instruction.txt")
    parser.add_argument("--output", type=str, default="response_variations.json")
    parser.add_argument("--variations", type=int, default=3)
    
    args = parser.parse_args()
    
    # Interactive mode
    complaint = args.complaint
    if not complaint:
        print("\n[ CUSTOMER SUPPORT RESPONSE DRAFTER ]")
        complaint = input("Enter customer complaint: ")

    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    with open(args.config, "r") as f:
        system_instruction = f.read().strip()

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )
    
    # Prompt for structured variations
    prompt = f"""
    Analyze the following customer complaint and generate {args.variations} different response variations.
    CUSTOMER COMPLAINT: "{complaint}"
    
    Output JSON format:
    {{
      "category": "Category Name",
      "variations": [
        {{ "type": "Direct/Professional", "content": "..." }},
        {{ "type": "Empathetic/Warm", "content": "..." }},
        {{ "type": "Concise/Quick", "content": "..." }}
      ]
    }}
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(response_mime_type="application/json")
        )
        data = json.loads(response.text)
        
        # Print to console
        print(f"\n[ CATEGORY: {data.get('category')} ]")
        for i, var in enumerate(data.get('variations', []), 1):
            print(f"\n--- VARIATION {i}: {var.get('type')} ---\n{var.get('content')}")
            
        # Save to file
        with open(args.output, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\nSUCCESS: Variations saved to '{args.output}'")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")

if __name__ == "__main__":
    main()
