# ⚡ Fast Tasks — Django App for Notes & Productivity
![Python](https://img.shields.io/badge/python-3.14-blue)
![Django](https://img.shields.io/badge/django-5.2.7-green)
![Status](https://img.shields.io/badge/Status-Finished-green.svg)  

> A fast, elegant, and minimalistic Django web app for managing your notes, to-dos, and daily tasks.  

---

## ✨ Features

- 📝 **Create, edit, and delete notes** in a simple and intuitive interface.  
- ⏰ **Add deadlines** and mark tasks as completed.  
- 🔍 **Search and filter** your notes easily.  
- 🌙 **Dark / Light mode** support for comfortable use.  
- 🧠 **User authentication** — register and manage your personal notes securely.  
- ⚙️ Built with clean and modular Django architecture (apps, models, views, templates).

---

## 🗂 Project Structure
```
fast_tasks/
│
├── fast_tasks/           # Main Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── tasks_app/                # Main app: models, views, etc.
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── tests.py
│   ├── admin.py
│   └── apps.py
│
│
├── templates/            # Base HTML templates
├── static/               # Global static files
├── manage.py
└── requirements.txt
```
---


## 🚀 Quick Start

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Lolkov1ch/fast_tasks
cd fast_tasks
```
### 2️⃣ Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Run migrations
```bash
python manage.py migrate
```
### 5️⃣ Start the development server
```bash
python manage.py runserver
```
