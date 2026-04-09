import os
import argparse
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def main():
    """
    Main function to handle CLI arguments and generate customer support responses.
    """
    parser = argparse.ArgumentParser(description="Draft Customer Support Responses using Gemini AI")
    parser.add_argument("--complaint", type=str, help="The customer complaint or feedback text")
    parser.add_argument("--config", type=str, default="system_instruction.txt", help="Path to the system instruction configuration file")
    parser.add_argument("--output", type=str, default="response.txt", help="Path to save the generated response")
    
    args = parser.parse_args()
    
    # Interactive mode if no complaint is provided via CLI
    complaint = args.complaint
    if not complaint:
        print("Welcome to the Customer Support Response Drafter!")
        complaint = input("Please enter the customer's complaint or feedback: ")
        if not complaint.strip():
            print("Error: Complaint cannot be empty.")
            return

    # Configure Gemini API
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Please set it in your environment or .env file.")
        return
    
    genai.configure(api_key=api_key)
    
    # Load system instruction from file
    try:
        with open(args.config, "r") as f:
            system_instruction = f.read().strip()
    except FileNotFoundError:
        system_instruction = (
            "You are a world-class customer support specialist. "
            "Your goal is to provide empathetic, professional, and solution-oriented responses "
            "to customer complaints. Always acknowledge their frustration, apologize sincerely, "
            "and offer a concrete next step or solution."
        )
        print(f"Note: Config file '{args.config}' not found. Using default system instructions.")

    # Initialize the model (using 1.5 Flash for speed)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )
    
    print("\n" + "="*50)
    print("STRATEGY: Analyzing complaint and drafting response...")
    print("="*50)
    
    try:
        # Generate the response
        response = model.generate_content(complaint)
        response_text = response.text
        
        # Structured Output
        print("\n[DRAFTED RESPONSE]")
        print("-" * 20)
        print(response_text)
        print("-" * 20)
        
        # Save to file
        with open(args.output, "w") as f:
            f.write(response_text)
        print(f"\nSUCCESS: Response saved to '{args.output}'")
        
    except Exception as e:
        print(f"\nERROR: Failed to generate response. {str(e)}")

if __name__ == "__main__":
    main()
