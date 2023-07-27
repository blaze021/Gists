import streamlit as st
import requests

def get_backend_response(text_input, file_input):
    # Replace 'http://backend-api-url' with the actual URL of your backend API
    backend_api_url = 'http://backend-api-url'
    
    # Define the data to be sent to the backend (you may modify this according to your API requirements)
    data = {
        'text_input': text_input,
        'file_content': file_input.getvalue() if file_input else None,
    }
    
    try:
        response = requests.post(backend_api_url, data=data)
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def main():
    st.title("Text and File Upload App")
    st.write("Enter your text below and upload a file if needed.")

    # User input
    text_input = st.text_area("Enter text here", value='', height=150)

    # File upload
    file_input = st.file_uploader("Upload a file", type=['txt', 'pdf', 'png', 'jpg'])

    if st.button("Submit"):
        # Call the backend to get the response
        response = get_backend_response(text_input, file_input)

        # Display the response
        st.write("Backend Response:")
        st.write(response)

if __name__ == "__main__":
    main()￼Enter
