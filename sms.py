from tkinter import *
import time
import ttkthemes
from tkinter import messagebox, ttk, filedialog
import mysql.connector
from PIL import ImageTk
import pandas as pd


# FONKSİYONLAR
def iexit():
    result = messagebox.askyesno('Confirm', 'Çıkış yapmak istiyor musunuz?')
    if result:
        root.destroy()
    else:
        pass


def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.xlsx')
    indexing = studentTable.get_children()
    newlist = []
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    table = pd.DataFrame(newlist,
                         columns=['NUMARA', 'İSİM', 'TELEFON', 'E-POSTA', 'ADRES', 'CİNSİYET', 'DOĞ. TAR.',
                                  'KAYIT TARİHİ', 'KAYIT SAATİ'])
    table.to_excel(url, index=False)
    messagebox.showinfo('Succes', 'Dosya başarıyla dışa aktarıldı.')


def toplevel_data(title, button_text, command):
    global idEntry, phoneEntry, nameEntry, emailEntry, addressEntry, genderEntry, dobEntry, screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    idLabel = Label(screen, text='Numara', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='İsim', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='Telefon', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text='E-posta', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(screen, text='Adres', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(screen, text='Cinsiyet', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(screen, text='Doğ. Tar.', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)
    if title == 'Öğrenci Güncelle':
        indexing = studentTable.focus()

        content = studentTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])


def update_data():
    query = 'update student set name=%s,mobile=%s,email=%s,address=%s,gender=%s,dob=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query, (
        nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(),
        date, currenttime, idEntry.get()))
    con.commit()
    messagebox.showinfo('Succes', f'{idEntry.get()} numaralı kişi başarıyla güncellendi.', parent=screen)
    screen.destroy()
    show_student()


def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def delete_student():
    indexing = studentTable.focus()
    print(indexing)
    content = studentTable.item(indexing)
    content_id = content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query, (content_id,))
    con.commit()
    messagebox.showinfo('Deleted', f'{content_id} numaralı kişi başarıyla silindi.')
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def search_data():
    query = 'select * from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'
    mycursor.execute(query, (
        idEntry.get(), nameEntry.get(), emailEntry.get(), phoneEntry.get(), addressEntry.get(), genderEntry.get(),
        dobEntry.get(),))
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def add_data():
    if idEntry.get() == '' or nameEntry.get() == '' or phoneEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '':
        messagebox.showerror('Error', 'Tüm Alanlar Doldurulmalı!', parent=screen)

    else:
        try:
            query = 'insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query, (
                idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
                genderEntry.get(), dobEntry.get(), date, currenttime))
            con.commit()
            result = messagebox.askyesno('Confirm', 'Veri Başarıyla Eklendi. Formu Temizlemek İstiyor Musunuz?',
                                         parent=screen)
            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)
            else:
                pass
        except:
            messagebox.showerror('Error', 'Var Olan Numara Girilmez!', parent=screen)
            return

        query = 'select * from student'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            datalist = list(data)
            studentTable.insert('', END, values=datalist)


def connect_database():
    def connect():
        global mycursor, con
        try:
            con = mysql.connector.connect(host=hostEntry.get(), user=usernameEntry.get(), password='')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Geçersiz Giriş!', parent=connectWindow)
            return
        try:
            query = 'create database userdata'
            mycursor.execute(query)
            query = 'USE userdata'
            mycursor.execute(query)
            query = 'create table student(id int not null primary key, name varchar(30), mobile varchar(10), email varchar(30), ' \
                    'address varchar(100), gender varchar(20), dob varchar(20), date varchar(50), time varchar(50))'
            mycursor.execute(query)

        except:
            query = 'use userdata'
            mycursor.execute(query)
        messagebox.showinfo('Succes', 'Veri Tabanı Bağlantısı Başarılı.', parent=connectWindow)
        connectWindow.destroy()
        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Veri Tabanına Bağlan')
    connectWindow.resizable(False, False)

    hostnameLabel = Label(connectWindow, text='Host Name', font=('arial', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=20)

    hostEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton = ttk.Button(connectWindow, text='CONNECT', command=connect)
    connectButton.grid(row=3, columnspan=2)


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
    global date, currenttime
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
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

connectButton = ttk.Button(root, text='Veri Tabanına Bağlan', command=connect_database)
connectButton.place(x=980, y=0)

leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image = ImageTk.PhotoImage(file='student.png')
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0)

addstudentButton = ttk.Button(leftFrame, text='Öğrenci Ekle', width=25, state=DISABLED,
                              command=lambda: toplevel_data('Öğrenci Ekle', 'Ekle', add_data))
addstudentButton.grid(row=1, column=0, pady=20)

searchstudentButton = ttk.Button(leftFrame, text='Öğrenci Ara', width=25, state=DISABLED,
                                 command=lambda: toplevel_data('Öğrenci Ara', 'Ara', search_data))
searchstudentButton.grid(row=2, column=0, pady=20)

deletestudentButton = ttk.Button(leftFrame, text='Öğrenci Sil', width=25, state=DISABLED, command=delete_student)
deletestudentButton.grid(row=3, column=0, pady=20)

updatestudentButton = ttk.Button(leftFrame, text='Öğrenci Güncelle', width=25, state=DISABLED,
                                 command=lambda: toplevel_data('Öğrenci Güncelle', 'Güncelle', update_data))
updatestudentButton.grid(row=4, column=0, pady=20)

showstudentButton = ttk.Button(leftFrame, text='Öğrenci Görüntüle', width=25, state=DISABLED, command=show_student)
showstudentButton.grid(row=5, column=0, pady=20)

exportstudentButton = ttk.Button(leftFrame, text='Dışa Aktar/Yazdır', width=25, state=DISABLED, command=export_data)
exportstudentButton.grid(row=6, column=0, pady=20)

exitButton = ttk.Button(leftFrame, text='Çıkış', width=25, command=iexit)
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

studentTable.column('NUMARA', width=65, anchor=CENTER)
studentTable.column('İSİM', width=200, anchor=CENTER)
studentTable.column('TEL. NO', width=100, anchor=CENTER)
studentTable.column('E-POSTA', width=200, anchor=CENTER)
studentTable.column('ADRES', width=300, anchor=CENTER)
studentTable.column('TEL. NO', width=100, anchor=CENTER)
studentTable.column('CİNSİYET', width=65, anchor=CENTER)
studentTable.column('DOĞ. TAR.', width=100, anchor=CENTER)
studentTable.column('KAYIT TARİHİ', width=100, anchor=CENTER)
studentTable.column('KAYIT SAATİ', width=100, anchor=CENTER)

style = ttk.Style()

style.configure('Treeview', rowheight=40, font=('arial', 13, 'bold'), background='white')
style.configure('Treeview.Heading', font=('arial', 13, 'bold'))

studentTable.config(show='headings')

root.mainloop()
