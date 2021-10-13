from game_clock import GameClock

import unittest
import time

class TestGameClock(unittest.TestCase):

    def test_init(self):
        clock = GameClock()

    def test_start(self):
        clock = GameClock()
        clock.start()
        self.assertNotEqual(clock.timer1.time, None)
        self.assertEqual(clock.timer2.time, None)

        clock.init()
        clock.start()
        time.sleep(3)
        self.assertEqual(clock.timer1.get_counter(), 17)
        self.assertEqual(clock.timer2.get_counter(), 20)

    def test_next(self):
        clock = GameClock()
        clock.start()
        time.sleep(3)
        clock.next()
        time.sleep(5)
        clock.interrupt()
        self.assertEqual(clock.timer1.get_counter(), 17)
        self.assertEqual(clock.timer2.get_counter(), 15)

    def test_next_fischer(self):
        clock = GameClock(20, 20)
        clock.start()
        time.sleep(3)
        clock.next()
        time.sleep(5)
        clock.next()
        clock.interrupt()
        self.assertEqual(clock.timer1.get_counter(), 37)
        self.assertEqual(clock.timer2.get_counter(), 35)

    def test_counters(self):
        clock = GameClock(20, 20)
        clock.start()
        time.sleep(3)
        clock.next()
        time.sleep(5)
        clock.next()
        self.assertEqual(clock.get_counters(), [37, 35])

