# Setting Up the Project

Hello Autofleet team!
As the task requires the project has two main components: server, client.
Make sure you are on the project directory.
The following file describes how to set up each component before running it locally. Let's dive in!

## Server

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

4. Navigate to the backend directory:
    ```
   cd backend
   ```
5. Set the Flask app environment variable:
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
     
6. Run the Flask app:
    ```
    flask run
   ```
   
7. You can run the tests with the following command:
    ```
    pytest tests/tests.py
   ```

## Client

### Client Prerequisites
npm 9.8.1
node version higher than 17 (I used 20.5.0)

## Running the client:

1. Navigate to the frontend directory:
    ```
   cd frontend
   ```

2. Start the React app:
    ```
   npm start
   ```


If you have any other questions, fell free to send a message: danielsht11@gmail.com