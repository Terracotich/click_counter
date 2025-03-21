import json
import threading
from datetime import datetime

USERS = 'users.json'
RESULTS = 'results.json'
LOG_FILE = "app.log"

class Config():
    def __init__(self):
        self.users = self.load_users()
        self.results = self.load_results()
        self.lock = threading.Lock()

    
    def save_users(self):
        with open(USERS, 'w', encoding='utf-8') as file:    
            json.dump(self.users, file, indent=4)

    def load_users(self):
        try:
            with open(USERS, 'r', encoding='utf-8') as file:
                data = file.read()
                if not data: 
                    return []
                return json.loads(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    def save_results(self, results):
        try:
            with self.lock:
                existing_results = self.load_results()
                if not isinstance(existing_results, list):
                    existing_results = []
                existing_results.append(results)

                with open(RESULTS, 'w', encoding='utf-8') as file:
                    json.dump(existing_results, file, indent=4)
        except Exception as e:
            self.log_error(results["username"], "cfg.py", f"Ошибка сохранения: {e}")

    def load_results(self):
        try:
            with open(RESULTS, 'r', encoding='utf-8') as file:
                data = file.read()
                if not data:
                    return [] 
                results = json.loads(data)
                return results if isinstance(results, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    def save_log(self, level, username, message):
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        log_entry = f"[{level}] [{timestamp}] [{username}] – {message}"

        with self.lock:
            with open(LOG_FILE, "a", encoding="utf-8") as file:
                file.write(log_entry + "\n")
