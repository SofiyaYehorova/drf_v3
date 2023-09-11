from unittest import TestCase

from ..services import calc


class ServicesTestCase(TestCase):
    def test_plus(self):
        res = calc(1, 2, '+')
        self.assertEquals(res, 3)

    def test_minus(self):
        res = calc(5, 2, '-')
        self.assertEquals(res, 3)

    def test_multi(self):
        res = calc(2, 2, '*')
        self.assertEquals(res, 4)

    def test_division(self):
        res = calc(4, 2, '/')
        self.assertEquals(res, 2)
        