from tkinter import *

root = Tk()

# Outer container
testarea = Frame(root, width=300, height=300)
testarea.grid(row=0, column=1)

text_label = Label(testarea, text="test")


# Inner frame inside testarea
frame = Frame(testarea, width=280, height=300)
frame.grid()
label2 = Label(frame, text="text")
label3 = Label(frame, text="example text")
label2.grid(row=1,column=0)
label3.grid(row=4,column=0)

# Canvas
canvas = Canvas(frame, width=260, height=300, scrollregion=(0, 0, 0, 2400))
canvas.grid(row=0, column=0)

# Scrollbar
bar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
bar.grid(row=0, column=1)
canvas.config(yscrollcommand=bar.set)

# Add labels to canvas
y = 0
for i in range(1, 100):
    label = Label(canvas, text=f"Round {i}: Result", font=("Courier", 12), compound=RIGHT)
    canvas.create_window(0, y, window=label, anchor=NW)
    y += 24

root.mainloop()
