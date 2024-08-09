from UsdtChart import *
from datetime import datetime

# Object definition from UsdtChart library
UsdtObj = UsdtChart()

# Data structure from saved date data
with open("DataBase/UsdtDB.txt", mode = "r") as file:
        #Read the last line from file
        UsdtObj.filelist =  file.readlines()
        last_line = UsdtObj.filelist[-1]

# Format last line from file to list and in the format[2024, 7, 3, "price"]
list = last_line.split()
# Price is popped out

list = list[:-1]

# Get today's date
today = datetime.now()

# Enlist format from 2024-07-06 to list
enlist_today = today.strftime("%Y %m %d").split()

# Change format from 2024-07-06  to 2024 7 6
format_today = []
for st in enlist_today:
        if st.startswith("0"):
                st = st.lstrip("0")
                
                format_today.append(st)
                
        else:
                format_today.append(st)
print(format_today)

# All function calls integration before the main function call
UsdtChart.file_update(format_today, list)

# Main App Display function call
UsdtObj.chartdisplay()