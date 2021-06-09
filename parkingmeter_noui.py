from decimal import *
from datetime import *
import datetime
import time
from dateutil.parser import parse
from money import *

class BadInputException(Exception):
    pass

class ParkingMeterNoUI():
    def __init__(self):
        self._moneycount = dict.fromkeys(list(map(Decimal, ['0.01', '0.02', '0.05',\
         '0.1', '0.2', '0.5', '1', '2', '5'])), 0)
        self._moneysum = 0
        self._parkingseconds = 0
        self._departure = 0
        self._timechange = timedelta(seconds=0)

    def pay_coin(self, coin):
        if coin.get_val() not in (10, 20, 50):
            try:
                if self._moneycount[coin.get_val()] == 200:
                    raise BadInputException
            except BadInputException:
                print("Bład\nMagazyn monet tego nominalu jest pelny")
                raise BadInputException
            else:
                self._moneycount[coin.get_val()] += 1
        self._moneysum += coin.get_val()
        self._departure = self.calc_departure()
        #print("Dodano", coin.get_val(), "kredytu")
    
    def get_bal(self):
        return self._moneysum

    def check_plate(self, plate):
        try:
            if(len(plate) > 8 or len(plate) < 4):
                raise BadInputException
            elif not all(c.isdigit() or c.isupper() for c in plate):
                raise BadInputException
        except BadInputException:
            print("Bład\nNiepoprawny nr rejestracyjny")
            return ""
        else:
            return plate

    def calc_seconds(self):
        temp = self.get_bal()
        if temp <= 2.0:
            _parkingseconds = temp * 30 * 60
        elif temp <= 6.0:
            temp -= 2
            _parkingseconds = (60 + temp * 15) * 60
        else:
            temp -= 6
            _parkingseconds = (120 + temp * 12) * 60
        return int(_parkingseconds)

    def calc_sec_to_20(self, departure: datetime.datetime):
        datetime_end = departure.replace(hour=20, minute=0, second=0, microsecond=0)
        return (datetime_end - departure).total_seconds()

    def calc_departure(self):

        seconds = self.calc_seconds()
        departure = datetime.datetime.now()+self._timechange

        while seconds != 0:
    
            if departure.weekday() == 6:
                departure += datetime.timedelta(days=1)
                departure = departure.replace(hour=8, minute=0, second=0, microsecond=0)
            elif departure.weekday() == 5:
                departure += datetime.timedelta(days=2)
                departure = departure.replace(hour=8, minute=0, second=0, microsecond=0)

            if departure.hour >= 20:
                departure += datetime.timedelta(days=1)
                departure = departure.replace(hour=8, minute=0, second=0, microsecond=0)
                continue
            elif departure.hour < 8:
                departure = departure.replace(hour=8, minute=0, second=0, microsecond=0)
            
            sec_to_20 = self.calc_sec_to_20(departure)
            if seconds < sec_to_20:
                departure += datetime.timedelta(seconds=seconds)
                seconds = 0
            else:
                departure += datetime.timedelta(seconds=sec_to_20)
                seconds -= sec_to_20
        return departure

    def buttonpln(self, arg, field):

        multiplier = field
        if not(multiplier.isdigit()):
            multiplier = 1

        multiplier = int(multiplier)

        if multiplier < 1:
            multiplier = 1

        for _ in range(multiplier):
            self.pay_coin(Money(arg))

    def popup_window(self, plate, sold, departure):

        plate = "Nr rejestracyjny: " + plate
        sold = "\nCzas zakupu: " + sold.strftime("%m/%d/%Y, %H:%M")
        departure = "\nKoniec biletu: " + departure.strftime("%m/%d/%Y, %H:%M")

        message = plate + sold + departure
        print(message)

    def confirm(self, plate):
        try:
            if self.check_plate(plate) == "":
                raise BadInputException
            if self._moneysum == 0:
                raise BadInputException
        except BadInputException:
            print("Błąd - Nie wrzucono monet")
            raise BadInputException
        else:
            self.popup_window(plate, datetime.datetime.now()+self._timechange, self.calc_departure())
            self._moneysum = 0

    def changedate(self, newdate):
        try:
            mydate = parse(newdate)
        except ValueError:
            print("Błąd - Niepoprawny format daty - YYYY-MM-DD hh:mm")
            raise ValueError
        else:
            self._timechange = mydate - datetime.datetime.now()

    def devicetime(self):
        return self._timechange + datetime.datetime.now()