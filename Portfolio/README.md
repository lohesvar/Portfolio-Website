# Lohesvar's Personal Portfolio

A modern, cinematic, and minimalistic personal portfolio website built with Flask, MySQL, HTML, CSS, and JavaScript.

## Features
- **Design**: Premium dark theme, glassmorphism, smooth scrolling, and custom animations.
- **Backend**: Python/Flask handles routing and API endpoints.
- **Database**: MySQL integration to store contact form submissions.
- **Responsive**: Fully optimized for desktop and mobile devices.

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- MySQL Server installed and running locally

### 2. Database Setup
1. Open your MySQL command line or a tool like MySQL Workbench.
2. Run the `schema.sql` file or copy its contents and execute them to create the database and table:
   ```bash
   mysql -u root -p < schema.sql
   ```

### 3. Environment Variables
1. Open the `.env` file in the root directory.
2. Update the credentials to match your local MySQL setup:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_actual_mysql_password
   DB_NAME=portfolio_db
   SECRET_KEY=generate_a_random_secret_key_here
   ```

### 4. Install Dependencies
Create a virtual environment (optional but recommended) and install the required Python packages:

```bash
# Create virtual environment (Windows)
python -m venv venv
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 5. Run the Application
Start the Flask development server:

```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000` to view the site!

## Troubleshooting
- **Database Connection Error**: Ensure your MySQL server is running and the credentials in `.env` are correct.
- **ModuleNotFoundError**: Make sure you activated your virtual environment and ran `pip install -r requirements.txt`.
- **Port 5000 in use**: You can change the port in `app.py` at the very bottom `app.run(debug=True, port=5001)`.
