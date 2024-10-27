from typing import Iterator
import io
from pathlib import Path


def last_lines(
    file_path: str, buffer_size: int = io.DEFAULT_BUFFER_SIZE
) -> Iterator[str]:
    with open(file_path, "r", encoding="utf-8") as file:
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
                new_lines_indexes = [
                    i for i, char in enumerate(remaining_read_file) if char == "\n"
                ]
                new_lines_indexes = [
                    i - len(remaining_read_file)
                    for i in new_lines_indexes
                    if i - len(remaining_read_file) < -1
                ]
                if not new_lines_indexes:
                    yield remaining_read_file
                    pos_add = 0
                    break
                next_pos = new_lines_indexes.pop()
                yield remaining_read_file[next_pos + 1 :]
                remaining_read_file = remaining_read_file[: next_pos + 1]
            pos = pos + pos_add


def main():
    file_path = Path(__file__).parent / "my_file.txt"
    for line in last_lines(file_path):
        print(line, end="")


if __name__ == "__main__":
    main()
