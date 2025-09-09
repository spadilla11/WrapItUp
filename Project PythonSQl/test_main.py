import unittest
import os
import sqlite3
from unittest.mock import patch

# Import functions (update 'your_script' with the actual filename without '.py')
from main import (
    clear_screen,
    get_gift,
    save_user_info,
    read_file,
    save_ideas,

)

class TestGiftFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup test DB
        cls.db_name = "mydb.db"
        cls.conn = sqlite3.connect(cls.db_name)
        cursor = cls.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gift_idea (
                gift_name TEXT,
                gender TEXT,
                age TEXT,
                occasion TEXT,
                interest TEXT
            )
        ''')
        cursor.execute("DELETE FROM gift_idea")  # clear
        cursor.executemany('INSERT INTO gift_idea VALUES (?, ?, ?, ?, ?)', [
            ("Football", "M", "T", "B", "S"),
            ("Necklace", "F", "A", "W", "A")
        ])
        cls.conn.commit()

    def test_clear_screen(self):
        with patch("os.system") as mock_sys:
            clear_screen()
            mock_sys.assert_called_once()

    def test_get_gift_found(self):
        result = get_gift("M", "T", "B", "S")
        self.assertEqual(result, ["Football"])

    def test_get_gift_not_found(self):
        result = get_gift("F", "Y", "G", "P")
        self.assertEqual(result, [])

    def test_save_user_info_creates_file(self):
        name = "testuser"
        save_user_info(name, "F", "A", "W", "A")
        file_path = f"gift-getting_folder/{name}-gift"
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, "r") as f:
            content = f.read()
            self.assertIn("Name:testuser", content)
        os.remove(file_path)

    def test_read_file_prints_lines(self):
        name = "readtest"
        folder = "gift-getting_folder"
        os.makedirs(folder, exist_ok=True)
        file_path = f"{folder}/{name}-gift"
        with open(file_path, "w") as f:
            for i in range(10):
                f.write(f"Line {i}\n")
        with patch("builtins.input", return_value=name):
            with patch("builtins.print") as mock_print:
                read_file()
                mock_print.assert_any_call("Line 6")
        os.remove(file_path)

    def test_save_ideas_appends_correctly(self):
        name = "ideatest"
        folder = "gift-getting_folder"
        os.makedirs(folder, exist_ok=True)
        file_path = f"{folder}/{name}-gift"
        with open(file_path, "w") as f:
            f.write("Initial info\n")

        gift_list = ["Watch", "Book", "Backpack"]
        with patch("builtins.input", return_value="1 3"):
            save_ideas(name, gift_list)

        with open(file_path, "r") as f:
            content = f.read()
        self.assertIn("-Watch", content)
        self.assertIn("-Backpack", content)
        os.remove(file_path)

if __name__ == "__main__":
    unittest.main()
