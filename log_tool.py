import logging

class Mylog:
    def __init__(self, log_name):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler = logging.FileHandler(f'./logs/{log_name}.log')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def log_message(self, message):
        self.logger.info(message)
        print(f"Log message: {message}")