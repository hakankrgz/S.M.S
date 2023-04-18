from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import mysql.connector


# Fonksiyonlar
def openeye_label(event):
    eyeLabel.configure(image=openeye)
    passwordEntry.config(show='')
    eyeLabel.bind("<Button-1>", closeye_label)


def closeye_label(event):
    eyeLabel.configure(image=closeye)
    passwordEntry.config(show='*')
    eyeLabel.bind("<Button-1>", openeye_label)


def signup_label(event):
    login_window.destroy()
    import signup


def login_user(event):
    if usernameEntry.get() == '' or passwordEntry.get() == '' or usernameEntry.get() == 'Kullanıcı Adı' or passwordEntry.get() == 'Şifre':
        messagebox.showerror('Error', 'Tüm Alanları Doldurmalısın!')


    else:
        try:
            con = mysql.connector.connect(host='localhost', user='root', password='')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Veritabanı Bağlantısında Hata Var, Tekrar Dene')
            return
        query = 'USE userdata'
        mycursor.execute(query)
        query = 'select * from data where username=%s and password=%s'
        mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
        row = mycursor.fetchone()
        if row == None:
            messagebox.showerror('Error', 'Geçersiz Kullanıcı Adı veya Şifre')
        else:
            messagebox.showinfo('Welcome', 'Giriş Başarılı!')
            login_window.destroy()
            import sms


def forget_pass(event):
    def change_password(event):
        if usernameEntry.get() == '' or newpass_entry.get() == '' or confirmpass_entry.get() == '':
            messagebox.showerror('Error', 'Tüm Alanları Doldurmalısın!', parent=window)
        elif newpass_entry.get() != confirmpass_entry.get():
            messagebox.showerror('Error', 'Şifreler Uyuşmuyor!', parent=window)
        else:
            con = mysql.connector.connect(host='localhost', user='root', password='', database='userdata')
            mycursor = con.cursor()
            query = 'SELECT * FROM data WHERE username=%s'
            mycursor.execute(query, (user_entry.get(),))
            row = mycursor.fetchone()
            if row is None:
                messagebox.showerror('Error', 'Geçersiz Kullanıcı Adı', parent=window)
            else:
                query = 'UPDATE data SET password=%s WHERE username=%s'
                mycursor.execute(query, (newpass_entry.get(), user_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'Şifre Değiştirildi. Lütfen yeni şifre ile giriş yapınız')
                window.destroy()

    window = Toplevel()
    window.title('Şifremi Unuttum')

    bgPic = ImageTk.PhotoImage(file='background.jpg')
    bglabel = Label(window, image=bgPic)
    bglabel.grid()

    heading_label = Label(window, text='ŞİFRE SIFIRLA', font=('arial', 23, 'bold'), bg='white', fg='magenta2')
    heading_label.place(x=510, y=60)

    userLabel = Label(window, text='Kullanıcı Adı', font=('arial', 12, 'bold'), bg='white', fg='orchid1')
    userLabel.place(x=470, y=130)

    user_entry = Entry(window, width=25, fg='magenta2', font=("arial", 11, 'bold'), bd=0, borderwidth=0,
                       highlightthickness=0)
    user_entry.place(x=470, y=160)

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=180)

    passwordLabel = Label(window, text='Yeni Şifre', font=('arial', 12, 'bold'), bg='white', fg='orchid1')
    passwordLabel.place(x=470, y=210)

    newpass_entry = Entry(window, width=25, fg='magenta2', font=("arial", 11, 'bold'), bd=0, borderwidth=0,
                          highlightthickness=0)
    newpass_entry.place(x=470, y=240)

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=260)

    confirmpassLabel = Label(window, text='Yeni Şifre Tekrar', font=('arial', 12, 'bold'), bg='white', fg='orchid1')
    confirmpassLabel.place(x=470, y=290)

    confirmpass_entry = Entry(window, width=25, fg='magenta2', font=("arial", 11, 'bold'), bd=0, borderwidth=0,
                              highlightthickness=0)
    confirmpass_entry.place(x=470, y=320)

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=340)

    submitLabel = Label(window, text='                   GÖNDER                   ',
                        font=('Open Sans', 19, 'bold'), fg='white', bg='magenta2', cursor='hand2')
    submitLabel.place(x=470, y=390)
    submitLabel.bind("<Button-1>", change_password)

    window.mainloop()


