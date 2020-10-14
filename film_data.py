import logging
import os
from dataclasses import dataclass, field
from typing import List, Optional, Iterable

from config import SUPPORTED_FORMATS

class MovieData:
    file_path: str
    file_name: str

    def __init__(self, full_path: str):
        self.file_name = os.path.basename(full_path)
        self.file_path = full_path


@dataclass
class MovieBundleData:
    relative_directory: str
    absolute_directory: str
    sample: Optional[MovieData] = None
    files: List[MovieData] = field(default_factory=list)

    def parse_files(self, files: Iterable[str]) -> bool:
        for f in files:
            if not _is_format_supported(f):
                continue
            if "SAMPLE" in f.upper():
                if self.sample is not None:
                    logging.warning("Multiple sample files found in folder.")
                self.sample = MovieData(os.path.join(self.absolute_directory,
                                                     f))
            else:
                self.files.append(
                        MovieData(os.path.join(self.absolute_directory, f)))
        if not self.files and self.sample is not None:
            logging.warning("Only sample found in directory")
            self.files.append(self.sample)
        return self.files != []

    def debug_print(self):
        for f in self.files:
            logging.debug(f.file_name)


@dataclass
class MovieDatabase:
    root: str
    filmBundles: List[MovieBundleData] = field(default_factory=list)

    def add_films(self, path: str, files: Iterable[str]):
        rel_path = path[len(self.root):]
        bundle = MovieBundleData(relative_directory=rel_path,
                                 absolute_directory=path)
        if not bundle.parse_files(files):
            return
        self.filmBundles.append(bundle)


def _is_format_supported(file_name: str) -> bool:
    for sup in SUPPORTED_FORMATS:
        if file_name.endswith(sup):
            return True
    return False


def parse_tree(path: str) -> MovieDatabase:
    db = MovieDatabase(root=path)
    for root, _, files in os.walk(path):
        db.add_films(root, files)
    return db
