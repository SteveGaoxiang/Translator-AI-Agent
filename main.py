from openai import OpenAI
from typing import List, Dict
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def translation_agent(source_text: str) -> str:
    """First agent that creates initial translation following technical rules."""
    completion = client.chat.completions.create(
        model="gpt-4",  # Changed to gpt-4
        messages=[
            {"role": "system", "content": "You are a Translation Agent that follows technical rules for accurate translation."},
            {"role": "user", "content": f"Translate this text: {source_text}"}
        ]
    )
    return completion.choices[0].message.content

def review_agent(translated_text: str) -> str:
    """Second agent that reviews and improves the translation."""
    completion = client.chat.completions.create(
        model="gpt-4",  # Changed to gpt-4
        messages=[
            {"role": "system", "content": "You are a Review Agent that improves translations for natural flow."},
            {"role": "user", "content": f"Review and improve this translation: {translated_text}"}
        ]
    )
    return completion.choices[0].message.content

def proofread_agent(reviewed_text: str, glossary: Dict[str, str]) -> str:
    """Third agent that checks against translation memory and glossary."""
    glossary_str = "\n".join([f"{k}: {v}" for k, v in glossary.items()])
    completion = client.chat.completions.create(
        model="gpt-4",  # Changed to gpt-4
        messages=[
            {"role": "system", "content": "You are a Proofreading Agent that ensures consistency with the glossary."},
            {"role": "user", "content": f"Check this translation against the glossary:\n\nTranslation: {reviewed_text}\n\nGlossary:\n{glossary_str}"}
        ]
    )
    return completion.choices[0].message.content

def translator_ai_agent(proofread_text: str) -> str:
    """Final agent that produces the final translation."""
    completion = client.chat.completions.create(
        model="gpt-4",  # Using gpt-4 for consistency
        messages=[
            {"role": "system", "content": "You are the main Translator AI Agent that produces final, polished translations."},
            {"role": "user", "content": f"Finalize this translation: {proofread_text}"}
        ]
    )
    return completion.choices[0].message.content

def translate_text(source_text: str, glossary: Dict[str, str] = None) -> str:
    """Main workflow that coordinates all agents."""
    if glossary is None:
        glossary = {}
    
    try:
        # Step 1: Initial translation
        initial_translation = translation_agent(source_text)
        
        # Step 2: Review translation
        reviewed_translation = review_agent(initial_translation)
        
        # Step 3: Proofread translation
        proofread_translation = proofread_agent(reviewed_translation, glossary)
        
        # Step 4: Final translation
        final_translation = translator_ai_agent(proofread_translation)
        
        return final_translation
    except Exception as e:
        print(f"Error during translation: {str(e)}")
        raise e

if __name__ == "__main__":
    source_text = "Hello world! This is a test message."
    glossary = {
        "Hello": "Hola",
        "world": "mundo"
    }
    
    final_translation = translate_text(source_text, glossary)
    print("Final translation:", final_translation)
