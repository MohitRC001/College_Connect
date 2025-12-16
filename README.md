# College Connect 🎓

College Connect is a Django-based student networking platform where students can:
- Create profiles
- Follow other students
- Chat in real time
- Explore students by skills and interests
- Admin can generate reports

## Tech Stack
- Django
- Django Channels
- Tailwind CSS + DaisyUI
- SQLite (Dev)
- WebSockets

## Setup Instructions
```bash
git clone https://github.com/MohitRC001/College_Connect.git
cd College_Connect
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
