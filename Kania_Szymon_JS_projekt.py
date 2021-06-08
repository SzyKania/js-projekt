from decimal import *
from datetime import *
import datetime
import time
from tkinter import *
from tkinter.messagebox import showinfo
from functools import partial
from dateutil.parser import parse

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
        self._timechange = timedelta(seconds=0)

        xdelta = 100
        ydelta = 45
        offs = 10

        window = Tk()
        window.geometry('455x300')

        multiplier = Entry(window, width=14)
        multiplier.place(x = xdelta+offs, y = 4*ydelta+offs)
        multiplier.insert(0, "Mnoznik monet")

        sumviewer = Label(window, text=self._moneysum)
        sumviewer.place(x=xdelta+offs, y = ydelta*5 + offs)

        departureviewer = Label(window, text="")
        #departureviewer.place(x=offs, )

        buttondata = [("0.01PLN", 0.01), ("0.02PLN", 0.02), ("0.05PLN", 0.05),\
                     ("0.10PLN", 0.1), ("0.20PLN", 0.2), ("0.50PLN", 0.5),\
                     ("1.00PLN", 1.0), ("2.00PLN", 2.0),  ("5.00PLN", 5.0),\
                     ("10.0PLN", 10.0), ("20.0PLN", 20.0), ("50.0PLN", 50.0)] 
        
        buttons = []
        for text, value in buttondata:
            buttons.append(Button(window, text=text, width=10, command=partial(self.buttonpln, value, multiplier, sumviewer)))
            
        buttons[0].place(x = offs, y = offs)
        buttons[1].place(x = xdelta+offs, y = offs)
        buttons[2].place(x = 2*xdelta+offs, y = offs)

        buttons[3].place(x = offs, y = ydelta+offs)
        buttons[4].place(x = xdelta+offs, y = ydelta+offs)
        buttons[5].place(x = 2*xdelta+offs, y = ydelta+offs)

        buttons[6].place(x = offs, y = 2*ydelta+offs)
        buttons[7].place(x = xdelta+offs, y = 2*ydelta+offs)
        buttons[8].place(x = 2*xdelta+offs, y = 2*ydelta+offs)
        
        buttons[9].place(x = offs, y = 3*ydelta+offs)
        buttons[10].place(x = xdelta+offs, y = 3*ydelta+offs)
        buttons[11].place(x = 2*xdelta+offs, y = 3*ydelta+offs)

        plate = Entry(window, width=14)
        plate.place(x = 2*xdelta+offs, y = 4*ydelta+offs)
        plate.insert(0, "Wpisz nr rejestr")

        confirmation = Button(window, text="Zatwierdz bilet", command=partial(self.confirm, plate))
        confirmation.place(x = 2*xdelta+offs, y = 5*ydelta+offs)            

        dateclock = Label(window, text=f"{datetime.datetime.now():%Y-%m-%d %H:%M}")
        dateclock.place(x=3*xdelta+offs, y = offs)

        newdate = Entry(window, width=22)
        newdate.place(x = 3*xdelta+offs, y = ydelta+offs)
        newdate.insert(0, "YYYY-MM-DD hh:mm")

        confirmation = Button(window, text="Zmien date i godzine", command=partial(self.changedate, newdate))
        confirmation.place(x = 3*xdelta+offs, y = 2*ydelta+offs)        

        def display_time():
            current_time = (datetime.datetime.now()+self._timechange).strftime("%Y-%m-%d %H:%M")
            dateclock['text'] = current_time
            dateclock.after(1000, display_time)

        display_time()
        window.mainloop()

    def pay_coin(self, coin, sumviewer):
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
        sumviewer['text'] = self._moneysum
        print("Dodano", coin.get_val(), "kredytu")
    
    def get_bal(self):
        return self._moneysum

    def check_plate(self, plate):
        if(len(plate) > 8 or len(plate) < 4):
            showinfo("Bład", "Niepoprawny nr rejestracyjny")
            return ""
        elif not all(c.isdigit() or c.isupper() for c in plate):
            showinfo("Bład", "Niepoprawny nr rejestracyjny")
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
       # print('Planowany departure:', departure)
        return departure

    def buttonpln(self, arg, field, sumviewer):

        multiplier = field.get()
        if not(multiplier.isdigit()):
            multiplier = 1

        multiplier = int(multiplier)

        if multiplier < 1:
            multiplier = 1

        for _ in range(multiplier):
            self.pay_coin(Money(arg), sumviewer)

    def popup_window(self, plate, sold, departure):
        window = Toplevel()
        plate = "Nr rejestracyjny: " + plate
        sold = "\nCzas zakupu: " + sold.strftime("%m/%d/%Y, %H:%M")
        departure = "\nKoniec biletu: " + departure.strftime("%m/%d/%Y, %H:%M")

        message = plate + sold + departure
        label = Label(window, text=message)
        label.pack(fill='x', padx=50, pady=5)

        button_close = Button(window, text="Zamknij", command=window.destroy)
        button_close.pack(fill='x')

    def confirm(self, plate):
        string = plate.get()
        if self.check_plate(string) == "":
            return
        elif self._moneysum == 0:
            showinfo("Bład", "Nie wrzucono monet")
            return
        else:
            self.popup_window(string, datetime.datetime.now()+self._timechange, self.calc_departure())
            self._moneysum = 0

    def changedate(self, newdate):
        mydate = newdate.get()
        try:
            mydate = parse(mydate)
        except ValueError:
            showinfo("Bład", "Niepoprawny format daty\nYYYY-MM-DD hh:mm")
            return
        self._timechange = mydate - datetime.datetime.now()


parkomat = ParkingMeter()