def user_enter(event):
    if usernameEntry.get() == 'Kullanıcı Adı':
        usernameEntry.delete(0, END)


def password_enter(event):
    if passwordEntry.get() == 'Şifre':
        passwordEntry.delete(0, END)


# GUI
login_window = Tk()
login_window.geometry('990x660+360+150')
login_window.resizable(False, False)
login_window.title('Giriş Yap')
bgImage = ImageTk.PhotoImage(file='bg.jpg')

bgLabel = Label(login_window, image=bgImage)
bgLabel.place(x=0, y=0)

heading = Label(login_window, text='KULLANICI GİRİŞİ', font=("Microsoft Yahei UI Light", 23, 'bold'), bg='white',
                fg='firebrick1')
heading.place(x=605, y=120)

usernameEntry = Entry(login_window, width=25, font=("Microsoft Yahei UI Light", 11, 'bold'), bg='white', borderwidth=0,
                      highlightthickness=0, fg='firebrick1')
usernameEntry.place(x=580, y=200)
usernameEntry.insert(0, 'Kullanıcı Adı')
usernameEntry.bind('<FocusIn>', user_enter)

fram1 = Frame(login_window, width=250, height=2, bg='firebrick1')
fram1.place(x=580, y=222)

passwordEntry = Entry(login_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bg='white', borderwidth=0,
                      highlightthickness=0, fg='firebrick1')
passwordEntry.place(x=580, y=260)
passwordEntry.insert(0, 'Şifre')
passwordEntry.bind('<FocusIn>', password_enter)

fram2 = Frame(login_window, width=250, height=2, bg='firebrick1')
fram2.place(x=580, y=282)

openeye = ImageTk.PhotoImage(Image.open('openeye.png'))
closeye = ImageTk.PhotoImage(Image.open('closeye.png'))
eyeLabel = Label(login_window, image=closeye, bg='white')
eyeLabel.place(x=800, y=253)
eyeLabel.bind("<Button-1>", openeye_label)

forgetLabel = Label(login_window, text='Şifreyi Unuttum!',
                    font=('Microsoft Yahei UI Light', 10, 'bold'), fg='firebrick1', bg='white', cursor='hand2')
forgetLabel.place(x=725, y=295)
forgetLabel.bind("<Button-1>", forget_pass)

loginLabel = Label(login_window, text='                       GİRİŞ                       ',
                   font=('Open Sans', 19, 'bold'), fg='white', bg='firebrick1', cursor='hand2')
loginLabel.place(x=578, y=350)
loginLabel.bind("<Button-1>", login_user)

orLabel = Label(login_window, text='--------------VEYA--------------', font=('Open Sans', 16), fg='firebrick1',
                bg='white')
orLabel.place(x=580, y=390)

facebook_logo = ImageTk.PhotoImage(Image.open('facebook.png'))
fbLabel = Label(login_window, image=facebook_logo, bg='white')
fbLabel.place(x=640, y=440)

google_logo = ImageTk.PhotoImage(Image.open('google.png'))
googleLabel = Label(login_window, image=google_logo, bg='white')
googleLabel.place(x=690, y=440)

twitter_logo = ImageTk.PhotoImage(Image.open('twitter.png'))
twitterLabel = Label(login_window, image=twitter_logo, bg='white')
twitterLabel.place(x=740, y=440)

signupLabel = Label(login_window, text='Hesabın yok mu? O halde Kayıt Ol', font=('Open Sans', 10, 'bold'),
                    fg='firebrick1', bg='white', cursor='hand2')
signupLabel.bind("<Button-1>", signup_label)
signupLabel.place(x=615, y=500)

login_window.mainloop()
