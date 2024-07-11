import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from move_images import move_file
import os
import shutil


class TestMoveFile(unittest.TestCase):

    @patch.object(Path, "is_file")
    @patch.object(Path, "mkdir")
    def test_file_doesnt_exist(self, mkdir_mock, is_file_mock):
        is_file_mock.return_value = False
        move_file('fake_src_path', 'fake_dest_path')
        is_file_mock.assert_called_once()
        mkdir_mock.assert_not_called()

    @patch('os.path.isfile')
    @patch.object(shutil, "move")
    @patch('os.path.basename')
    @patch('os.path.join')
    @patch.object(Path, "is_file")
    @patch.object(Path, "mkdir")
    def test_file_already_exists_at_destination(self, mkdir_mock, is_file_mock, os_join_mock, os_basename_mock, 
                                                shutil_move_mock, os_isfile_mock):
        is_file_mock.return_value = True
        os_isfile_mock.return_value = True
        os_join_mock.return_value = 'fake_join_path'
        os_basename_mock.return_value = 'fake_basename'
        move_file('fake_src_path', 'fake_dest_path')
        is_file_mock.assert_called_once()
        mkdir_mock.assert_called_once()
        os_basename_mock.assert_called_once()
        os_join_mock.assert_called_once()
        os_isfile_mock.assert_called_once()
        shutil_move_mock.assert_not_called()

    @patch('os.path.isfile')
    @patch.object(shutil, "move")
    @patch('os.path.basename')
    @patch('os.path.join')
    @patch.object(Path, "is_file")
    @patch.object(Path, "mkdir")
    def test_successful_move_of_file(self, mkdir_mock, is_file_mock, os_join_mock, os_basename_mock, 
                                     shutil_move_mock, os_isfile_mock):
        is_file_mock.return_value = True
        os_isfile_mock.return_value = False
        os_join_mock.return_value = 'fake_join_path'
        os_basename_mock.return_value = 'fake_basename'
        move_file('fake_src_path', 'fake_dest_path')
        is_file_mock.assert_called_once()
        mkdir_mock.assert_called_once()
        os_basename_mock.assert_called_once()
        os_join_mock.assert_called_once()
        os_isfile_mock.assert_called_once()
        shutil_move_mock.assert_called_once_with('fake_src_path', 'fake_join_path')


if __name__ == '__main__':
    unittest.main()
