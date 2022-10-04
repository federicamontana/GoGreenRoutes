import pandas as pd
import os 

path_data = 'dataframe/df_complete.csv'
my_path_data = os.path.abspath(path_data)

class Twitter_Sentiment:
    def __init__(self):
        self.output_data_folder = my_path_data





# class Employee:
#     raise_amount = 1.04 
#     def __init__(self, first, last, pay):
#         self.first = first 
#         self.last = last
#         self.pay = pay
#         self.email = first + '.' + last + '@company.com'
    
#     def fullname(self):
#         return '{} {}'.format(self.first,self.last)

#     def apply_raise(self):
#         self.pay = int(self.pay * self.raise_amount)



# emp_1 = Employee('Corey', 'Schafer', 50000)
# #emp1.__dict__
# emp_1.fullname()
