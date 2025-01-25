import streamlit as st
import requests
import json
import re

# Function to read the content of the Markdown file
def read_markdown_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to extract tables from Markdown content using regex
def extract_tables_from_markdown(markdown_content):
    # Using regex to find tables in the markdown
    tables = re.findall(r"\|.*\|", markdown_content)
    if not tables:
        return None  # No table found
    return tables

# Function to refine the content using the dataset (Markdown content)
def refine_content_using_dataset(markdown_content):
    """Refine the input content by analyzing and adjusting it based on the dataset."""
    # Extract relevant sections from Markdown (such as tables or headers)
    tables = extract_tables_from_markdown(markdown_content)
    refined_content = markdown_content  # Start with the raw content

    # Example: You can enhance the content by processing tables, headers, or certain sections
    if tables:
        refined_content += "\n\nRefined tables section added:\n" + "\n".join(tables)

    # Additional logic can be added here to refine the content based on specific needs
    # For example, removing unnecessary sections, emphasizing important parts, etc.
    return refined_content

# Function to query the Gemini API
def query_gemini(prompt):
    """Send the prompt to the Gemini API to generate content."""
    try:
        # Gemini API Key (Replace with the actual key from here)
        GEMINI_API_KEY = "AIzaSyC_aP3sTq_kPSJjyLrGdilWgYHhLDdX9t4"  # Your API key

        # URL for Gemini model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

        # Request headers
        headers = {
            "Content-Type": "application/json"
        }

        # Request payload with the prompt as input
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        # Send the POST request
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            # Extract the generated content
            generated_content = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response")
            return generated_content
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

# Main function to process the Markdown content, refine it, and send it to Gemini API
def process_markdown_and_query(file_path, query_text):
    markdown_content = read_markdown_file(file_path)
    
    # Try to extract tables from the Markdown content
    tables = extract_tables_from_markdown(markdown_content)
    
    # Refine the content using the dataset (Markdown file)
    refined_content = refine_content_using_dataset(markdown_content)
    
    # If a query is entered, we send it to Gemini
    if query_text:
        response = query_gemini(query_text)
        st.write(f"Response from Gemini: {response}")
        return
    
    # Show the extracted tables if found, or process the entire refined content as a prompt
    if tables:
        st.write("Table found in the Markdown content:")
        st.write("\n".join(tables))
    else:
        st.write("No table found in the Markdown file. Proceeding with refined text content.")
        response = query_gemini(refined_content)  # Send the refined content as a prompt
        st.write(f"Response from Gemini: {response}")

# Streamlit UI components
st.title("Markdown Table and Gemini API Integration")

# File uploader to upload the markdown file
uploaded_file = st.file_uploader("Upload a Markdown file", type=["md"])

# Query box for user input
query_text = st.text_input("Enter your query")

if uploaded_file:
    # Save the uploaded file temporarily
    with open("uploaded_file.md", "wb") as f:
        f.write(uploaded_file.read())

    # Process the file and display the result
    process_markdown_and_query("uploaded_file.md", query_text)
else:
    st.write("Please upload a Markdown file to continue.")
