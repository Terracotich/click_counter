from authenticate import Authenticate

class Registration:
    def __init__(self, config):
        self.config = config

    def registration(self):
        while True:
            username = input("Введите логин: ")
            password = input("Введите пароль: ")

            if any(user['username'] == username for user in self.config.load_users()):
                print(f"Ошибка: пользователь с логином {username} уже существует")
            else:
                self.config.users.append({"username" : username, "password" : password})
                self.config.save_users()
                print("Регистрация прошла успешно!")
                auth = Authenticate(self.config)
                auth.authenticate()
                break


