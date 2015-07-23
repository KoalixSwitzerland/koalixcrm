
DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "c82186b5-e39f-489c-b570-ae2748a7af182ae2373e-12c5-45ae-a5a4-919c3a225209cc7334e2-3c79-4bee-8324-35e033c230b3"
NEVERCACHE_KEY = "69e1a22f-5c49-4f18-8c29-80e7cf83f966ca0446c7-de3f-4068-8356-a2831fc1f9562267b36f-518c-4759-b96d-99d3503eefd5"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "dev.db",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

# SHOP_CURRENCY_LOCALE = "de_CH"
APPEND_SLASH = True

ROOT_URLCONF = "urls"