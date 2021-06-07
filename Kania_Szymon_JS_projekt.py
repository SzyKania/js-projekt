from decimal import *
from datetime import *
import datetime
from tkinter import *
from functools import partial

class BadNominalException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value) 

class Money():
    
    def __init__(self, val):
        val = Decimal(float(val)).quantize(Decimal('.01'), rounding = ROUND_DOWN)
        allowed = list(map(Decimal, ['0.01', '0.02', '0.05',\
        '0.1', '0.2', '0.5', '1', '2', '5', '10', '20', '50']))
        if val in allowed:
            self._val = val
        else:
            raise BadNominalException(val)
        
    def get_val(self):
        return self._val
    

class ParkingMeter():
    
    def __init__(self):
        self._moneycount = dict.fromkeys(list(map(Decimal, ['0.01', '0.02', '0.05',\
         '0.1', '0.2', '0.5', '1', '2', '5'])), 0)
        self._moneysum = 0
        self._parkingseconds = 0
        self._departure = 0

    def pay_coin(self, coin):
        if not isinstance(coin, Money):
            print("Przesłany obiekt nie jest instancją pieniądza")
            return
        if coin.get_val() not in (10, 20, 50):
            if self._moneycount[coin.get_val()] == 200:
                print("Magazyn monet tego nominalu jest pelny")
                return
            else:
                self._moneycount[coin.get_val()] += 1
        self._moneysum += coin.get_val()
        self._departure = self.calc_departure()
        print("Dodano", coin.get_val(), "kredytu")
    
    def get_bal(self):
        return self._moneysum

    def check_plate(self, plate):
        if(len(plate) > 8 or len(plate) < 4):
            print("Niepoprawny nr rejestracyjny")
            return ""
        elif not all(c.isdigit() or c.isupper() for c in plate):
            print("Niepoprawny nr rejestracyjny")
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
        departure = datetime.datetime.now()

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


       # print('Planowany departure:', departure)
        return departure

    def buttonpln(self, arg):
        self.pay_coin(Money(arg))

    def main(self):
        window = Tk()
        window.geometry('683x384')

        buttondata = [("0.01PLN", 0.01), ("0.02PLN", 0.02), ("0.05PLN", 0.05),\
                     ("0.10PLN", 0.1), ("0.20PLN", 0.2), ("0.50PLN", 0.5),\
                     ("1.00PLN", 1.0), ("2.00PLN", 2.0),  ("5.00PLN", 5.0),\
                     ("10.0PLN", 10.0), ("20.0PLN", 20.0), ("50.0PLN", 50.0)] 
        
        buttons = []
        for text, value in buttondata:
            buttons.append(Button(window, text=text, width=10, command=partial(self.buttonpln, value)))
            
        xdelta = 100
        ydelta = 45
        buttons[0].place(x = 0, y = 0)
        buttons[1].place(x = xdelta, y = 0)
        buttons[2].place(x = 2*xdelta, y = 0)

        buttons[3].place(x = 0, y = ydelta)
        buttons[4].place(x = xdelta, y = ydelta)
        buttons[5].place(x = 2*xdelta, y = ydelta)

        buttons[6].place(x = 0, y = 2*ydelta)
        buttons[7].place(x = xdelta, y = 2*ydelta)
        buttons[8].place(x = 2*xdelta, y = 2*ydelta)
        
        buttons[9].place(x = 0, y = 3*ydelta)
        buttons[10].place(x = xdelta, y = 3*ydelta)
        buttons[11].place(x = 2*xdelta, y = 3*ydelta)

        window.mainloop()


parkomat = ParkingMeter()
parkomat.main()