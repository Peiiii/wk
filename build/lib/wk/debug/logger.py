
class LoggerFile:
    def __init__(self,path,recreate=False):
        self.path=path
        if recreate:
            self.recreate()
    def recreate(self):
        with open(self.path,'w') as f:
            pass
    def _push(self,text):
        with open(self.path,'a') as f:
            f.write(text)
    def log(self,*msgs):
        print(*msgs)
        self.logtofile(*msgs)
    def logtofile(self,*msgs):
        msgs = [str(msg) if hasattr(msg, '__str__') else repr(msg) for msg in msgs]
        msgs = ' '.join(msgs)+'\n'
        self._push(msgs)

