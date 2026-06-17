# Kindled

Curated video learning platform for college students. Every video personally picked by the developer.

## Location
`/home/raj/Documents/Intern projects/kindled/`

## Stack
- Django 6.0.5 + SQLite
- HTML, CSS, vanilla JS
- Managed with `uv` (`.venv/`)
- Python 3.12.3
- No user auth in v1

## Project structure
```
kindled/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── models.py       # Category, Video (w/ recommended), Suggestion
│   ├── views.py        # home (filterable by ?category & ?recommended), video_detail, suggest
│   ├── forms.py        # SuggestionForm
│   ├── admin.py        # All 3 registered (uses format_html for thumbnail)
│   └── migrations/
├── templates/
│   └── core/
│       ├── base.html          # Logo, favicon, nav with search + suggest
│       ├── home.html          # Explainer paragraph, filter pills, video grid
│       ├── video_detail.html  # embed_disabled conditional
│       ├── suggest.html       # Per-field help text
│       └── suggest_success.html
├── static/
│   ├── css/
│   │   └── main.css           # Responsive (mobile + desktop)
│   ├── favicon/               # Favicon assets (ico, png, webmanifest)
│   └── logo.png               # Site logo
├── CREDITS.md                    # Contributor credits (logo by Kishore)
├── screenshots/
│   ├── Kindled-website-preview.png
│   └── favicon_io/            # Source favicon files
├── deploy.py                  # PythonAnywhere API deploy script
├── manage.py
└── db.sqlite3
```

## URL routes
```
/                       → home (filterable by ?category=slug or ?recommended=1)
/video/<youtube_id>/    → video_detail
/suggest/               → suggest (GET form, POST submit)
/admin/                 → Django admin
```

## Models

### Category
- name, slug (unique), icon (emoji), order
- Meta: ordering=['order'], verbose_name_plural='Categories'

### Video
- title, youtube_id (unique), category (FK), channel_name, curator_note (unlimited), date_added (auto), embed_disabled, recommended
- Meta: ordering=['-date_added']

### Suggestion
- name (optional), department (optional), youtube_url, description, status (pending/reviewed/added/not_a_fit), submitted_at (auto)

## Admin customizations
- CategoryAdmin: prepopulated_fields slug from name
- VideoAdmin: thumbnail_preview from youtube_id, list_filter by category and recommended, list_display includes recommended
- SuggestionAdmin: list_filter by status
- Admin uses `format_html` for thumbnail (NOT deprecated `allow_tags`)

## Frontend — what exists
- `templates/core/base.html` — sticky glassmorphism nav with logo (image), search bar, suggest button; favicon links, web manifest, theme-color meta tag
- `templates/core/home.html` — explainer paragraph, filter pills (including 🌟 Recommended) + video grid with recommended badge overlay on thumbnails, empty state
- `templates/core/video_detail.html` — YouTube embed (or Watch on YouTube card if embed_disabled), title, channel, curator note, back link
- `templates/core/suggest.html` — Django form with styled fields
- `templates/core/suggest_success.html` — confirmation page with checkmark icon
- `static/css/main.css` — full responsive design (nav, hero, pills, grid, cards, form, video detail, no-embed box, success page)
- `static/logo.png` — website logo in navbar
- `static/favicon/` — favicon in 5 formats + apple-touch-icon + webmanifest

## Design rules
- Navbar: sticky, glassmorphism (blur), logo + search bar + suggest button
- Video detail: NO related/recommended videos (rel=0, modestbranding=1)
- Filter pills: click → reload with `?category=slug` or `?recommended=1`, client-side JS can do this
- Recommended videos: marked via boolean field, show 🌟 badge on card thumbnail and have a dedicated filter pill
- Search: client-side filter by title (hide matching cards) via input in nav
- Suggestion form: opens from navbar suggest button
- Thumbnails: `https://img.youtube.com/vi/{youtube_id}/hqdefault.jpg`
- Logo hover: slight rotate + scale animation
- No student login
- SQLite for now

## Deployment
- **Live at** [kindled.pythonanywhere.com](https://kindled.pythonanywhere.com) — already deployed with real student engagement
- Deploy via `python3 deploy.py --reload` (API token embedded)
- Uploads all project files to `/home/kindled/kindled/` and reloads the web app

## Known issues to fix
- `settings.py`: missing `DEFAULT_AUTO_FIELD` (Django W042 warning)

## TODO
- Write tests
- Add more categories and videos
- Add search results count
- Make curator_note limit consistent in admin form

## Contributors
- **Raj G.** — creator, developer, curator
- **kieskishore-cyber** — designed the website logo & favicon

## DB state (as of Jun 15 2026)
- 7 Categories (Programming 💻, Web Dev 🌐, AI 🤖, Cybersecurity 🔐, Physics ⚛️, Math 📐, General 🧠)
- 28 Videos (1 recommended)
- 0 Suggestions
