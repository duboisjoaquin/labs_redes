import requests
from datetime import date
import random

def get_url(year):
    return f"https://nolaborables.com.ar/api/v2/feriados/{year}"

months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
days = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

def day_of_week(day, month, year):
    return days[date(year, month, day).weekday()]

class NextHoliday:
    def __init__(self):
        self.loading = True
        self.year = date.today().year
        self.holiday = None
        self.holiday_by_type = None

    def set_next(self, holidays):
        now = date.today()
        today = {
            'day': now.day,
            'month': now.month
        }
        holiday = next(
            (h for h in holidays if h['mes'] == today['month'] and h['dia'] > today['day'] or h['mes'] > today['month']),
            holidays[0]
        )

        self.loading = False
        self.holiday = holiday

    def fetch_holidays(self):
        response = requests.get(get_url(self.year))
        data = response.json()
        self.set_next(data)

    def set_next_by_type(self, holidays, tp : str):
        now = date.today()
        today = {
            'day': now.day,
            'month': now.month
        }
        holiday = next(
            (h for h in holidays if h['mes'] == today['month'] and h['dia'] > today['day'] and tp == h['tipo'] or h['mes'] > today['month']),
            holidays[0]
        )

        self.loading = False
        self.holiday = holiday

    def fetch_holidays_by_type(self, tp : str):
        response = requests.get(get_url(self.year))
        data = response.json()
        self.set_next_by_type(data, tp)

    def render(self):
        if self.loading:
            print("Buscando...")
        else:
            print("Próximo feriado")
            print(self.holiday['motivo'])
            print("Fecha:")
            print(day_of_week(self.holiday['dia'], self.holiday['mes'] - 1, self.year))
            print(self.holiday['dia'])
            print(months[self.holiday['mes'] - 1])
            print("Tipo:")
            print(self.holiday['tipo'])

if __name__ == '__main__':
    next_holiday = NextHoliday()
    next_holiday.fetch_holidays()
    next_holiday.render()
    print("\n")
    tipos = ['puente', 'inamovible', 'trasladable', 'nolaborable']
    tp = random.choice(tipos)
    next_holiday.fetch_holidays_by_type(tp)
    next_holiday.render()



