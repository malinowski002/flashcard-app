import json
from tkinter import *
from tkinter import simpledialog
import random

BACKGROUND_COLOR = "#9FE6FF"
global current_language
current_language = "spanish"

# ------------------------ USER ACTIONS HANDLING ------------------------ #

def wrong_clicked():
    if current_language != "spanish":
        show_other_side()
    # Changing current word count
    current_word = canvas.itemcget(card_word, "text")
    data[current_word][1] += 1
    with open("spanish_words.json", "w") as file:
        json.dump(data, file, indent=1)

    # Generating new word
    next_word = random.choice(list(data))
    canvas.itemconfig(card_word, text=next_word)
    repeats_number = data[next_word][1]
    repeats_label.config(text=f"upcoming repeats of that word: {repeats_number}")


def right_clicked():
    if current_language != "spanish":
        show_other_side()
    # Changing current word count
    current_word = canvas.itemcget(card_word, "text")
    data[current_word][1] -= 1
    with open("spanish_words.json", "w") as file:
        json.dump(data, file, indent=1)

    # Generating new word
    next_word = random.choice(list(data))
    canvas.itemconfig(card_word, text=next_word)
    repeats_number = data[next_word][1]
    repeats_label.config(text=f"upcoming repeats of that word: {repeats_number}")


def show_other_side():
    global current_language
    if current_language == "spanish":
        # Changing canvas image
        canvas.itemconfig(card_bg, image=back_card_img)
        # Changing text
        canvas.itemconfig(card_title, text="English")
        current_word = canvas.itemcget(card_word, "text")
        canvas.itemconfig(card_word, text=data[current_word][0])
        # Change language flag
        current_language = "english"
    else:
        # Changing canvas image
        canvas.itemconfig(card_bg, image=front_card_img)
        # Changing text
        canvas.itemconfig(card_title, text="Spanish")
        current_word = canvas.itemcget(card_word, "text")
        keys = [key for key, value in data.items() if value[0] == current_word]
        canvas.itemconfig(card_word, text=keys[0])
        # Change language flag
        current_language = "spanish"


def add_button_clicked():
    dialog = simpledialog.Toplevel(window)
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
        new_word = {spanish_word: [english_word, repeat_count]}
        data.update(new_word)
        with open("spanish_words.json", "w") as file:
            json.dump(data, file, indent=1)
        print(data)

    Button(dialog, text="Cancel", command=dialog.destroy).grid(row=3, column=0, pady=10)
    Button(dialog, text="OK", command=add_word).grid(row=3, column=1, pady=10)

# ------------------------ SETUP ------------------------ #

window = Tk()
window.title("Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

with open("spanish_words.json", "r") as data_file:
    data = json.load(data_file)
    random_word = random.choice(list(data))

# canvas = Canvas(height=526, width=800)
canvas = Canvas(height=340, width=810)
front_card_img = PhotoImage(file="img/card_front.png")
back_card_img = PhotoImage(file="img/card_back.png")
card_bg = canvas.create_image(430, 170, image=front_card_img)
card_title = canvas.create_text(408, 110, text="Spanish", fill="#000470", font="Helvetica 35 italic")
card_word = canvas.create_text(408, 180, text=random_word, fill="#000470", font="Helvetica 65 bold")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=4)

wrong_img = PhotoImage(file="img/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, bd=0, command=lambda: wrong_clicked())
wrong_button.grid(row=1, column=0, pady=10)

right_img = PhotoImage(file="img/right.png")
right_button = Button(image=right_img, highlightthickness=0, bd=0, command=lambda: right_clicked())
right_button.grid(row=1, column=1, pady=10)

show_img = PhotoImage(file="img/show.png")
show_button = Button(image=show_img, highlightthickness=0, bd=0, command=lambda: show_other_side())
show_button.grid(row=1, column=2, pady=10)

add_img = PhotoImage(file="img/add.png")
add_button = Button(image=add_img, highlightthickness=0, bd=0, command=lambda: add_button_clicked())
add_button.grid(row=1, column=3, pady=10)

repeats = data[random_word][1]
repeats_label = Label(text=f"upcoming repeats of that word: {repeats}", bg=BACKGROUND_COLOR, font="Helvetica 20")
repeats_label.config(foreground="#000470")
repeats_label.grid(row=2, column=1, columnspan=2)

window.mainloop()