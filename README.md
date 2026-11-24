# Expertz Acoustics & Interiors – Django site with admin

The original design, now driven by a database. The site owner logs in at `/admin/` and changes
photos, logo, contact details, services, projects and FAQs without touching code.

## First-time setup (Windows / Mac / Linux)

```bash
python -m venv venv
venv\Scripts\activate          # Mac/Linux:  source venv/bin/activate
pip install -r requirements.txt

python manage.py makemigrations main
python manage.py migrate
python manage.py seed_content      # loads your photos + starting text
python manage.py createsuperuser   # choose the admin username & password
python manage.py runserver
```

* Website: http://127.0.0.1:8000/
* Admin:   http://127.0.0.1:8000/admin/  (log in with the superuser you just created)

## What the admin can change

| Admin section | Controls |
|---|---|
| **Site settings** | Header logo, footer logo, home-page photos, About photos, "Why us" and call-to-action backgrounds, phone numbers, WhatsApp number (the enquiry form sends here), email, address, Facebook and video links |
| **Services** | The 6 service tabs: title, text, bullet points, photo, order, show/hide. Add or remove services freely |
| **Projects** | Gallery photos: title, Previous/Ongoing, photo, order, show/hide |
| **FAQs** | Questions and answers, order, show/hide |

To replace a photo: open the item, tick "Clear" or choose a new file next to the image field, press Save.
Changes show on the website immediately.

## Notes
* `seed_content` is safe to re-run; it only fills empty things. `--reset` reloads services/projects/FAQs.
* Uploaded photos are stored in `media/`. Back this folder up along with `db.sqlite3`.
* To share it online with an https link and a secured setup, follow **DEPLOY.md**.
