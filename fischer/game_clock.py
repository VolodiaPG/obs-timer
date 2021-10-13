from .timer import Timer

class GameClock(object):

    def __init__(self, counter = 20, fischer = 0):
        self._counter = counter
        self._fischer = fischer
        self.init()

    def init(self):
        self.timer1 = Timer(self._counter, self._fischer)
        self.timer2 = Timer(self._counter, self._fischer)

    def start(self):
        self.timer1.start()

    def next(self):
        if(self.timer1.time == self.timer2.time == None):
            self.timer1.start()
        else:
            self.timer1.start_stop()
            self.timer2.start_stop()

    def interrupt(self):
        self.timer1.interrupt()
        self.timer2.interrupt()

    def get_counters(self):
        return [ self.timer1.get_formatted_counter(),
                 self.timer2.get_formatted_counter(),
                 self.turn_id() ]

    def turn_id(self):
        if self.timer1.time == None:
            if self.timer2.time == None:
                return 1
            else:
                return 2
        else:
            if self.timer2.time == None:
                return 1

        raise Warning('The 2 timers are started at the same time')





