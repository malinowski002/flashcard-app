import json
from tkinter import Canvas, Label, Button, PhotoImage, simpledialog, Entry
import random
from word_manager import WordManager

BACKGROUND_COLOR = "#9FE6FF"
global current_language
current_language = "spanish"

class FlashcardApp:
    global BACKGROUND_COLOR
    def __init__(self, window):
        self.window = window
        self.window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
        self.word_manager = WordManager("spanish_words.json")
        self.BACKGROUND_COLOR = BACKGROUND_COLOR

        self.current_language = "spanish"

        self.repeats_label = Label(text="", bg=self.BACKGROUND_COLOR, font="Helvetica 20")
        self.repeats_label.config(foreground="#000470")
        self.repeats_label.grid(row=2, column=1, columnspan=2)

        self.canvas = Canvas(height=340, width=810)
        self.front_card_img = PhotoImage(file="img/card_front.png")
        self.back_card_img = PhotoImage(file="img/card_back.png")
        self.card_bg = self.canvas.create_image(430, 170, image=self.front_card_img)
        self.card_title = self.canvas.create_text(408, 110, text="Spanish", fill="#000470", font="Helvetica 35 italic")
        self.card_word = self.canvas.create_text(
            420, 170, text="", fill="#000470",
            font="Helvetica 65 bold")
        self.show_random_word()

        self.canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=4)

        self.wrong_img = PhotoImage(file="img/wrong.png")
        self.wrong_button = Button(image=self.wrong_img, highlightthickness=0, bd=0, command=self.wrong_clicked)
        self.wrong_button.grid(row=1, column=0, pady=10)

        self.right_img = PhotoImage(file="img/right.png")
        self.right_button = Button(image=self.right_img, highlightthickness=0, bd=0, command=self.right_clicked)
        self.right_button.grid(row=1, column=1, pady=10)

        self.show_img = PhotoImage(file="img/show.png")
        self.show_button = Button(image=self.show_img, highlightthickness=0, bd=0, command=self.show_other_side)
        self.show_button.grid(row=1, column=2, pady=10)

        self.add_img = PhotoImage(file="img/add.png")
        self.add_button = Button(image=self.add_img, highlightthickness=0, bd=0, command=self.add_button_clicked)
        self.add_button.grid(row=1, column=3, pady=10)

    def show_random_word(self):
        random_word, repeats_number = self.word_manager.get_next_word()
        self.canvas.itemconfig(self.card_title, text="Spanish")
        self.canvas.itemconfig(self.card_bg, image=self.front_card_img)
        self.canvas.itemconfig(self.card_word, text=random_word)
        self.repeats_label.config(text=f"upcoming repeats of that word: {repeats_number}")

    def wrong_clicked(self):
        if self.current_language != "spanish":
            self.show_other_side()

        current_word = self.canvas.itemcget(self.card_word, "text")
        self.word_manager.update_word_count(current_word, "+")

        self.show_random_word()

    def right_clicked(self):
        if self.current_language != "spanish":
            self.show_other_side()

        current_word = self.canvas.itemcget(self.card_word, "text")
        self.word_manager.update_word_count(current_word, "-")

        self.show_random_word()

    def show_other_side(self):
        if self.current_language == "spanish":
            self.canvas.itemconfig(self.card_bg, image=self.back_card_img)
            self.canvas.itemconfig(self.card_title, text="English")

            current_word = self.canvas.itemcget(self.card_word, "text")

            self.canvas.itemconfig(self.card_word, text=self.word_manager.get_english_translation(current_word))
            self.current_language = "english"
        else:
            self.canvas.itemconfig(self.card_bg, image=self.front_card_img)
            self.canvas.itemconfig(self.card_title, text="Spanish")

            current_word = self.canvas.itemcget(self.card_word, "text")

            self.canvas.itemconfig(self.card_word, text=self.word_manager.get_spanish_translation(current_word))
            self.current_language = "spanish"

    def add_button_clicked(self):
        dialog = simpledialog.Toplevel(self.window)
        dialog.title("Add New Word")

        Label(dialog, text="Spanish Word:").grid(row=0, column=0)
        spanish_word_entry = Entry(dialog)
        spanish_word_entry.grid(row=0, column=1)

        Label(dialog, text="English Translation:").grid(row=1, column=0)
        english_translation_entry = Entry(dialog)
        english_translation_entry.grid(row=1, column=1)

        Label(dialog, text="Count:").grid(row=2, column=0)
        repeats_entry = Entry(dialog)
        repeats_entry.grid(row=2, column=1)

        def add_word():
            spanish_word = spanish_word_entry.get()
            english_word = english_translation_entry.get()
            repeat_count = int(repeats_entry.get())
            self.word_manager.add_word(spanish_word, english_word, repeat_count)
            dialog.destroy()
            self.show_random_word()

        Button(dialog, text="Cancel", command=dialog.destroy).grid(row=3, column=0, pady=10)
        Button(dialog, text="OK", command=add_word).grid(row=3, column=1, pady=10)