import os
import argparse
import json
from datetime import datetime
from openai import OpenAI

# --- CONFIGURATION ---
# This system instruction is configurable. 
# You can change the tone or specific business rules here.
DEFAULT_SYSTEM_INSTRUCTION = """
You are an expert Customer Support Specialist. 
Your task is to analyze a customer's message and provide:
1. Sentiment Analysis (Positive, Neutral, or Negative)
2. Summary of the Issue
3. A Drafted Response that is empathetic, professional, and provides a clear solution.

Guidelines:
- If the customer is angry, acknowledge their frustration immediately.
- If a technical solution isn't clear, ask clarifying questions or offer a follow-up.
- Keep the tone helpful and concise.
"""

def generate_support_response(api_key, customer_input, system_instruction):
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Customer Message: {customer_input}"}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling API: {str(e)}"

def save_output(content, customer_id="support_draft"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{customer_id}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def main():
    parser = argparse.ArgumentParser(description="AI Customer Support Draft Tool")
    
    # Arguments
    parser.add_argument("--input", type=str, help="The customer complaint or feedback text")
    parser.add_argument("--key", type=str, help="Your OpenAI API Key")
    parser.add_argument("--instruction", type=str, default=DEFAULT_SYSTEM_INSTRUCTION, 
                        help="Optional: Override the default system instruction")
    parser.add_argument("--file", action="store_true", help="Save the output to a text file")

    args = parser.parse_args()

    # Handle missing API key
    api_key = args.key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: API Key is required. Provide it via --key or set OPENAI_API_KEY env var.")
        return

    # Handle missing input (Interactive mode)
    customer_text = args.input
    if not customer_text:
        print("--- Drafting Customer Support Responses ---")
        customer_text = input("Please enter the customer's message: ")

    print("\n[Processing Draft...]\n")
    
    result = generate_support_response(api_key, customer_text, args.instruction)

    # Structured Output to Console
    print("="*30)
    print("AI-GENERATED SUPPORT DRAFT")
    print("="*30)
    print(result)
    print("="*30)

    # Save to File
    if args.file:
        saved_file = save_output(result)
        print(f"\nDraft saved successfully to: {saved_file}")

if __name__ == "__main__":
    main()
