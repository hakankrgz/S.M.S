from tkinter import *
import time
import ttkthemes
from tkinter import ttk

# FONKSİYONLAR

count = 0
text = ''


def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)


def clock():
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    print(date, currenttime)
    datetimeLabel.config(text=f'    Tarih: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)


# GUİ
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')

root.geometry('1174x680+300+150')
root.resizable(False, False)
root.title('Öğrenci Yönetim Sistemi')

datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
clock()
s = 'Öğrenci Yönetim Sistemi'
sliderLabel = Label(root, font=('arial', 28, 'italic bold'), width=35)
sliderLabel.place(x=200, y=0)
slider()

connectButton = ttk.Button(root, text='Veri Tabanına Bağlan')
connectButton.place(x=980, y=0)

leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image = PhotoImage(file='student.png')
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0)

addstudentButton = ttk.Button(leftFrame, text='Öğrenci Ekle', width=25, state=DISABLED)
addstudentButton.grid(row=1, column=0, pady=20)

searchstudentButton = ttk.Button(leftFrame, text='Öğrenci Ara', width=25, state=DISABLED)
searchstudentButton.grid(row=2, column=0, pady=20)

deletestudentButton = ttk.Button(leftFrame, text='Öğrenci Sil', width=25, state=DISABLED)
deletestudentButton.grid(row=3, column=0, pady=20)

updatestudentButton = ttk.Button(leftFrame, text='Öğrenci Güncelle', width=25, state=DISABLED)
updatestudentButton.grid(row=4, column=0, pady=20)

showstudentButton = ttk.Button(leftFrame, text='Öğrenci Görüntüle', width=25, state=DISABLED)
showstudentButton.grid(row=5, column=0, pady=20)

exportstudentButton = ttk.Button(leftFrame, text='Dışa Aktar', width=25, state=DISABLED)
exportstudentButton.grid(row=6, column=0, pady=20)

exitButton = ttk.Button(leftFrame, text='Çıkış', width=25)
exitButton.grid(row=7, column=0, pady=20)

rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=820, height=600)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=(
    'NUMARA', 'İSİM', 'TEL. NO', 'E-POSTA', 'ADRES', 'CİNSİYET', 'DOĞ. TAR.', 'KAYIT TARİHİ', 'KAYIT SAATİ'),
                            xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(fill=BOTH, expand=1)

studentTable.heading('NUMARA', text='NUMARA')
studentTable.heading('İSİM', text='İSİM')
studentTable.heading('TEL. NO', text='TEL. NO')
studentTable.heading('E-POSTA', text='E-POSTA')
studentTable.heading('ADRES', text='ADRES')
studentTable.heading('CİNSİYET', text='CİNSİYET')
studentTable.heading('DOĞ. TAR.', text='DOĞ. TAR.')
studentTable.heading('KAYIT TARİHİ', text='KAYIT TARİHİ')
studentTable.heading('KAYIT SAATİ', text='KAYIT SAATİ')

studentTable.config(show='headings')

root.mainloop()
