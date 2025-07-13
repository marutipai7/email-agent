# 📧 Email Extractor Agent

A Django + Pydantic powered mini AI agent to extract emails from text input, classify them (Personal / Business / Spam), and save them to a user dashboard with export support.

## 🚀 Features

- Extract emails from text
- Classify type (using simple AI rules)
- User register/login/logout
- Dashboard with pagination
- Export contacts to CSV
- Admin panel support

## 🛠️ Tech Stack

- Python 3.10+
- Django 5.x
- Pydantic 2.x
- SQLite (default) or PostgreSQL
- Bootstrap (basic styling)
- Gunicorn + Render for deployment

## 🧪 Installation

```bash
git clone https://github.com/marutipai7/email-agent.git
cd email-extractor
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
