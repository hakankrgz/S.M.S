from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import webbrowser
import mysql.connector


# FONKSİYONLAR
def clear():
    emailEntry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirmEntry.delete(0, END)
    check.set(0)


def connect_database(event):
    if emailEntry.get() == '' or usernameEntry.get() == '' or passwordEntry.get() == '' or confirmEntry.get() == '':
        messagebox.showerror('Error', 'Tüm alanlar zorunludur!')
    elif passwordEntry.get() != confirmEntry.get():
        messagebox.showerror('Error', 'Şifreler Uyuşmuyor!')
    elif check.get() == 0:
        messagebox.showerror('Error', 'Lütfen "Şartlar ve Koşulları" Kabul Edin!')
    else:
        try:
            con = mysql.connector.connect(host='localhost', user='root', password='')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Veritabanı Bağlantısında Hata Var, Tekrar Dene')
            return

        try:
            query = 'CREATE DATABASE userdata'
            mycursor.execute(query)
            query = 'USE userdata'
            mycursor.execute(query)
            query = 'CREATE TABLE data (id INT AUTO_INCREMENT PRIMARY KEY not null, email varchar(50),username varchar(100),password varchar(20))'
            mycursor.execute(query)
        except:
            mycursor.execute('USE userdata')

        query = 'SELECT * from data where username=%s'
        mycursor.execute(query, (usernameEntry.get(),))

        row = mycursor.fetchone()
        if row != None:
            messagebox.showerror('Error', 'Kullanıcı Adı Mevcut!')
        else:
            query = 'INSERT INTO data(email,username,password) values(%s,%s,%s)'
            mycursor.execute(query, (emailEntry.get(), usernameEntry.get(), passwordEntry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Succes', 'Kayıt başarılı.')
            clear()
            signup_window.destroy()
            import signin


def login_page(event):
    signup_window.destroy()
    import signin


# GUI
signup_window = Tk()

background = ImageTk.PhotoImage(file='bg.jpg')
signup_window.title('Kayıt Ol')
signup_window.resizable(False, False)

bgLabel = Label(signup_window, image=background)
bgLabel.grid()

frame = Frame(signup_window, bg='white')
frame.place(x=560, y=100)

heading = Label(frame, text='KAYIT OL', font=("Microsoft Yahei UI Light", 24, 'bold'), bg='white',
                fg='firebrick1')
heading.grid(row=0, column=0, padx=45, pady=10)

emailLabel = Label(frame, text='E-posta', font=("Microsoft Yahei UI Light", 12, 'bold'), bg='white', fg='firebrick1')
emailLabel.grid(row=1, column=0, sticky='w', padx=23, pady=(10, 0))

emailEntry = Entry(frame, width=25, font=("Microsoft Yahei UI Light", 12, 'bold'), fg='white', bg='firebrick1',
                   borderwidth=0, highlightthickness=0)
emailEntry.grid(row=2, column=0, sticky='w', padx=25)

usernameLabel = Label(frame, text='Kullanıcı Adı', font=("Microsoft Yahei UI Light", 12, 'bold'), bg='white',
                      fg='firebrick1')
usernameLabel.grid(row=3, column=0, sticky='w', padx=23, pady=(10, 0))

usernameEntry = Entry(frame, width=25, font=("Microsoft Yahei UI Light", 12, 'bold'), fg='white', bg='firebrick1',
                      borderwidth=0, highlightthickness=0)
usernameEntry.grid(row=4, column=0, sticky='w', padx=25)

passwordLabel = Label(frame, text='Şifre', font=("Microsoft Yahei UI Light", 12, 'bold'), bg='white',
                      fg='firebrick1')
passwordLabel.grid(row=5, column=0, sticky='w', padx=23, pady=(10, 0))

passwordEntry = Entry(frame, width=25, font=("Microsoft Yahei UI Light", 12, 'bold'), fg='white', bg='firebrick1',
                      borderwidth=0, highlightthickness=0)
passwordEntry.grid(row=6, column=0, sticky='w', padx=25)

confirmLabel = Label(frame, text='Şifreyi Doğrula', font=("Microsoft Yahei UI Light", 12, 'bold'), bg='white',
                     fg='firebrick1')
confirmLabel.grid(row=7, column=0, sticky='w', padx=23, pady=(10, 0))

confirmEntry = Entry(frame, width=25, font=("Microsoft Yahei UI Light", 12, 'bold'), fg='white', bg='firebrick1',
                     borderwidth=0, highlightthickness=0)
confirmEntry.grid(row=8, column=0, sticky='w', padx=25)

check = IntVar()
termsandconditions = Checkbutton(frame, text='Şartlar ve Koşulları kabul ediyorum.',
                                 font=("Microsoft Yahei UI Light", 12), fg='black', bg='white',
                                 cursor='hand', variable=check)
termsandconditions.grid(row=9, column=0, pady=10)

signupLabel = Label(frame, text='                   KAYIT OL                   ',
                    font=('Open Sans', 19, 'bold'), fg='white', bg='firebrick1', cursor='hand2', height=2)
signupLabel.grid(row=10, column=0, padx=13, pady=15)
signupLabel.bind("<Button-1>", connect_database)

signinLabel = Label(frame, text='Hesabın var mı?\nGiriş yapmak için tıkla!', font=('Open Sans', 12, 'bold'),
                    fg='firebrick1', bg='white', cursor='hand2')
signinLabel.bind("<Button-1>", login_page)
signinLabel.grid(row=11, column=0)

signup_window.mainloop()
