from config import Config
from algorithm import Calculator

if __name__ == '__main__':
    config = Config()
    config.init_config_from_local()
    calculator = Calculator(config)
    calculator.calculate()
    resultFile = open("result.txt", 'r')
    print(resultFile.read())
    resultFile.close()
