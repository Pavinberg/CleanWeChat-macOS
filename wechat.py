from pathlib import Path
from typing import List, Tuple

__all__ = ["iter_dir_macos", "WeChatStructure"]


testMode = False


def iter_dir_macos(directory: Path):
    '''Iterate all files in directory but skip .DS_Store'''
    return filter(lambda d: d.name != ".DS_Store", directory.iterdir())


class WeChatStructure:

    wechatHome = Path.home() / "Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat" if not testMode else Path("test/wechatHome").absolute()

    def __init__(self):
        self.latestVerDir = Path()
        self.oldVerDirs = []
        self.latestHashDir = Path()
        self.oldHashDirs = []

        self.fit_structure()
                
    def fit_structure(self):
        self.fit_version_dir()
        self.fit_hash_dir()

    def fit_version_dir(self) -> None:
        self.latestVerDir, self.oldVerDirs = \
            self._filter_latest_dir(self.wechatHome, lambda d: not d.name.startswith("."))

    def fit_hash_dir(self) -> None:
        excludes = set(("Avatar", "CGI", "checkVersionFile", "CrashReport", "KeyValue", "MMappedKV", "MMResourceMgr", "nsid", "topinfo.data", "upgradeHistoryFile", "WeVoIP", "whatsNewVersionFile"))
        self.latestHashDir, self.oldHashDirs = \
            self._filter_latest_dir(self.latestVerDir,
                                    lambda d: not d.name.startswith(".") and not d in excludes and len(d.name) > 30)

    def glob_empty_message_dir(self):
        messageDir = self.latestHashDir / "Message/MessageTemp/"
        for subDir in iter_dir_macos(messageDir):
            if all(map(lambda d: d.is_dir(), subDir.glob("**/*"))): # subDir has no files
                yield subDir

    def get_latest_version_dir(self) -> Path:
        return self.latestVerDir

    def get_latest_message_dir(self) -> Path:
        return self.latestHashDir / "Message"

    def get_old_version_dirs(self) -> List[Path]:
        return self.oldVerDirs

    def get_old_hash_dirs(self) -> List[Path]:
        return self.oldHashDirs
    
    def _filter_latest_dir(self, baseDir, excludeFunc) -> Tuple[Path, List[Path]]:
        '''Get the latest version directory in `baseDir` and exclude dir in `excludes`
        Return: latest direcoty, [old directories...]
        '''
        latestTime, latestDir = 0, None
        oldDirs = []
        for directory in filter(excludeFunc, baseDir.iterdir()): # skip hidden files and excludes
            if directory.stat().st_mtime > latestTime:
                if latestDir:
                    oldDirs.append(latestDir)
                latestTime = directory.stat().st_mtime
                latestDir = directory
            else:
                oldDirs.append(directory)

        return latestDir, oldDirs
