import yaml

from src.utils.file_util import open_file

if __name__ == "__main__":

    config_file = open_file('../config.yaml')
    configs = yaml.safe_load(config_file)
    print(configs)

