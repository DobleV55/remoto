from calendar import Calendar
from collections import defaultdict
import random
import pdb

year = 2019
month = 8

current_month_days = [day for day in Calendar().itermonthdates(year, month) if day.weekday() not in [5,6] and day.month == month]

dev =['leo', 'mati', 'diego', 'eric', 'mariano', 'jorge', 'mateo',]

adm = ['yo', 'nadia', 'josh', 'pedro', 'gonza', 'timoteo', 'bauti']


GROUPS = [dev, adm]

#print (current_month_days)

def choose_remoto_days(groups):
    #pdb.set_trace()
    res = {}
    for members in groups:
      valid_days = current_month_days[:14]
      valid_days_2 = current_month_days[15:]
      for member in members:      
            remoto_1 = (random.choice(valid_days))
            valid_days.remove(remoto_1)
            remoto_2 = (random.choice(valid_days_2))
            #pdb.set_trace()           
            valid_days_2.remove(remoto_2) 
            print (valid_days)
            print ("\n")
            print (remoto_1)
            print ("\n")
            print (valid_days_2)
            print ("\n")
            print (remoto_2)
            print ("\n")
            res[member]=[remoto_1, remoto_2]
      print (res)
if __name__ == '__main__':
    choose_remoto_days(GROUPS)
    #choose_remoto_days(groups)
