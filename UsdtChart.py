from importlib.metadata import files
from matplotlib.backend_bases import Event
import matplotlib.pyplot as plt
import matplotlib.dates as matdates
from datetime import datetime, timedelta
from matplotlib.widgets import Slider
import numpy as numpy


class UsdtChart:
        # Constructor declaration for in-app variables and function call
        def __init__(self):
                self.year = 2024

        def chartdisplay(self):
                #Data Structure for Year, Month, Days and Price traded in each day(datetime library)
                # Opening file that holds the Database(Year, Month, Day and Price) in order
                with open("DataBase/UsdtDB.txt", mode = "r") as file:
                        self.filelist =  file.readlines()
                
                # Formatting all existing dates and prices in UsdtDB.txt to list
                newlist = [tuple(v.split()) for v in self.filelist]
                
                # Empty list for values(y-axis) and dates(x-axis)
                values = []
                dates = []

                # Each index in newlist comprises of the data for x-axis and y-axis which was extracted from file
                # Here comes the loop to extract x-axis(price) and y-axis(date) as they need to be seperated
                for valuedates in newlist:
                        dates.append([])
                        for order in valuedates:
                                length = len(valuedates)
                                lgt = valuedates.index(order)
                                indLen = newlist.index(valuedates)
                                sub = length - 1
                                if lgt <  sub:
                                        # Date Extract WIP
                                        dates[indLen].append(newlist[indLen][lgt])
                                else:
                                        # Value Extract WIP
                                        values.append(int(newlist[indLen][lgt]))
                # print(dates)
                # Values from newlist(file) successfully extracted to values
                # Dates from newlist(file) successfully extracted to dates but still requires a standard formatting.

                # Indepth dates formatting which includes but not limited to typecasting, list migration and get index method.
                list = []
                for val in dates:
                        list.append([])
                        for i in val:
                                conv = int(i)
                                index = dates.index(val)
                                list[index].append(conv)

                                
                dateDB = [tuple(element) for element in list]
                # print(dateDB)
                
                final_list = []
                for element in dateDB:
                        var = element
                        vb = datetime(*var)
                        final_list.append(vb)
                # indepth formatting completed
                # print(final_list)

                date_nums = matdates.date2num(final_list)
                # print(date_nums)

                # Operation to adjust X-axis limit
                xlength = len(final_list)
                mx_length = xlength - 30
                
                # Operation to get the max price so far
                values_max = max(values)
                valindex_max = values.index(values_max)
                datemax = final_list[valindex_max]

                # Operation to get the min price so far
                values_min = min(values)
                valindex_min = values.index(values_min)
                datemin = final_list[valindex_min]
                
                # Indepth Graph formatting methods
                fig, chart = plt.subplots(figsize=(13, 6))
                chart.fill_between(final_list, values, color="skyblue", alpha=0.6, linestyle="-")
                chart.plot(final_list, values, color='Slateblue', alpha=0.4, linewidth=1)
                chart.plot(final_list[-1], values[-1], 'o', markersize=6, markerfacecolor='skyblue', markeredgewidth=2, markeredgecolor='skyblue')
                chart.plot(datemax, values_max, 'o', markersize=6, markerfacecolor='green', markeredgewidth=1, markeredgecolor='green', alpha = 0.5)
                chart.plot(datemin, values_min, 'o', markersize=6, markerfacecolor='red', markeredgewidth=1, markeredgecolor='red', alpha = 0.5)
                # plt.xticks(rotation=20)
                chart.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

                

                current_price = """Blue - Current Price
Green - All Time High
Red - All Time Low"""
                plt.text(1.01, 0.5, current_price, transform=chart.transAxes, fontsize=8, verticalalignment='center', color='grey')
                

                plt.gca().xaxis.set_major_formatter(matdates.DateFormatter('%B %d, %Y'))
                plt.gca().xaxis.set_major_locator(matdates.DayLocator(interval = 4))

                chart.set_xlim(date_nums[0], date_nums[30])
                
                chart.set_title('USDNGN Chart', fontsize=12, fontweight='bold', color='grey')
                chart.set_xlabel('Date', fontsize=8, fontweight='bold', color='grey')
                chart.set_ylabel('Foreign Exchange Rate(Naira)', fontsize=8, fontweight='bold', color='grey')

                ax_slider = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
                slider = Slider(ax_slider, 'Flow path', date_nums[0], date_nums[mx_length] ,valinit=date_nums[0], valstep=1)



                def update(val):
                        pos = slider.val
                        date_val = matdates.num2date(pos)
                        chart.set_xlim(date_val, date_val + timedelta(days=31))
                        # chart.set_xlim(pos, pos + 20)
                        fig.canvas.draw_idle()
                        chart.plot(datemax, values_max, 'o', markersize=6, markerfacecolor='green', markeredgewidth=1, markeredgecolor='green', alpha = 0.5)
                        chart.plot(datemin, values_min, 'o', markersize=6, markerfacecolor='red', markeredgewidth=1, markeredgecolor='red', alpha = 0.5)

                slider.on_changed(update)



                plt.gcf().autofmt_xdate()

                # Show the plot
                plt.show()

        # Function to check if file((UsdtDB.txt) is up to date and can proceed to display chart
        def file_update(format_today, list):

                # Compares the last element on the file if it's updated with today's date
                if format_today == list:
                        print("File is up to date.")
                        return
                else:
                        # Asks the user for options
                        print("Price is not up to date! Would you like to proceed?")
                        print("Input Y to proceed to load chart")
                        print("Input N to update price and load chart")

                        while True:
                                try:
                                        cmd = input("Input a valid command: ").upper()[0]
                                        if cmd == "Y":
                                                print("loading...")
                                                break

                                        elif cmd == "N":
                                                while True:
                                                        try:
                                                                newprice = int(input("What is today's price: "))
                                                                # Format the line to write to the file
                                                                format_today.append(newprice)
                                                                fm = [str(element) for element in format_today]
                                                                line_to_write = ' '.join(fm)
                                                                print(line_to_write)
                                                                print(*fm)
                                                                                
                                                                # Update file with today's price and the inputted price
                                                                with open("DataBase/UsdtDB.txt", mode = "a") as file:
                                                                        file.write("\n" + line_to_write)
                                                                        print("File is updated")
                                                                        return
                                                        except:
                                                                print("Invalid price format!")
                                        else:
                                                print("Wrong input!")
                                except:
                                        print("Wrong input!")