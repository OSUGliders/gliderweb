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
