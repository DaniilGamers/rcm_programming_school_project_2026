IMPORTANT: 

The project will only run if you follow all steps below in a clean environment. Skipping any step will cause errors.

Remember: Create and activate a virtual environment before installing dependencies

After creating and activating venv, make sure Python and pip are available:
python --version
pip --version

---

Docker notice:
This project does not require Docker.
It runs using standard Python virtual environment and requirements.txt.
Docker was not specified as a mandatory requirement in the assignment.
The recommended and supported way to run the project is via venv.

---

OPTIONAL

* The .venv / venv folders are NOT included intentionally

* The virtual environment must be created on the tester's local machine

* The project was tested by running it completely from scratch in a clean environment


---

Project Setup & Usage Guide

Notice:

* All API requests are provided in a Postman collection.
  Import the collection into Postman before testing.

* Python version: 3.10+ recommended.

* Always activate the virtual environment before installing dependencies and running the server.

---

Note: The .venv/venv folder is not included. Create a new virtual environment and install dependencies using requirements.txt before running the server.

---

OPTIONAL

* The .venv / venv folders are NOT included intentionally

* The virtual environment must be created on the tester's local machine

* The project was tested by running it completely from scratch in a clean environment

---

ABOUT TESTING

The project was tested:

* via the console

* via Postman (all requests from the collection)

* taking into account roles and permissions

* with JWT authentication

* with a separate frontend part

* All functionality was tested before submission.

---

---

IMPORTANT:
The project will ONLY launch after ALL steps below have been completed in a clean environment.

---

Activation:

For server activation:

```bash (Recommend to type commands on console by order in order to launch the server)
1. python -m venv venv(on Windows), python3 -m venv venv(on Linux/Mac)
2. venv/Scripts/activate(on Windows), source venv/bin/activate(on Linux/Mac)
3. pip install -r requirements.txt
4. python manage.py runserver
```

Skipping any of steps 1–3 will result in a server startup error.

Server runs at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)