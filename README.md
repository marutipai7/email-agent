# 📧 Email Contact Extractor with Dashboard (Django + Pydantic)

This is a smart email contact extractor built using **Django**, **Pydantic**, and basic ML logic to classify contacts as personal, business, or spam. Extracted contacts are saved in the database and displayed on a clean dashboard with pagination and CSV export support.

---

## 🔧 Features

- 🧠 AI-Powered Email Type Classification (Personal, Business, Spam)
- 📄 Email Extraction from Text Input
- 🧰 Form-based Upload
- 🔐 Register/Login/Logout
- 🗃️ Dashboard to View Contacts
- 📥 CSV Export
- 📄 SQLite for local DB
- 🚀 Deployable to Render

---

## 🏗️ Tech Stack

- **Backend:** Django, Pydantic
- **Frontend:** HTML (Jinja templates)
- **DB:** SQLite (you can switch to PostgreSQL)
- **Export:** CSV using `HttpResponse`
- **Deployment:** Render (free-tier)

---

## 🧪 Installation

```bash
git clone https://github.com/marutipai7/email-agent.git
cd email-extractor
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
