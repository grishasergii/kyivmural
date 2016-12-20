# The Murals of Kyiv website

Production: http://kyivmural.com

Development: http://188.166.67.16

# Set-up

Init database and add defaults like the admin user and the languages
```bash
python run.py db init
python run.py set_defaults --name YOUR_ADMIN_NAME --pass YOUR_ADMIN_PASS
```

Do migration
```bash
pyrhon run.py db migrate
```

Upgrade
```bash
pyrhon run.py db upgrade
```

# Run

Run on localhost with `gunicorn`
```bash
gunicorn run:app -b localhost:XXXX
```

# Internationalization and Localization

## Update existing languages
1. Extract texts for translations
2. Update the translations
3. Compile translated texts

```bash
pybabel extract -F babel.cfg -o messages.pot --input-dirs=./app
pybabel update -i messages.pot -d app/translations
pybabel compile -d app/translations/
```

## Adding a new language

Add a new language, for example Spanish `es`
```bash
pybabel init -i messages.pot -d app/translations -l es
```

# Requirements

See [requirements.txt](./requirements.txt)
