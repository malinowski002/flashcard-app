from tkinter import Tk
from flashcard_app import FlashcardApp

if __name__ == "__main__":
    window = Tk()
    window.title("Flashcard App")
    app = FlashcardApp(window)
    window.mainloop()
