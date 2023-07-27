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





_---------
Sure! Below is an example of a Flask API that accepts a CSV file and text as input, processes the input, and returns a response. For demonstration purposes, let's assume that the API reads the CSV file, counts the number of rows and columns, and appends the text input to each row in the CSV file before returning it.

First, make sure you have Flask and pandas installed. If not, you can install them using pip:

```bash
pip install flask pandas
```

Create a Python file (e.g., `app.py`) and add the following code:

```python
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

def process_input(csv_file, text_input):
    # Read the CSV file using pandas
    df = pd.read_csv(csv_file)

    # Count the number of rows and columns in the CSV file
    num_rows, num_columns = df.shape

    # Append the text input to each row in the CSV file
    df['Text_Input'] = text_input

    return df.to_dict(orient='records'), num_rows, num_columns

@app.route('/process_data', methods=['POST'])
def process_data():
    # Get the CSV file and text input from the request
    csv_file = request.files['csv_file']
    text_input = request.form['text_input']

    # Check if both CSV file and text input are provided
    if not csv_file or not text_input:
        return jsonify({"error": "CSV file and text input are required."}), 400

    try:
        # Process the input
        processed_data, num_rows, num_columns = process_input(csv_file, text_input)
        
        # Return the response as JSON
        return jsonify({
            "processed_data": processed_data,
            "num_rows": num_rows,
            "num_columns": num_columns,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

Save the file and run the Flask app using the following command:

```bash
python app.py
```

Your Flask API will be up and running at `http://127.0.0.1:5000/`. It exposes a single endpoint `/process_data` that accepts a POST request with a CSV file and a text input. The API will process the input and return a JSON response containing the processed data (with text appended to each row), the number of rows, and the number of columns in the CSV file.

Please note that this is a simple example to demonstrate the Flask API. In a real-world scenario, you may need to perform more complex processing based on the input data. Additionally, consider adding proper error handling and input validation to the API for production use.




--------------


Sure! Below is an example of a Streamlit UI code where the user can input text and upload a file. The backend will generate a response based on the input and display it to the user.

First, make sure you have Streamlit installed. If not, you can install it using pip:

```bash
pip install streamlit
```

Now, create a Python file (e.g., `app.py`) and add the following code:

```python
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
    main()
```

Note that in the `get_backend_response()` function, you need to replace `'http://backend-api-url'` with the actual URL of your backend API that handles the processing based on the text and file inputs. The backend API should handle the input and generate the response accordingly.

Ensure that your backend API is running and correctly handles the data sent from the frontend (Streamlit app). Once the Streamlit app is running, it will provide a UI where the user can enter text and upload a file. When the user clicks the "Submit" button, it will call the backend API, receive the response, and display it to the user on the Streamlit UI.
