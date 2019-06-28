from calendar import Calendar
from collections import defaultdict
import pprint
import random

year = 2019
month = 8

current_month_days = [day for day in Calendar().itermonthdates(year, month) if day.weekday() not in [5,6] and day.month == month]

dev =['leo', 'mati', 'diego', 'eric', 'mariano', 'jorge', 'mateo',]

adm = ['yo', 'nadia', 'josh', 'monica', 'mauricio', 'timoteo', 'bauti']

sales = ['Dominica', 'pedro', 'gonza', 'tarta', 'alan', 'julian']

consultoria = ['eze', 'lisandro', 'roberto', 'rodrigo', 'josefina', 'lisa']

GROUPS = [dev, adm, sales, consultoria]

valid_days = current_month_days[:12]
valid_days_2 = current_month_days[13:]

def choose_remoto_days(groups):
    res = {}
    usados = defaultdict(int)
    for members in groups:
      for member in members:      
            remoto_1 = (random.choice(valid_days))
            usados[remoto_1] += 1
            if usados[remoto_1] == 3:
                valid_days.remove(remoto_1)           
            remoto_2 = (random.choice(valid_days_2))
            usados[remoto_2] += 1          
            if usados[remoto_2] == 3:
                valid_days_2.remove(remoto_2) 
            res[member]=[remoto_1, remoto_2]
    pprint.pprint(res)
    pprint.pprint(usados)
        
if __name__ == '__main__':
    choose_remoto_days(GROUPS)
