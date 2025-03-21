class Authenticate:
    def __init__(self, config):
        self.config = config

    def authenticate(self):
        username = input("Введите логин: ")
        password = input("Введите пароль: ")
        return self.check_auth(username, password)

    def check_auth(self, username, password):
        for user in self.config.load_users():
            if user["username"] == username and user["password"] == password:
                print("Аутентификация успешна!")
                return username 
        print("Неверное имя пользователя или пароль")
        return None
        
        