# This is the Main file. The main logic & UI in a single file written here.

# Import important requirements.
from tkinter import *
import pandas
from tkinter import messagebox

# Load existing data into Data Frame 
mydf = pandas.read_csv("words_bank.csv")
words_list = [[row.word, row.meaning] for (index, row) in mydf.iterrows()]
word_no = 0
clicked = 1


def hide_home_buttons():
    exsz_button.place_forget()
    add_adit_button.place_forget()

def home_page():
    global clicked, word_no
    next_meaning_button.place_forget()
    word_lable.place_forget()
    meaning_lable.place_forget()
    word_entry.place_forget()
    meaning_entry.place_forget()
    save_button.place_forget()
    search_button.place_forget()
    delete_button.place_forget()
    canvas2.place_forget()
    exsz_button.place(x=680, y=600)
    add_adit_button.place(x=680, y=635)
    next_meaning_button.config(text=" START ")
    word_entry.delete(0, END)
    word_entry.insert(index=1, string="type word")
    meaning_entry.delete("1.0", "end")
    meaning_entry.insert(INSERT, "type meaning")
    clicked = 1
    word_no = 0

def exsz_page():
    hide_home_buttons()
    next_meaning_button.place(x=1050, y=420)

def show_meaning():
    global clicked, word_no
    clicked += 1
    if word_no < len(words_list):
        if clicked % 2 == 0:
            word_lable.config(text=f'"{words_list[word_no][0].title()}"')
            word_lable.place(x=430, y=200)
            next_meaning_button.config(text="Meaning")
            meaning_lable.place_forget()
            canvas2.place(x=975, y=67)
        else:
            canvas2.place_forget()
            meaning_lable.config(text=words_list[word_no][1])
            meaning_lable.place(x=550, y=270)
            next_meaning_button.config(text=" Next >> ")
            word_no += 1
    else:
        messagebox.showinfo(message="Dictionary Exhausted. You have Tried All Words.")
        home_page()

def save_word():
    if len(word_entry.get().strip()) <=0 or len(meaning_entry.get("1.0", "end-1c")) <=1:
        messagebox.showerror(title="Error", message="Blank/Short Entry Not Allowed!!")
    else:
        word_exist = False
        for (index, row) in mydf.iterrows():
            if row.word == word_entry.get().lower():
                if messagebox.askokcancel(title="Confirmation", message="Do You Want to Save CHANGES?"):
                    row.meaning = meaning_entry.get("1.0", "end-1c")
                    messagebox.showinfo(message="Changes Saved Successfully. !!Change Reflects post Restart!!")
                word_exist = True
        if word_exist is False:
            if messagebox.askokcancel(title="Confirmation", message="Do You Want to Add NEW WORD into Dictionary?"):
                mydf.loc[len(mydf.index)] = [word_entry.get().lower().strip(), meaning_entry.get("1.0", "end-1c")]
                messagebox.showinfo(message="New Word Added Successfully. !!Change Reflects post Restart!!")
        mydf.to_csv("words_bank.csv", index=False)
        word_entry.delete(0, END)
        meaning_entry.delete("1.0", "end")

def add_adit_page():
    hide_home_buttons()
    word_entry.place(x=470, y=230)
    meaning_entry.place(x=470, y=260)
    save_button.place(x=470, y=310)
    search_button.place(x=753, y=225)
    delete_button.place(x=753, y=310)

def search_word():
    word_found = False
    for item in words_list:
        if item[0] == word_entry.get().lower():
            meaning_entry.delete("1.0", "end")
            meaning_entry.insert(INSERT, item[1])
            word_found = True
    if not word_found:
            messagebox.showinfo(message="This Word is not Found.")
            meaning_entry.delete("1.0", "end")

def delete_word():
    if messagebox.askokcancel(title="Caution",message="Will be DELETED Permanently."):
        mydf.drop(mydf.index[(mydf["word"] == word_entry.get())], axis=0, inplace=True)
        mydf.to_csv("words_bank.csv", index=False)
        messagebox.showinfo(message="Deleted Successfully.")
    word_entry.delete(0, END)
    meaning_entry.delete("1.0", "end")

window = Tk()
window.title("Skill Up")
window.config(bg="#A7D2CB", height=750, width=1350, padx=20)

canvas = Canvas(width=290, height=337, bg="yellow", highlightthickness=0)
logo_image = PhotoImage(file="img2.png")
canvas.create_image(150, 167, image=logo_image)
canvas.place(x=30, y=170)

canvas2 = Canvas(width=290, height=337, bg="#A7D2CB", highlightthickness=0)
logo_image2 = PhotoImage(file="img4.png")
canvas2.create_image(150, 167, image=logo_image2)

welcome_lable = Label(text="MR's  Vocab  Builder", font=("Broadway", 20), bg="#A7D2CB", fg="#15133C")
welcome_lable.place(x=500, y=20)

word_lable = Label(font=("arial black", 22), bg="#A7D2CB", fg="#810034")
meaning_lable = Label(font=("Berlin Sans FB", 20), bg="#A7D2CB", fg="#172774", wraplength=600, justify="left")

home_button = Button(text="Home", width=10, bg="#FFC5E6", command=home_page)
home_button.place(x=10, y=30)
exsz_button = Button(text=" Excercise ", width=23,fg="#B6FFEA",font=("arial black", 10),bg="#3D6CB9", command=exsz_page)
exsz_button.place(x=680, y=600)
add_adit_button = Button(text="Add / Edit", width=23,fg="#B6FFEA",font=("arial black", 10),bg="#3D6CB9", command=add_adit_page)
add_adit_button.place(x=680, y=635)
next_meaning_button = Button(text=" START ", width=17, fg="#B6FFEA",font=("arial black", 10),bg="#414141", command=show_meaning)

word_entry = Entry(width=30, bg="#E3DFFD")
word_entry.insert(index=1, string="type word")
word_entry.focus()
meaning_entry = Text(height=2, width=45, bg="#E3DFFD")
meaning_entry.insert(INSERT, "type meaning")

save_button = Button(text="Save", width=10, command=save_word, bg="#414141", fg="#B6FFEA")
search_button = Button(text="Search", width=10, command=search_word, bg="#414141", fg="#B6FFEA")
delete_button = Button(text="Delete", width=10, command=delete_word, bg="#414141", fg="red")

# Keep window open untill it is closed.
window.mainloop()
