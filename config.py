import os

ROOT_DIR=os.path.dirname(__file__)
LOGS_DIR={"web_page_logs": os.path.join(ROOT_DIR, "logs", "web_page_data.log")}
DATA_DIR=os.path.join(ROOT_DIR, "data", "operations.xlsx")
USER_SETTINGS_DIR=os.path.join(ROOT_DIR, "user_settings.json")
ENV_DIR=os.path.join(ROOT_DIR, ".env")
