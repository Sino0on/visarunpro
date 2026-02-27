from decouple import config

BOT_TOKEN = config("BOT_TOKEN")
REDIS_URL = config("REDIS_URL")
BACKEND_URL = config("BACKEND_URL")
API_SECRET_KEY = config("API_SECRET_KEY")
ADMIN_GROUP_ID = int(config("ADMIN_GROUP_ID"))
