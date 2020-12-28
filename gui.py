#!/usr/bin/python
# -*- coding: utf-8 -*-
# Module: GUI.py
import tkinter
from tkinter import *
from tkinter import filedialog, messagebox, font

import pandas as pd

# our modules
from main import remove_hard_to_phrase_words, send_data_to_YAP

SCREEN_PROPORTIONS = 0.5  # half of the screen proportions
PROGRAM_NAME = "טען טקסט"
AMOUNT_OF_ELEMENTS_ROWS = 3
AMOUNT_OF_ELEMENTS_COLS = 1
TITLE = "NLPH"


class Gui:

    def __init__(self, data, root=None):
        self.root = root
        self.data = data
        self.init_elements()
        self.text_to_process=''
        self.text_to_phrase

    def init_elements(self):
        self.root.title(TITLE)
        root.geometry('500x500')
        self.pad_y = int(self.screen_ration_height() * 2 / AMOUNT_OF_ELEMENTS_ROWS)
        self.pad_x = int(self.screen_ration_width() / AMOUNT_OF_ELEMENTS_COLS)
        self.set_buttons()
        self.set_entries()

    def set_buttons(self):
        row, col = self.pad_y, self.pad_x
        Button(self.root, text=PROGRAM_NAME, command=self.load_text, width=25, anchor='w').place(
            x=self.screen_ration_width() / 4, y=row * 0.5)

    def set_scale_val(self, val):
        selection = str(val)
        self.threshold_amount.config(text=selection)
        data['threshold'] = val

    def set_entries(self):
        row, col, col_factor = self.pad_y, self.pad_x, 1.5
        self.text_to_phrase = Entry(self.root, justify='center',width=60)
        self.text_to_phrase.place(x=0 * col_factor, y=0)

    def load_text(self):
        row, col = self.pad_y, self.pad_x
        text = self.text_to_phrase.get()
        text = remove_hard_to_phrase_words(text)
        self.text_to_process = text
        parsed = send_data_to_YAP(self.text_to_process)
        response = Text(self.root, font = ('Tahoma', 14), width=70)
        response.tag_configure('tag-right', justify='right')
        response.place(x=0, y=row * 1)
        for key, val in parsed.items():
            if key == 'tokenized_text' or key == 'segmented_text' or key == 'lemmas':
                response.insert(INSERT, '{0}:\n{1}\n\n'.format(key, val),'tag-right')

    def screen_ration_height(self):
        return int(int((self.root.winfo_screenheight() / 2) - (self.root.winfo_reqheight() / 2)) * SCREEN_PROPORTIONS)

    def screen_ration_width(self):
        return int(int((self.root.winfo_screenwidth() / 2) - (self.root.winfo_reqwidth() / 2)) * SCREEN_PROPORTIONS)


root = Tk()
data = {}
my_gui = Gui(data, root)
root.mainloop()
