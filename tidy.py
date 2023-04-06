'''Utilitiy functions to tidy trash to a tmp direcory'''


import time
import json
from pathlib import Path
import shutil
import subprocess
from wechat import WeChatStructure, iter_dir_macos

__all__ = ["tidy"]


DEFAULT_FILE_MODE = 0o700
trashDir = Path.home() / ".Trash"


def create_tmp_dir(baseDir=Path("/tmp/"), rand=True) -> Path:
    name = "cleanWechat-macOS"
    if rand:
        name += f"-{int(time.time())}"
    tmpDir = baseDir / name
    tmpDir.mkdir(mode=DEFAULT_FILE_MODE)
    return tmpDir        


def delete_dir(dirName: Path):
    '''Delete directory even if it is not empty'''
    shutil.rmtree(dirName)


def move_into(path: Path, target: Path):
    path.rename(target / path.name)
    

class TidyStructure:

    def __init__(self, baseDir=Path("/tmp/"), rand=True):
        self.tidyDir: Path = create_tmp_dir(baseDir, rand)
        self.wechatStructure = WeChatStructure()
        self.metadata = {
            "wechat_home": str(self.wechatStructure.wechatHome),
            "latest_version": str(self.wechatStructure.get_latest_version_dir()),
            "latest_hash": str(self.wechatStructure.latestHashDir)
        }

    def tidy_dirs_to(self, dirs, tidySubDir):
        '''Create symlink in `tidySubDir` to old versions directories'''
        tidySubDir.mkdir(mode=DEFAULT_FILE_MODE, exist_ok=True)
        for d in dirs:
            tname = tidySubDir / d.name
            tname.symlink_to(d)

    def tidy(self):
        self.tidy_dirs_to(self.wechatStructure.get_old_version_dirs(), self.tidyDir / "old_versions")
        self.tidy_dirs_to(self.wechatStructure.get_old_hash_dirs(), self.tidyDir / "old_hashes")

        self.tidy_dirs_to(self.wechatStructure.glob_empty_message_dir(), self.tidyDir / "empty")
        self.dump_metadata()

    def dump_metadata(self, filename="metadata.json"):
        '''Dump metadata to filename'''
        with open(self.tidyDir / filename, 'w') as fp:
            json.dump(self.metadata, fp, indent=2)

    def open_tidy_dir(self):
        subprocess.run(["open", self.tidyDir])

    def clean_up(self):
        trashPath = trashDir / self.tidyDir.name
        trashPath.mkdir(mode=DEFAULT_FILE_MODE)
        for subDir in iter_dir_macos(self.tidyDir):
            subTrashPath = trashPath / subDir.name
            subTrashPath.mkdir(mode=DEFAULT_FILE_MODE)
            for targetDir in iter_dir_macos(subDir):
                move_into(targetDir.resolve(), subTrashPath)
                
    def clear_tidy(self):
        delete_dir(self.tidyDir)
