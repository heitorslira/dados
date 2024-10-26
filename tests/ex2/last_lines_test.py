from unittest import TestCase
import pathlib

from typing import Iterator
import io


def last_lines(file_path:str)-> Iterator[str]:
    yield 'And this is line 3'
    yield 'This is line 2'
    yield 'This is a file'
    
    
class TestLastLines(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_folder = pathlib.Path(__file__).parent / 'test_files'
    
    #test if returns an iterator
    def test_last_line_returns_iterator(self):
        file_path = self.file_folder/'my_file.txt'
        lines = last_lines(file_path)
        self.assertIsInstance(lines, Iterator)
        
    def test_last_line_yields_string(self):
        file_path = self.file_folder/'my_file.txt'
        lines = last_lines(file_path)
        self.assertIsInstance(next(lines), str)
        
    def test_last_line_yields_from_last_to_first(self):
        file_path = self.file_folder/'my_file.txt'
        lines = last_lines(file_path)
        self.assertEqual(next(lines), 'And this is line 3')
        self.assertEqual(next(lines), 'This is line 2')
        self.assertEqual(next(lines), 'This is a file')
        
    def test_last_line_yields_from_last_to_first_my_file2(self):
        file_path = self.file_folder/'my_file2.txt'
        lines = last_lines(file_path)
        self.assertEqual(next(lines), 'This is a file')
        self.assertEqual(next(lines), 'This is line 2')
        self.assertEqual(next(lines), 'And this is line 3')
        
        
    
        
        
        
