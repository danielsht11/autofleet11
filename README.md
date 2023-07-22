# Setting Up the Project

## Running the backend:

1. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set the Flask app environment variable:
   - On Windows (Command Prompt):
     ```
     set FLASK_APP=app
     ```
     or PowerShell:
     ```
     $env:FLASK_APP = "app"
     ```
   - On macOS and Linux:
     ```
     export FLASK_APP=app
     ```
     
5. Run the Flask app:
    ```
    flask run
   ```

## Running the client:

1. 
