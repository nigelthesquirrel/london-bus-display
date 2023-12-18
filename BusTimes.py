import os
import tkinter as tk
from tkinter import font
import requests
import datetime

window = tk.Tk()
window['bg'] = "black"
# window.attributes("-fullscreen", True)
frm_mainframe = tk.Frame(background="black")
label_font = font.Font(size=70, family="LED Counter 7")

line_count = 5
lbl_lines = []

stop_id = 'BP2236'  # church road towards Bromley
# stop_id = '37294'   #Bromley South Station North
# stop_id = '40104'   #Bromley South Station South

def refresh():
    response = requests.get(f"https://countdown.api.tfl.gov.uk/interfaces/ura/instant_V1?ReturnList=LineName,"
                            f"DestinationName,EstimatedTime,&StopId={stop_id}")

    if response.status_code == 200:

        text = response.text

        items = text.split(os.linesep)

        stop_only_list = [k for k in items if "[4" not in k]  # strip header

        structured = sorted([string_to_tuple(s) for s in stop_only_list], key=lambda i: i[2])
        structured = structured[:line_count]

        for lbl_line in lbl_lines:
            lbl_index, lbl_bus_no, lbl_bus_name, lbl_when = lbl_line
            lbl_index['text'] = ""
            lbl_bus_no['text'] = ""
            lbl_bus_name['text'] = ""
            lbl_when['text'] = ""

        line_no = 0
        for lbl_line in lbl_lines:
            lbl_index, lbl_bus_no, lbl_bus_name, lbl_when = lbl_line

            if line_no >= len(structured):
                break

            item_text, bus_no_text, where_text, when_text = tuple_to_description(structured[line_no], line_no)

            lbl_index['text'] = item_text
            lbl_bus_no['text'] = bus_no_text
            lbl_bus_name['text'] = where_text
            lbl_when['text'] = when_text

            line_no = line_no + 1


    else:
        for lbl_line in lbl_lines:
            lbl_line['text'] = "Error"

    window.after(5000, lambda: refresh())


def tuple_to_description(bus_tuple, item_no):
    bus_number, where, when_mins = bus_tuple

    if when_mins <= 0:
        when = '  due'
    else:
        when = "{0:>2}min".format(when_mins)

    bus_number = bus_number.ljust(4, ' ')
    when = when.ljust(5, ' ')

    return item_no + 1, bus_number, where, when


def string_to_tuple(stop_string):
    stop_string = stop_string[1:-1]

    (bus_number, where, when) = stop_string.split('",')
    bus_number = bus_number[3:]
    where = where[1:]

    when = int(when)

    now = datetime.datetime.now(datetime.UTC)
    bus_ts = datetime.datetime.fromtimestamp(when / 1000, datetime.UTC)

    duration = bus_ts - now
    duration_in_s = duration.total_seconds()

    return bus_number, where, int(divmod(duration_in_s, 60)[0])


def do_stuff():
    frm_mainframe.pack()

    for i in range(0, line_count):
        lbl_item = tk.Label(master=frm_mainframe, text="1", bg="black", fg="orange",
                            font=label_font, justify="left", anchor="w", width=2)
        lbl_item.grid(row=i + 1, column=1)

        lbl_bus_number = tk.Label(master=frm_mainframe, text="", bg="black", fg="orange",
                                  font=label_font, justify="left", anchor="w", width=4)
        lbl_bus_number.grid(row=i + 1, column=2)

        lbl_bus_name = tk.Label(master=frm_mainframe, text="", bg="black", fg="orange",
                                font=label_font, justify="left", anchor="w", width=20)
        lbl_bus_name.grid(row=i + 1, column=3)

        lbl_bus_when = tk.Label(master=frm_mainframe, text="", bg="black", fg="orange",
                                font=label_font, justify="left", anchor="w", width=5)

        lbl_bus_when.grid(row=i + 1, column=4)

        lbl_lines.append((lbl_item, lbl_bus_number, lbl_bus_name, lbl_bus_when))

    refresh()
    window.mainloop()


if __name__ == '__main__':
    def main():
        do_stuff()

main()