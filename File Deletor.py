from tkinter import Tk, filedialog, Text, Button, Label, ttk, messagebox, IntVar
from tkinter.constants import DISABLED, END, NORMAL, W, E
from os import walk, remove, sep

helpText = r'''
NOTE : For Larger folders it's not recommended to use "Advanced Search"

---------
Folder :
---------
Mention the path where you want to delete the files

Ex : C:\Users\SUJATHA\Desktop\temp2

------------
Extension :
------------
Mention the extension of the files that you want to delete.
Ex : .txt
To delete all types of files, give the input as "All"

----------------
Exclude files :
----------------
You can also mention the files that you don't want to delete(Extension with filename is not needed)

Ex : kiran

--> To exclude multiple files from deletion give the input with comma separated value

Ex : kiran,dileep,sai

--> If you have entered "All" in "Files you want to delete" then don't forget to mention the filename with extension in this field...

Ex : kiran.txt,dileep.jpeg,sai.pdf

------------------
Exclude folders :
------------------
To exclude deletions from directory, mention the directory name

Ex : Folder1

--> To exclude multiple directories from deletion give the input with comma separated value

Ex : Folder1,Folder2,Folder3'''

main_window = Tk()
width = main_window.winfo_screenwidth()
height = main_window.winfo_screenheight()
main_window.title("File Deletor")
main_window.resizable(0, 0)
# main_window.iconbitmap("delete file.ico")

set_op_window_width = 500
set_op_window_height = 350

set_op_window_position_x = (width//2)-(set_op_window_width//2)
set_op_window_position_y = (height//2)-(set_op_window_height//2)

main_window.geometry(
    f"{set_op_window_width}x{set_op_window_height}+{set_op_window_position_x}+{set_op_window_position_y}")


def Browse_func():
    dirDialog = filedialog.askdirectory()
    findExtensions(dirDialog)
    text.config(state=NORMAL)
    text.delete(1.0, END)
    text.insert(END, dirDialog)
    text.config(state=DISABLED)


def findExtensions(path):
    getExtensions = []
    for root, dirs, files in walk(path):
        for i in files:
            temp = i.split('.')
            if len(temp) > 1:
                getExtensions.append(temp[-1])
    getExtensions = ["."+i for i in list(dict.fromkeys(getExtensions))]
    choose_ext_comboBox["values"] = tuple(["All"] + getExtensions)
    choose_ext_comboBox.current(0)


def changeWidget():
    if isSelected.get():
        findExtensions(text.get(1.0, END)[:-1])
        choose_ext_text.grid_forget()
        choose_ext_comboBox.grid(row=3, column=1, sticky=W)
    else:
        choose_ext_comboBox.grid_forget()
        choose_ext_text.grid(row=3, column=1)


def deleteFiles():
    fileWhichAreDeleted = ""
    try:
        path = text.get(1.0, END)[:-1]
        ext = choose_ext_comboBox.get() if isSelected.get(
        ) else choose_ext_text.get(1.0, END)[:-1]
        exc_files = list(map(lambda x: x+ext, exclude_files_text.get(1.0, END)[:-1].split(
            ","))) if ext != "All" else list(exclude_files_text.get(1.0, END)[:-1].split(","))
        exc_dirs = exclude_folder_text.get(1.0, END)[:-1].split(',')
        exc_files = list(map(lambda x: x.strip(), exc_files))
        exc_dirs = list(map(lambda x: x.strip(), exc_dirs))
        for root, dirs, files in walk(path):
            if(True in list(map(lambda x: x in root.split(sep), exc_dirs))):
                pass
            else:
                for file in files:
                    if file.endswith(ext):
                        if file in exc_files:
                            pass
                        else:
                            fileWhichAreDeleted += f"{file}\n"
                            remove(rf"{root}\{file}")
                    elif ext == "All":
                        if file in exc_files:
                            pass
                        else:
                            fileWhichAreDeleted += f"{file}\n"
                            remove(rf"{root}\{file}")
        messagebox.showinfo("Deleted Files", fileWhichAreDeleted) if fileWhichAreDeleted != "" else messagebox.showinfo(
            "Deleted Files", "No files to delete")
        findExtensions(text.get(1.0, END)[:-1])
    except:
        print("Oops! Sorry an error occured...")


def onHelp():
    helpWindow = Tk()
    helpWindow.title("Help")
    # helpWindow.iconbitmap("help.ico")
    content = Label(helpWindow, text=helpText)
    content.grid(row=0, column=0)
    helpWindow.mainloop()


help = Button(main_window, text="Help", command=onHelp)
help.grid(row=0, column=51)

title = Label(main_window, text="File Deletor", font=("Calibri", 14), pady=20)
title.grid(row=1, column=0, columnspan=51)


folder_mention_label = Label(
    main_window, text="Folder",  font=("Cambria", 13))
text = Text(main_window, background="#d1cfcf",
            height=1, width=30, font=("Calibri", 11))
buttonBrowse = Button(main_window, text="Browse",
                      command=Browse_func, cursor="hand2", relief="groove", width=8).grid(row=2, column=3, padx=5)

folder_mention_label.grid(sticky=E, row=2, column=0, padx=10)
text.grid(sticky=W, row=2, column=1)


choose_ext_label = Label(
    main_window, text="Extension", font=("Cambria", 13), pady=10)
choose_ext_comboBox = ttk.Combobox(main_window, state='readonly')
choose_ext_text = Text(main_window, font=("Calibri", 11),
                       height=1, width=30, background="#d1cfcf")
choose_ext_label.grid(sticky=E, row=3, column=0, padx=10)
choose_ext_text.grid(sticky=W, row=3, column=1)

exclude_ext_label = Label(
    main_window, text="Exclude files", font=("Cambria", 13), wraplength=200)
exclude_files_text = Text(main_window, background="#d1cfcf",
                          height=1, width=40, font=("Calibri", 12),)
exclude_ext_label.grid(sticky=E, row=4, column=0, padx=10)
exclude_files_text.grid(sticky=W, row=4, column=1, columnspan=50, pady=10)

exclude_folder_label = Label(
    main_window, text="Exclude folders", font=("Cambria", 13), wraplength=200)
exclude_folder_text = Text(main_window, background="#d1cfcf",
                           height=1, width=40, font=("Calibri", 12),)
exclude_folder_label.grid(sticky=E, row=5, column=0, padx=10)
exclude_folder_text.grid(sticky=W, row=5, column=1, columnspan=50)

submit_btn = Button(main_window, text="DELETE", cursor="hand2", relief="groove",
                    padx=10, pady=2, command=deleteFiles)
submit_btn.grid(row=6, column=0, pady=20, columnspan=300)

isSelected = IntVar()
advanced_search = ttk.Checkbutton(
    main_window, text="Advanced Search", onvalue=1, offvalue=0, variable=isSelected, command=changeWidget)
advanced_search.grid(row=7, column=0, columnspan=300)


main_window.mainloop()
