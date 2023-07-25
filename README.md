# Setting Up the Project

Hello Autofleet team!
As the task requires the project has two main components: server, client.
The following file describes how to set up each component before running it locally. Let's dive in!

### Server Prerequisites
python 3.8.6 (at least)

## Running the server:
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

3. Install requirements:
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
