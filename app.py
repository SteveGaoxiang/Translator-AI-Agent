import streamlit as st
import pandas as pd
from main import translate_text
import json

def load_glossary_from_excel(file):
    """Load glossary from uploaded Excel file"""
    try:
        df = pd.read_excel(file)
        # Assuming the first two columns are source and target
        # Get the column names
        source_col = df.columns[0]
        target_col = df.columns[1]
        return dict(zip(df[source_col], df[target_col]))
    except Exception as e:
        st.error(f"Error reading Excel file: {str(e)}")
        return {}

def main():
    st.title("Multi-Agent Translation System")
    
    # Create two columns for source and target language selection
    col1, col2 = st.columns(2)
    
    with col1:
        source_lang = st.selectbox(
            "Source Language",
            ["English", "Spanish", "French", "German", "Chinese", "Japanese"]
        )
    
    with col2:
        target_lang = st.selectbox(
            "Target Language",
            ["Spanish", "English", "French", "German", "Chinese", "Japanese"]
        )
    
    # Text area for source text
    source_text = st.text_area(
        "Enter text to translate",
        height=150,
        placeholder="Enter your text here..."
    )
    
    # Glossary upload section
    st.subheader("Glossary Upload")
    st.markdown("""
    Upload an Excel file with your glossary. The Excel file should have two columns:
    - First column: Words in the source language
    - Second column: Corresponding translations in the target language
    """)
    
    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=["xls", "xlsx"],
        help="Upload your glossary in Excel format (.xls or .xlsx)"
    )
    
    glossary = {}
    if uploaded_file is not None:
        try:
            glossary = load_glossary_from_excel(uploaded_file)
            if glossary:
                st.success("Glossary loaded successfully!")
                
                # Display glossary preview
                st.write("Glossary Preview:")
                preview_df = pd.DataFrame(list(glossary.items()), columns=['Source', 'Target'])
                st.dataframe(preview_df, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading glossary: {str(e)}")
    
    # Translation button
    if st.button("Translate"):
        if not source_text:
            st.warning("Please enter some text to translate.")
        else:
            try:
                with st.spinner("Translating..."):
                    # Call the translation function
                    final_translation = translate_text(source_text, glossary)
                    
                    # Display results in a nice format
                    st.subheader("Translation Results")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Original Text:**")
                        st.write(source_text)
                    
                    with col2:
                        st.markdown("**Translated Text:**")
                        st.write(final_translation)
                    
                    # Add download button for the translation
                    st.download_button(
                        label="Download Translation",
                        data=final_translation,
                        file_name="translation.txt",
                        mime="text/plain"
                    )
                    
            except Exception as e:
                st.error(f"Translation error: {str(e)}")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Multi-Agent Translator",
        page_icon="🌐",
        layout="wide"
    )
    main() 