# The Murals of Kyiv website

Production: http://kyivmural.com
Development: http://188.166.67.16

# Run

tba

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

## Adding new language

Add new language, for example spanish `es`
```bash
pybabel init -i messages.pot -d app/translations -l es
```

# Requirements

see [requirements.txt](./requirements.txt)
