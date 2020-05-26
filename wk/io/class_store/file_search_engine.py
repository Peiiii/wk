from .fs_handles import FakeOS
import re

class FileSearchEngine(FakeOS):
    def __init__(self,path):
        super().__init__(path)
        self.files=self.get_all_files()
    def refresh_cache(self):
        self.files=self.get_all_files()
    def get_all_files(self):
        return self.glob('./**/*.*',recursive=True)
    def search(self,keywords,match_all=True):
        fs=self.files
        if match_all:
            for word in keywords:
                fs=list(filter(lambda f:re.findall(word,f),fs))
            return fs
        else:
            def match(text,ptns):
                for ptn in ptns:
                    if re.findall(ptn,text):return True
                return False
            fs=list(filter(lambda f:match(f,keywords),fs))
            return fs

