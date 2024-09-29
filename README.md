# FastAPI  UserRegistration 
This repository contains a FastAPI application that implements user registration and OTP (One-Time Password) based authentication. Users can register, receive an OTP via email, and authenticate using the OTP. This setup is ideal for applications requiring an extra layer of security.


## Table of Contents

1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Project Setup](#project-setup)
4. [Running the Application](#running-the-application)
5. [Running Tests](#running-tests)

## Getting Started
Follow the instructions below to set up and run your FastAPI project.

### Prerequisites
Ensure you have the following installed:

- Python >= 3.12
- PostgreSQL

### Project Setup
1. Clone the project repository:
    ```bash
    git clone https://github.com/MOHAN2310/UserRegistration.git
    ```
   
2. Navigate to the project directory:
    ```bash
    cd UserRegistration/
    ```

3. Create and activate a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up environment variables by copying the example configuration:
    ```bash
    cp .env.example .env
    ```


## Running the Application
Start the application:
    ```bash
    uvicorn routes:main --reload
    ```

