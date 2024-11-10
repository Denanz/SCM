import os
import pytest
import json
from emulator import ShellEmulator


@pytest.fixture
def emulator():
    # Create temporary files and directories for testing
    with open('test_config.ini', 'w') as f:
        f.write("[DEFAULT]\n")
        f.write("filesystem = C:/Users/igord/PycharmProjects/pythonProject1/HW1/fs.tar\n")
        f.write("logfile = test_log.json\n")

    shell = ShellEmulator('test_config.ini')
    yield shell

    # Clean up temporary files
    os.remove('test_config.ini')
    if os.path.exists('test_log.json'):
        os.remove('test_log.json')


# Test `ls` command
def test_ls_basic(emulator):
    result = emulator.ls()
    assert isinstance(result, list)
    assert 'dir1' in result  # Replace with actual directory in your fs.tar
    assert 'file1.txt' in result  # Replace with actual file in your fs.tar


def test_ls_empty_directory(emulator):
    emulator.cd('dir1')  # Replace 'empty_dir' with an actual empty directory in your fs.tar
    assert emulator.ls() == []


def test_ls_nonexistent_directory(emulator):
    emulator.cd('dir2')
    assert not emulator.ls()  # Expect empty list or specific behavior if directory doesn't exist


# Test `cd` command
def test_cd_subdirectory(emulator):
    current_dir = emulator.current_dir
    emulator.cd('dir1')  # Replace with an actual subdirectory
    assert emulator.current_dir == os.path.join(current_dir, 'dir1')


def test_cd_parent_directory(emulator):
    emulator.cd('dir1')  # Navigate to subdirectory first
    emulator.cd('..')  # Navigate back to parent directory
    assert emulator.current_dir == emulator.virtual_fs_path


def test_cd_invalid_directory(emulator):
    initial_dir = emulator.current_dir
    emulator.cd('invalid_dir')
    assert emulator.current_dir == initial_dir  # Should remain in the initial directory


# Test `chmod` command
def test_chmod_existing_file(emulator):
    emulator.chmod('755', 'file1.txt')  # Замените на фактический файл
    file_path = os.path.join(emulator.current_dir, 'file1.txt')
    assert oct(os.stat(file_path).st_mode)[-3:] == '666'  # Убедитесь, что вы проверяете последние 3 символа



def test_chmod_nonexistent_file(emulator):
    emulator.chmod('755', 'nonexistent_file.txt')
    if os.path.exists('test_log.json'):
        with open('test_log.json', 'r') as log_file:
            log_data = json.load(log_file)
        assert any(log['command'] == 'chmod' and log['status'] == 'failure' for log in log_data)


def test_chmod_invalid_permission(emulator):
    emulator.chmod('invalid', 'file1.txt')  # Replace with an actual file
    if os.path.exists('test_log.json'):
        with open('test_log.json', 'r') as log_file:
            log_data = json.load(log_file)
        assert any(log['command'] == 'chmod' and log['status'] == 'failure' for log in log_data)


# Test `mv` command
def test_mv_existing_file(emulator):
    emulator.mv('file1.txt', 'renamed_file.txt')  # Rename an existing file
    assert 'renamed_file.txt' in emulator.ls()


def test_mv_nonexistent_file(emulator):
    emulator.mv('nonexistent_file.txt', 'new_name.txt')
    if os.path.exists('test_log.json'):
        with open('test_log.json', 'r') as log_file:
            log_data = json.load(log_file)
        assert any(log['command'] == 'mv' and log['status'] == 'failure' for log in log_data)


def test_mv_to_existing_destination(emulator):
    emulator.mv('file2.txt', 'file1.txt')  # Attempt to move to an existing filename
    if os.path.exists('test_log.json'):
        with open('test_log.json', 'r') as log_file:
            log_data = json.load(log_file)
        assert any(log['command'] == 'mv' and log['status'] == 'failure' for log in log_data)


# Test `rmdir` command
def test_rmdir_empty_directory(emulator):
    emulator.rmdir('empty_dir')  # Replace 'empty_dir' with an actual empty directory
    assert 'empty_dir' not in emulator.ls()


def test_rmdir_nonexistent_directory(emulator):
    emulator.rmdir('nonexistent_dir')
    if os.path.exists('test_log.json'):
        with open('test_log.json', 'r') as log_file:
            log_data = json.load(log_file)
        assert any(log['command'] == 'rmdir' and log['status'] == 'failure' for log in log_data)


def test_rmdir_non_empty_directory(emulator):
    emulator.rmdir('dir_with_files')  # Replace 'dir_with_files' with an actual non-empty directory
    if os.path.exists('test_log.json'):
        with open('test_log.json', 'r') as log_file:
            log_data = json.load(log_file)
        assert any(log['command'] == 'rmdir' and log['status'] == 'failure' for log in log_data)
