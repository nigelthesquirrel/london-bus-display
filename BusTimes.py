import tkinter as tk
from tkinter import font
import requests
import datetime

window = tk.Tk()
window['bg'] = "black"
window.attributes("-fullscreen", True)
frm_mainframe = tk.Frame(background="black")

line_count = 5
lbl_lines = []
stop_id = ''
config = {}


def refresh():
    response = requests.get(f"https://countdown.api.tfl.gov.uk/interfaces/ura/instant_V1?ReturnList=LineName,"
                            f"DestinationName,EstimatedTime,&StopId={stop_id}")

    if response.status_code == 200:

        stop_only_list = [k for k in response.text.split("\r\n") if "[4" not in k]  # strip header which has [4
        structured = sorted([string_to_tuple(s) for s in stop_only_list], key=lambda i: i[2])[:line_count]

        for lbl_line in lbl_lines:
            lbl_index, lbl_bus_no, lbl_bus_name, lbl_when = lbl_line

            for lbl in (lbl_index, lbl_bus_no, lbl_bus_name, lbl_when):
                lbl['text'] = ""

        line_no = 0
        for lbl_line in lbl_lines:
            lbl_index, lbl_bus_no, lbl_bus_name, lbl_when = lbl_line

            if line_no >= len(structured):
                break

            lbl_index['text'], lbl_bus_no['text'], lbl_bus_name['text'], lbl_when['text'] = tuple_to_description(
                structured[line_no], line_no)

            line_no = line_no + 1

    else:
        for lbl_line in lbl_lines:
            lbl_line['text'] = "Error"

    window.after(10000, lambda: refresh())


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
    now = datetime.datetime.utcnow()
    bus_ts = datetime.datetime.fromtimestamp(when / 1000, datetime.UTC)
    duration = bus_ts - now
    duration_in_s = duration.total_seconds()

    return bus_number, where, int(divmod(duration_in_s, 60)[0])


def setup():
    global config
    with open("config") as f:
        read_lines = f.readlines()
        l = [line.split("#")[0].rstrip().split("=") for line in read_lines if
             not line.startswith("#") and not line.isspace()]
        config = {key.strip(): value.strip() for key, value in l}

    frm_mainframe.pack()

    global line_count
    line_count = int(config['line_count'])
    global stop_id
    stop_id = config['stop_id']

    label_font = font.Font(size=int(config['font_size']), family=f"{config['font']}")

    for i in range(0, line_count):
        lbl_item = tk.Label(master=frm_mainframe, text="", bg="black", fg="orange",
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


def create_label(width, row, column):
    label_font = font.Font(size=int(config['font_size']), family=f"{config['font']}")
    lbl = tk.Label(master=frm_mainframe, text="", bg="black", fg="orange",
                   font=label_font, justify="left", anchor="w", width=width)
    lbl.grid(row=row, column=column)
    return lbl


if __name__ == '__main__':
    def main():
        setup()

main()
