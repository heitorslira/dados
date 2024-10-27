import pathlib
from typing import Iterator
from unittest import TestCase

from src.ex2.ex2 import last_lines


class TestLastLines(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_folder = pathlib.Path(__file__).parent / "test_files"

    # test if returns an iterator
    def test_last_line_returns_iterator(self):
        file_path = self.file_folder / "my_file1.txt"
        lines = last_lines(file_path)
        self.assertIsInstance(lines, Iterator)

    def test_last_line_yields_string(self):
        file_path = self.file_folder / "my_file1.txt"
        lines = last_lines(file_path)
        self.assertIsInstance(next(lines), str)

    def test_last_line_yields_from_last_to_first(self):
        file_path = self.file_folder / "my_file1.txt"
        lines = last_lines(file_path)
        self.assertEqual(next(lines), "And this is line 3\n")
        self.assertEqual(next(lines), "This is line 2\n")
        self.assertEqual(next(lines), "This is a file\n")

    def test_last_line_yields_from_last_to_first_my_file2(self):
        file_path = self.file_folder / "my_file2.txt"
        lines = last_lines(file_path)
        self.assertEqual(next(lines), "This is a file\n")
        self.assertEqual(next(lines), "This is line 2\n")
        self.assertEqual(next(lines), "And this is line 3\n")

    def test_last_line_yields_from_last_to_first_my_file4(self):
        file_path = self.file_folder / "my_file4.txt"
        lines = last_lines(file_path)
        line1 = next(lines)
        line2 = next(lines)
        line3 = next(lines)
        self.assertEqual(line1, "Agora com um tipo_especial\n")
        self.assertEqual(line2, "E esta é a linha 2 tão grande\n")
        self.assertEqual(line3, "Essa é a linha 1\n")

    def test_last_line_accepts_buffer_size(self):
        file_path = self.file_folder / "my_file2.txt"
        lines = last_lines(file_path, 10)

        # not raises exception
        self.assertTrue(True)

    def test_last_line_reads_buffersize(self):
        test_file_path = self.file_folder / "test_file.txt"
        buffer_size = 20
        row_string = "a" * (buffer_size)
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(row_string)
        lines = last_lines(test_file_path, buffer_size)
        line1 = next(lines)

        line1_bytes = bytes(line1, "utf-8")

        self.assertEqual(line1, "a" * buffer_size)
        self.assertLessEqual(len(line1_bytes), buffer_size)

    def test_last_line_reads_buffersize_or_less(self):
        test_file_path = self.file_folder / "test_file.txt"
        buffer_size = 20
        row_string = "a" * (buffer_size + 1)
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(row_string)
        lines = last_lines(test_file_path, buffer_size)
        line1 = next(lines)
        line2 = next(lines)

        line1_bytes = bytes(line1, "utf-8")
        line2_bytes = bytes(line2, "utf-8")

        self.assertLessEqual(len(line1_bytes), buffer_size)
        self.assertLessEqual(len(line2_bytes), buffer_size)

    def test_last_line_reads_file5(self):
        test_file_path = self.file_folder / "my_file5.txt"
        buffer_size = 20
        lines = last_lines(test_file_path, buffer_size)

        for line in lines:
            in_bytes = bytes(line, "utf-8")
            self.assertLessEqual(len(in_bytes), buffer_size)

    def test_last_line_reads_file6(self):
        test_file_path = self.file_folder / "my_file6.txt"
        buffer_size = 300
        lines = last_lines(test_file_path, buffer_size)
        line1 = next(lines)
        line2 = next(lines)
        line3 = next(lines)
        line4 = next(lines)
        line5 = next(lines)
        line6 = next(lines)
        line7 = next(lines)
        line8 = next(lines)

        self.assertEqual(line1, "minha função funciona em casos extremos\n")
        self.assertEqual(line2, "poderei ver como\n")
        self.assertEqual(line3, "desta forma\n")
        self.assertEqual(line5, "sem esquecer de usar alguns caracteres especiais\n")
        self.assertEqual(line6, "de tamanha variado\n")
        self.assertEqual(line4, "como por exemplo é o ã\n")
        self.assertEqual(line7, "coloco um texto\n")
        self.assertEqual(line8, "Neste arquivo\n")


# Neste arquivo
# coloco um texto
# de tamanha variado
# sem esquecer de usar alguns caracteres especiais
# como por exemplo é o ã
# desta forma
# poderei ver como
# minha função funciona em casos extremos
