import os
from dataclasses import dataclass


@dataclass
class Paths:
    STORAGE: str = os.path.dirname(__file__) + "/storage/files.json"
    TEMP_FILES: str = os.path.dirname(__file__) + "/temp_files/"
