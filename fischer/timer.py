import time

class Timer(object):

    def __init__(self, counter = 20, fischer = 0):
        self.counter = counter
        self.fischer = fischer
        self.time = None

    def start(self):
        self.time = time.time()

    def stop(self):
        self.counter = self.get_counter() + self.fischer
        self.time = None

    def interrupt(self):
        self.counter = self.get_counter()
        self.time = None

    def start_stop(self):
        if (self.time == None):
            self.start()
        else:
            self.stop()

    def get_counter(self):
        if (self.time == None): return self.counter
        now = time.time()
        since = int(round(now - self.time))
        now_counter = self.counter - since
        return(0 if (now_counter < 0) else now_counter)

    def show(self):
        print(self.get_counter())

    def get_formatted_counter(self):
        counter = self.get_counter()
        minutes = counter / 60
        seconds = counter % 60
        return "{}:{}".format(str(minutes).zfill(2), str(seconds).zfill(2))




