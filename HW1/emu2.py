import os
import json
import tarfile
import configparser
import argparse
import sys

class ShellEmulator:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.virtual_fs_path = self.extract_tar(self.config['filesystem'])
        self.current_dir = self.virtual_fs_path
        self.log_data = []

    def load_config(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        return config['DEFAULT']

    def extract_tar(self, tar_path):
        temp_dir = 'virtual_fs'
        os.makedirs(temp_dir, exist_ok=True)
        with tarfile.open(tar_path, 'r') as tar:
            tar.extractall(path=temp_dir)
        return temp_dir

    def ls(self):
        return os.listdir(self.current_dir)

    def cd(self, dir_name):
        if dir_name == "..":
            # Переход на уровень выше
            parent_dir = os.path.dirname(self.current_dir)
            if parent_dir.startswith(self.virtual_fs_path):  # Проверка, чтобы не выйти за пределы виртуальной ФС
                self.current_dir = parent_dir
                self.log_action({'command': 'cd', 'directory': dir_name, 'status': 'success'})
            else:
                self.log_action(
                    {'command': 'cd', 'directory': dir_name, 'status': 'failure', 'error': 'Already at root'})
        else:
            new_path = os.path.join(self.current_dir, dir_name)
            if os.path.isdir(new_path):
                self.current_dir = new_path
                self.log_action({'command': 'cd', 'directory': dir_name, 'status': 'success'})
            else:
                self.log_action(
                    {'command': 'cd', 'directory': dir_name, 'status': 'failure', 'error': 'Not a directory'})

    def exit(self):
        self.log_actions_to_file()
        sys.exit()

    def chmod(self, mode, file_name):
        file_path = os.path.join(self.current_dir, file_name)
        try:
            # Устанавливаем права файла в восьмеричном формате
            os.chmod(file_path, int(mode, 8))
            self.log_action({'command': 'chmod', 'file': file_name, 'mode': mode, 'status': 'success'})
        except Exception as e:
            self.log_action({'command': 'chmod', 'file': file_name, 'mode': mode, 'status': 'failure', 'error': str(e)})

    def mv(self, source, destination):
        source_path = os.path.join(self.current_dir, source)
        dest_path = os.path.join(self.current_dir, destination)
        try:
            os.rename(source_path, dest_path)
            self.log_action({'command': 'mv', 'source': source, 'destination': destination, 'status': 'success'})
        except Exception as e:
            self.log_action({'command': 'mv', 'source': source, 'destination': destination, 'status': 'failure', 'error': str(e)})

    def rmdir(self, dir_name):
        dir_path = os.path.join(self.current_dir, dir_name)
        try:
            os.rmdir(dir_path)
            self.log_action({'command': 'rmdir', 'directory': dir_name, 'status': 'success'})
        except Exception as e:
            self.log_action({'command': 'rmdir', 'directory': dir_name, 'status': 'failure', 'error': str(e)})

    def log_action(self, action):
        self.log_data.append(action)

    def log_actions_to_file(self):
        with open(self.config['logfile'], 'w') as log_file:
            json.dump(self.log_data, log_file, indent=4)

    def run(self):
        while True:
            command = input(f"{self.current_dir}> ").strip().split()
            if not command:
                continue
            cmd = command[0]
            args = command[1:]

            if cmd == 'ls':
                print(self.ls())
            elif cmd == 'cd':
                if args:
                    self.cd(args[0])
                else:
                    print("cd: missing argument")
            elif cmd == 'exit':
                self.exit()
            elif cmd == 'chmod':
                if len(args) == 2:
                    self.chmod(args[0], args[1])
                else:
                    print("chmod: missing arguments")
            elif cmd == 'mv':
                if len(args) == 2:
                    self.mv(args[0], args[1])
                else:
                    print("mv: missing arguments")
            elif cmd == 'rmdir':
                if args:
                    self.rmdir(args[0])
                else:
                    print("rmdir: missing argument")
            else:
                print(f"{cmd}: command not found")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='Path to configuration file')
    args = parser.parse_args()

    shell = ShellEmulator(args.config)
    shell.run()
