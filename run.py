import sys
import os

# Tambahkan direktori root proyek ke sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from comic_reader.main import main

if __name__ == "__main__":
    main()
