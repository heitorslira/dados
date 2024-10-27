from unittest import TestCase
import pathlib

from typing import Iterator
import io


def last_lines(file_path: str, buffer_size: int = io.DEFAULT_BUFFER_SIZE) -> Iterator[str]:
    with open(file_path, 'r',encoding='utf-8') as file:
        file.seek(0, io.SEEK_END)
        pos = file.tell()
        while pos > 0:
            read_size = min(buffer_size, pos)
            new_possible_pos = pos - read_size
            pos = max(0, new_possible_pos)  # Cannot be negative
            file.seek(pos, io.SEEK_SET)
            
            remaining_read_file = file.read(read_size)
            while True:
                pos_add = len(remaining_read_file)
                new_lines_indexes = [i for i, char in enumerate(remaining_read_file) if char == '\n']
                new_lines_indexes = [i-len(remaining_read_file) for i in new_lines_indexes if i-len(remaining_read_file)<-1 ]
                if not new_lines_indexes:
                    yield remaining_read_file
                    pos_add = 0
                    break
                next_pos = new_lines_indexes.pop()
                yield remaining_read_file[next_pos+1:]
                remaining_read_file = remaining_read_file[:next_pos+1]
                # new_lines_indexes = [i for i, char in enumerate(remaining_read_file) if char == '\n']
            
            
            # number_of_lines = len(new_lines_indexes)
            # if number_of_lines <= 1:
            #     yield remaining_read_file
            # next_pos = new_lines_indexes.pop(0)
            # reversed_indexes = [i-len(remaining_read_file) for i in new_lines_indexes]
            
            # while reversed_indexes:
            #     end = reversed_indexes.pop()
            #     start = reversed_indexes.pop()
            #     if end+1 == 0:
            #         yield remaining_read_file[start+1:]
                
            #     end = start
            #     start = reversed_indexes.pop()
            #     yield remaining_read_file[start+1:end+1]
                    
                
                
                    
            pos = pos + pos_add
    

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

    def test_last_line_yields_from_last_to_first_my_file4(self):
        file_path = self.file_folder/'my_file4.txt'
        lines = last_lines(file_path)
        line1= next(lines)
        line2 = next(lines)
        line3 = next(lines)
        self.assertEqual(line1, 'Agora com um tipo_especial\n')
        self.assertEqual(line2, 'E esta é a linha 2 tão grande\n')
        self.assertEqual(line3, 'Essa é a linha 1\n')
        
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

        self.assertLessEqual(len(line1_bytes), buffer_size)
        self.assertLessEqual(len(line2_bytes), buffer_size)

    def test_last_line_reads_file5(self):
        test_file_path = self.file_folder / 'my_file5.txt'
        buffer_size = 20
        lines = last_lines(test_file_path, buffer_size)
        
        for line in lines:
            in_bytes = bytes(line, 'utf-8')
            self.assertLessEqual(len(in_bytes), buffer_size)

    def test_last_line_reads_file6(self):
        test_file_path = self.file_folder / 'my_file6.txt'
        buffer_size = 300
        lines = last_lines(test_file_path,buffer_size)
        line1 = next(lines)
        line2 = next(lines)
        line3 = next(lines)
        line4 = next(lines)
        line5 = next(lines)
        line6 = next(lines)
        line7 = next(lines)
        line8 = next(lines)
        
        self.assertEqual(line1, 'minha função funciona em casos extremos\n')
        self.assertEqual(line2, 'poderei ver como\n')
        self.assertEqual(line3, 'desta forma\n')
        self.assertEqual(line5, 'sem esquecer de usar alguns caracteres especiais\n')
        self.assertEqual(line6, 'de tamanha variado\n')
        self.assertEqual(line4, 'como por exemplo é o ã\n')
        self.assertEqual(line7, 'coloco um texto\n')
        self.assertEqual(line8, 'Neste arquivo\n')
        
        
# Neste arquivo
# coloco um texto
# de tamanha variado
# sem esquecer de usar alguns caracteres especiais
# como por exemplo é o ã
# desta forma
# poderei ver como
# minha função funciona em casos extremos
            
        
    
        
        
        
