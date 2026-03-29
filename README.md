# Glider Website - Deployment & Setup Guide

Welcome to the Guide! It provides step-by-step instructions on how to set up, configure, and run this application.

## 1. Project Setup & Installation

1. **Create a project directory** to hold the codebase:
   ```bash
   mkdir glider_web_app #Just for your reference, you can name it anything you want.
   cd glider_web_app
   ```
2. **Download (Clone) the application code** from GitHub:
   ```bash
   git clone https://github.com/OSUGliders/gliderweb.git
   ```
3. **Install Python tools** required to create an isolated "Virtual Environment". A virtual environment keeps our app's dependencies organized and prevents conflicts with other system software.
   ```bash
   sudo apt update
   sudo apt install python3.13-venv
   ```
4. **Create and activate the virtual environment**:

   ```bash
   python3 -m venv "v_env" #Just for your reference, you can name it anything you want.
   source v_env/bin/activate
   ```

   _(You should now see `(v_env)` at the beginning of your terminal prompt)._

5. **Navigate into the project folder** and install all necessary software packages:
   ```bash
   cd TrackMultipleGliders
   pip install --upgrade pip #Upgrade the current version of pip to the latest stable version
   pip install -r requirements.txt #To install all the required packages.
   pip install psycopg #To install the PostgreSQL adapter for Python.
   ```

## 2. Database Setup (PostgreSQL)

1. **Install PostgreSQL**:
   ```bash
   sudo apt update #Update the package list
   sudo apt install postgresql postgresql-contrib
   ```
2. **Verify Installation**:
   Confirm the installation was successful:
   ```bash
   dpkg -l | grep postgresql
   ```
3. **Manage the Database Service**:
   Start the service and check its status to ensure it is actively running:

   ```bash
   sudo systemctl start postgresql
   sudo systemctl status postgresql
   ```

4. **Initialize Database and User Credentials**:
   Enter the PostgreSQL interactive terminal:

   ```bash
   sudo -u postgres psql
   ```

   At the `postgres=#` prompt, run the following SQL commands to securely provision your application's database. \*

   ```sql
   CREATE USER "username" WITH PASSWORD "password";
   CREATE DATABASE "database_name";
   GRANT ALL PRIVILEGES ON DATABASE "database_name" TO "username";
   ```

5. **Verify the Database Connection**:
   Test accessing the database using our newly created credentials:

   ```bash
   psql -U "username" -d "database_name"
   ```

   Type `\l` (backslash + lowercase L) to list all databases and verify the database is present.

6. **Troubleshooting Database Access**:
   Only if the database connection fails, manually reset the schema ownership:

   ```bash
   sudo -u postgres psql -d "database_name"
   ```

   Drop and recreate the public schema:

   ```sql
   DROP SCHEMA public CASCADE;
   CREATE SCHEMA public AUTHORIZATION "username";
   ```

## 3. Environment Variables

Use `.env.example` as a template (which is present inside the gliderweb repo) and store actual values in a new `.env` file.
(You can also use the copyable template provided in Step 2 below).

1. Copy template to active file:
   ```bash
   cp .env.example .env
   nano .env
   ```
2. Add your server configuration variables (replace placeholder values with your actual values):
   ```env
   SECRET_KEY="your_django_secret_key"
   # Use True for local development; set False in production
   DEBUG=True
   DB_NAME="database_name"
   DB_USER="username"
   DB_PASSWORD="password"
   # Database host
   DB_HOST="localhost"
   # Example for production domain
   GLIDER_HOST_DOMAIN="glider.example.com"
   # Default PostgreSQL port
   DB_PORT="5432"
   ```
3. Save the file and exit (Ctrl + O, Enter, then Ctrl + X).
