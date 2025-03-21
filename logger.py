import threading
import time

class Logger:
    def __init__(self, config, username="SYSTEM"):
        self.config = config
        self.username = username
        self.log_queue = []  
        self.lock = threading.Lock()
        self.running = True

        self.thread = threading.Thread(target=self._log_worker, daemon=True)
        self.thread.start()

    def _log_worker(self):
        while self.running or self.log_queue:
            if self.log_queue:
                with self.lock:
                    logs_to_write = self.log_queue[:]
                    self.log_queue.clear()

                for log in logs_to_write:
                    self.config.save_log(*log)  

            time.sleep(0.5)

    def log_info(self, action):
        with self.lock:
            self.log_queue.append(("INFO", self.username, action))

    def log_error(self, location, error):
        with self.lock:
            self.log_queue.append(("ERROR", self.username, f"{location}: {error}"))

    def stop(self):
        self.running = False
        self.thread.join()