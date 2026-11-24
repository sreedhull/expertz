# Put the site online (free, with an https link) – PythonAnywhere

You get a link like `https://YOURNAME.pythonanywhere.com`. Replace YOURNAME with your account name.

## 1. Upload
1. Create a free account at pythonanywhere.com.
2. **Files** tab → upload `expertz_django.zip` into your home folder.
3. Open a **Bash console** and run:
```bash
unzip expertz_django.zip
cd expertz_django
python3 -m venv ~/venv
source ~/venv/bin/activate
pip install -r requirements.txt
```

## 2. Secrets (never share these)
Generate a key:  `python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"`

In the console, set the variables for setup (the same ones go into the WSGI file in step 4):
```bash
export DJANGO_PRODUCTION=1
export DJANGO_SECRET_KEY='paste-the-long-key-here'
export DJANGO_ALLOWED_HOSTS='YOURNAME.pythonanywhere.com'
export DJANGO_ADMIN_URL='manage-x7k2q/'      # pick your own secret admin address, ends with /

python manage.py makemigrations main
python manage.py migrate
python manage.py seed_content
python manage.py createsuperuser              # strong password, 10+ characters
python manage.py collectstatic --noinput
```

## 3. Web app
**Web** tab → *Add a new web app* → *Manual configuration* → Python 3.10+ .
* **Virtualenv:** `/home/YOURNAME/venv`
* **Static files** (add two rows):
  * URL `/static/`  → `/home/YOURNAME/expertz_django/staticfiles`
  * URL `/media/`   → `/home/YOURNAME/expertz_django/media`
* Turn on **Force HTTPS**.

## 4. WSGI file (link on the Web tab) – replace everything with:
```python
import os, sys
sys.path.insert(0, "/home/YOURNAME/expertz_django")
os.environ["DJANGO_SETTINGS_MODULE"] = "expertz.settings"
os.environ["DJANGO_PRODUCTION"] = "1"
os.environ["DJANGO_SECRET_KEY"] = "paste-the-same-long-key-here"
os.environ["DJANGO_ALLOWED_HOSTS"] = "YOURNAME.pythonanywhere.com"
os.environ["DJANGO_ADMIN_URL"] = "manage-x7k2q/"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
Press **Reload**. Site: `https://YOURNAME.pythonanywhere.com/` · Admin: `https://YOURNAME.pythonanywhere.com/manage-x7k2q/`

Using your own domain later: add it to `DJANGO_ALLOWED_HOSTS` (comma separated) and point it in the Web tab.

## Security built in
* Live mode (`DJANGO_PRODUCTION=1`): debug off, secret key from the server, only your hostnames allowed
* Forced HTTPS, secure cookies, HSTS, clickjacking and content-sniffing protection
* Secret admin address and strong-password rules; admin sessions expire after 8 hours
* Uploads limited to jpg/png/webp, max 5 MB, verified as real images

## Keep it safe
* Never put the secret key or admin address in the zip or on GitHub.
* Back up `db.sqlite3` and `media/` regularly (Files tab → download).
* Use one admin account with a long unique password; create staff accounts only for people who need them.
* Update with `pip install -U -r requirements.txt` now and then.
