import time,functools

class Timer:
    def __init__(self, verbose=True,msg=None,mute=None):
        self.history = []
        self.dt_history = []
        self.steps = 0
        self.start_time = time.time()
        self.history.append(self.start_time)
        self.verbose = verbose
        self.mute=mute
        if self.verbose:
            self.print('Timer started at %s' % (self.start_time))
        if msg:
            self.print(msg)
    def print(self,*args,**kwargs):
        if not self.mute:
            print(*args,**kwargs)
    def step(self,msg=None):
        t = time.time()
        dt = t - self.history[-1]
        self.dt_history.append(dt)
        self.history.append(t)
        self.steps += 1
        if self.verbose:
            self.print('step=%s , %s time since last step: %s' % (self.steps,'msg=%s'%(msg) if msg else '',dt))
        return dt
    def mean(self):
        if not len(self.dt_history):return None
        return sum(self.dt_history)/len(self.dt_history)
    def plot_dt_history(self,title='Timer History',*args,**kwargs):
        from matplotlib import pyplot as plt
        plt.plot(self.dt_history)
        plt.show(title=title,*args,**kwargs)

    def end(self):
        t = time.time()
        self.end_time = t
        dt = t - self.history[-1]
        self.dt_history.append(dt)
        self.history.append(t)
        self.steps += 1
        if self.verbose:
            self.print('time since last step: %s' % (dt))
        return dt
DEFALUT_TIMER=None
def timer_step(msg=None):
    global DEFALUT_TIMER
    if not DEFALUT_TIMER:
        DEFALUT_TIMER=Timer()
    else:
        DEFALUT_TIMER.step(msg)


def run_timer(func):
    name = func.__name__

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('running %s ...' % (name))
        t = Timer(verbose=False)
        ret = func(*args, **kwargs)
        dt = t.end()
        print('finished running %s ,time consumed: %s' % (name, dt))
        return ret
    return wrapper

