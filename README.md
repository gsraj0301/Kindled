# Kindled

**Curated video learning platform for college students.**  
Every video personally picked by the developer. No algorithms, no noise — just great resources.

**Live at** [kindled.pythonanywhere.com](https://kindled.pythonanywhere.com)

## Stack

- **Backend:** Django 6.0.5 + SQLite
- **Frontend:** HTML, CSS, vanilla JS
- **Python:** 3.12.3
- **Deployment:** PythonAnywhere

## Features

- Browse hand-picked educational videos by category
- **Recommended** section — must-watch videos picked by the curator, with a dedicated filter pill and badge on cards
- Filter by topic with pill-style navigation
- Watch embedded YouTube videos (with `rel=0&modestbranding=1` for no distractions)
- Graceful fallback for embed-disabled videos — shows "Watch on YouTube" card
- Curator notes explain why each video was chosen
- Students can suggest videos via the suggestion form
- Fully responsive — works on mobile and desktop

## Project structure

```
kindled/
├── config/           # Django project settings
├── core/             # Main app (models, views, forms, admin)
├── templates/core/   # HTML templates
├── static/css/       # Stylesheet
├── deploy.py         # PythonAnywhere deployment script
├── manage.py
└── db.sqlite3
```

## Local development

```bash
python manage.py runserver
```

## Deployment

```bash
python3 deploy.py --reload
```

Built with care by Raj G.
