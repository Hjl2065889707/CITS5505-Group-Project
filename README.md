## CITS5505 Group Project

This repository is used for our CITS5505 Agile Web Development group project.

### Group Members

| Name          | Student ID | GitHub Username |
| ------------- | ---------- | --------------- |
| Junlong Huang | 24041892   | Hjl2065889707   |
| Raega Tanadi  | 24761312   | Chrommanito     |
| Shuo Ma       | 23914891   | Felix-Ma1209    |
| Lizhou Xiong  | 24258175   | Oliver24258175  |

---

## Getting Started (How to Run the Project)

Please follow these steps to set up your local development environment:

### 1. Clone the repository

```bash
git clone https://github.com/YourOrg/CITS5505-Group-Project.git
cd CITS5505-Group-Project
```

### 2. Set up the Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

```bash
# Create the virtual environment
python3 -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup the Database

We use Flask-Migrate and SQLite. Before running the app for the first time, you need to create the database tables and populate it with some dummy data for testing.

```bash
# Apply database migrations
flask db upgrade

# Seed the database with fake users and posts
python seed.py
```

### 5. Run the Application

```bash
python run.py
```

The application will be available at: **http://127.0.0.1:5001/**

---

## Project Structure

- `app/` — Main Flask application folder
  - `routes/` — Page routes (Views)
  - `api/` — RESTful API endpoints for asynchronous JavaScript actions
  - `models.py` — SQLAlchemy Database Models
  - `templates/` — Jinja2 HTML Templates
  - `static/` — CSS, JavaScript, and Images
- `DESIGN.md` — Our Design System (Colors, Typography, UI Components)
