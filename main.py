from registration import Registration
from authenticate import Authenticate
from cfg import Config
from counter import Counter
from logger import Logger


def main():
    print("Добро пожаловать в счетчик кликов! ")
    config = Config()
    logger = Logger(config) 

    try:
        action = int(input("Выберите действие: \n"
                            "1 - вход \n"
                            "2 - регистрация \n"))
        if action == 1:
            auth = Authenticate(config)
            username = auth.authenticate()
            if username:
                logger.username = username
                logger.log_info("Вошел в систему")

                counter = Counter(username, config, logger)
                counter.start_listening()
                print("Для завершения программы нажмите клавишу SHIFT")
                while True:
                    pass
        elif action == 2:
            reg = Registration(config)
            reg.registration()
            logger.log_info("зарегистрировал новый аккаунт.")
        else:
            print("Ошибка ввода!")
            logger.log_error("main.py", "Некорректный ввод.")

    except ValueError as e:
        print("Введите число!")
        logger.log_error("main.py", f"Ошибка ValueError: {e}")


if __name__ == "__main__":
    main()  
