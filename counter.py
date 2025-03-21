import threading
from pynput import keyboard, mouse
import sys
import time

class Counter:
    def __init__(self,username,config, logger):
        self.username = username
        self.config = config
        self.logger = logger

        self.key_press_count = 0
        self.mouse_click_count = 0

    def on_key_press(self, key):
        self.key_press_count += 1
        print(f'Клавиш нажато: {self.key_press_count}')
        self.logger.log_info(f"нажал клавишу ({key}).")

        if key == keyboard.Key.shift:
            print("Клавиша SHIFT была нажата, работа программы окончена")
            self.logger.log_info("завершил программу (нажал SHIFT).")
            self.stop_listening() 
            self.save_results()
            time.sleep(1)
            sys.exit()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.mouse_click_count += 1
            print(f'Кликов мыши: {self.mouse_click_count}')
            self.logger.log_info(f"кликнул мышью ({button}).")

    def start_listening(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()
    
    def stop_listening(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()

    def save_results(self):
        results = {
            "username": self.username,
            "key_press_count": self.key_press_count,
            "mouse_click_count": self.mouse_click_count
        }

        def save_async(results):
            try:    
                self.config.save_results(results)
                print("Результаты успешно сохранены.")
                self.logger.log_info("сохранил результаты работы.")
            except Exception as e:
                print(f"Ошибка при сохранении результатов: {e}")
                self.logger.log_error("counter.py", f"Ошибка при сохранении: {e}")

        save_thread = threading.Thread(target=save_async,  args=(results,))
        save_thread.start()
        save_thread.join()  

