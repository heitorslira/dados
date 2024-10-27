from unittest import TestCase
import pathlib

from typing import Iterator
import io


def last_lines(file_path: str, buffer_size: int = io.DEFAULT_BUFFER_SIZE) -> Iterator[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        file.seek(0, io.SEEK_END)
        pos = file.tell()
        while pos > 0:
            read_size = min(buffer_size, pos)
            new_possible_pos = pos - read_size
            pos = max(0, new_possible_pos)  # Cannot be negative
            file.seek(pos, io.SEEK_SET)
            # lines = []
            read_file = file.read(read_size) 
            lines = []
            for line in file.readline(read_size):
                lines.append(line)
            
            lines.reverse()
            for line in lines:
                yield line
                
    

class TestLastLines(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_folder = pathlib.Path(__file__).parent / 'test_files'
    
    #test if returns an iterator
    def test_last_line_returns_iterator(self):
        file_path = self.file_folder/'my_file1.txt'
        lines = last_lines(file_path)
        self.assertIsInstance(lines, Iterator)
        
    def test_last_line_yields_string(self):
        file_path = self.file_folder/'my_file1.txt'
        lines = last_lines(file_path)
        self.assertIsInstance(next(lines), str)
        
    def test_last_line_yields_from_last_to_first(self):
        file_path = self.file_folder/'my_file1.txt'
        lines = last_lines(file_path)
        self.assertEqual(next(lines), 'And this is line 3\n')
        self.assertEqual(next(lines), 'This is line 2\n')
        self.assertEqual(next(lines), 'This is a file\n')
        
    def test_last_line_yields_from_last_to_first_my_file2(self):
        file_path = self.file_folder/'my_file2.txt'
        lines = last_lines(file_path)
        self.assertEqual(next(lines), 'This is a file\n')
        self.assertEqual(next(lines), 'This is line 2\n')
        self.assertEqual(next(lines), 'And this is line 3\n')
        
    def test_last_line_accepts_buffer_size(self):
        file_path = self.file_folder/'my_file2.txt'
        lines = last_lines(file_path, 10)
        
        #not raises exception
        self.assertTrue(True)
        
    def test_last_line_reads_buffersize(self):
        test_file_path = self.file_folder / 'test_file.txt'
        buffer_size=20
        row_string = 'a'*(buffer_size)
        with open(test_file_path,'w', encoding='utf-8') as f:
            f.write(row_string)
        lines = last_lines(test_file_path,buffer_size)
        line1 = next(lines)
        
        line1_bytes = bytes(line1,'utf-8')
        
        self.assertEqual(line1,'a'*buffer_size)
        self.assertLessEqual(len(line1_bytes),buffer_size)

    def test_last_line_reads_buffersize_or_less(self):
        test_file_path = self.file_folder / 'test_file.txt'
        buffer_size = 20
        row_string = 'a' * (buffer_size + 1)
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(row_string)
        lines = last_lines(test_file_path, buffer_size)
        line1 = next(lines)
        line2 = next(lines)

        line1_bytes = bytes(line1, 'utf-8')
        line2_bytes = bytes(line2, 'utf-8')

        self.assertEqual(line1, 'a' * buffer_size)
        self.assertLessEqual(len(line1_bytes), buffer_size)
        self.assertEqual(line2, 'a' * 1)
        self.assertLessEqual(len(line2_bytes), buffer_size)
            
        
    
        
        
        
