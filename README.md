# IT Company Task Manager

A Django-based task management system for IT teams — featuring projects, tasks, workers, teams, and positions.

---

## 🛠 Tech Stack

- Python 3.12+ (tested on 3.12.3)
- Django 5.1+
- SQLite (default)
- Bootstrap 5 (via Soft UI Dashboard)
- crispy-forms + crispy-bootstrap5

---

## 🔧 Setup Instructions

1. **Clone the repository**:

```bash
git clone <https://github.com/TenbReala/IT_company_task_manager.git>
cd IT_company
```

2. **Create virtual environment**:

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Apply migrations**:

```bash
python manage.py migrate
```

5. **Load test data** (26 workers, 3 teams, 3 projects, 36 tasks):

```bash
python manage.py loaddata fixtures/test_data.json
```

6. **Run development server**:

```bash
python manage.py runserver
```

---

## 👤 Test Account

Use this account to log in as a regular user:

- **Username:** `anna_olson`
- **Password:** `test1234`

Optional: Set `is_staff=True` for admin panel access.

---

## 📁 File Structure Highlights

- `task_manager/models.py` — all core models (Worker, Task, Project, etc.)
- `task_manager/views.py` — class-based views for CRUD and dashboard
- `templates/` — Soft UI Dashboard-based HTML templates
- `fixtures/test_data.json` — demo dataset for development

---

## 🗂 Database Schema

The following diagram shows the structure of the main models and their relationships:

📎 [Click to open .drawio file](task_manager.drawio)

---

## 🧪 Running Tests

Test module is present but currently contains no test cases. To run tests once implemented:

```bash
python manage.py test
```

---

## 📌 Notes

- All migrations were reset for this version (see commit `migrations: reset`)

---

## ✅ To-Do / Future Improvements

- Dark mode toggle
- Registration form styling
- Pagination display counter
- Admin-only access to Position/TaskType editing
- Avatar and color scheme support for workers/projects

---

## 💡 Development Tips

- Format code with `black .`
- Lint code with `flake8 .`
- Use `python manage.py createsuperuser` to make admin user
- Use `python manage.py flush && python manage.py loaddata ...` to reset data

---

## 📄 License

MIT License (or your chosen license here)

---

## ✍️ Author

Viktor Zhdanovych

---

## Acknowledgments

Parts of this project were generated with the help of ChatGPT-4o, including the initial README, test fixture, and some code components (e.g., modals).

## Live Demo
https://task-manager-jt4c.onrender.com
