from parkingmeter_noui import *
from money import *
from datetime import *
import unittest

class ParkingMeterTest(unittest.TestCase):

    def setUp(self):
        self.root = ParkingMeterNoUI()

    def test_one(self):
        self.assertRaises(ValueError, self.root.changedate, "2021-10-10 99:99:99")
        self.root.changedate("2021-10-10 12:34:00")
        self.assertEqual(self.root.devicetime().strftime("%H:%M"), "12:34")

    def test_two(self):
        self.root.changedate("2021-10-7 9:00:00") #Ustawienie godziny by test zawierał się w jednym dniu
        self.root.buttonpln(2.0, "1")
        self.assertEqual(self.root.calc_seconds()/3600, 1)
        self.root.buttonpln(2.0, "2")
        self.assertEqual(self.root.calc_seconds()/3600, 2)
        self.root.buttonpln(5.0, "1")
        self.assertEqual(self.root.calc_seconds()/3600, 3)
        self.root.buttonpln(5.0, "1")
        self.assertEqual(self.root.calc_seconds()/3600, 4)

    def test_three(self):
        self.root.changedate("2021-6-10 19:30:00")
        self.root.buttonpln(5.0, "1")
        self.assertEqual(self.root.calc_departure().date(), self.root.devicetime().date()+ timedelta(days=1))
    
    def test_four(self):
        self.root.changedate("2021-6-11 19:30:00")
        self.root.buttonpln(5.0, "1")
        self.assertEqual(self.root.devicetime().weekday(), 4) # weekday()=4 oznacza piątek
        self.assertEqual(self.root.calc_departure().weekday(), 0) # weekday()=0 oznacza poniedziałek

    def test_five(self):
        self.root.changedate("2021-6-11 10:00:00")#Zmiana daty aby za pół godziny parking działał
        self.root.buttonpln(1.0, "1")
        self.assertEqual(self.root.calc_seconds()/3600, 0.5)

    def test_six(self):
        self.root.changedate("2021-6-11 10:00:00")#Zmiana daty aby za godzinę parking działał
        self.root.buttonpln(0.01, "200")
        self.assertEqual(self.root.calc_seconds()/3600, 1)

    def test_seven(self):
        self.root.changedate("2021-6-11 10:00:00")#Zmiana daty aby za godzinę parking działał
        self.assertRaises(BadInputException, self.root.buttonpln, 0.01, "201")

    def test_eight(self):
        self.assertRaises(BadInputException, self.root.confirm, "KR343VU")

    def test_nine(self):
        self.assertRaises(BadInputException, self.root.confirm, "")
        self.assertRaises(BadInputException, self.root.confirm, "@#$")

if __name__ == '__main__':
    unittest.main()
