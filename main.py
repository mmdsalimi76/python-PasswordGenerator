import random
from string import ascii_lowercase, ascii_uppercase, digits
import sqlite3
symbol_library = ['!','@','#','$','%','&','*']

# password table
conn=sqlite3.connect('C:\\Users\\mamad salimi\\Desktop\\PY\\project\\password generator final\\Passworddata.db')
cur=conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS password(
id INTEGER PRIMARY KEY,
name TEXT,
password text
)
''')
conn.close()

# user registery
conn = sqlite3.connect('C:\\Users\\mamad salimi\\Desktop\\PY\\project\\password generator final\\Passworddata.db')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    securityquestion TEXT
)
''')
conn.close()
class Password_Generator:
    def __init__(self,lenght,upper,symb,digitt):
        self.lenght=lenght
        self.upper=upper
        self.digit=digitt
        self.symb=symb
        self._password=[]
    def generate(self):
        self._password.clear()
        for up in range(self.upper):
            self._password.append(random.choice(ascii_uppercase))
        for s in range(self.symb):
            self._password.append(random.choice(symbol_library))
        for d in range(self.digit):
            self._password.append(random.choice(digits))
        rest=self.lenght-(self.digit+self.upper+self.symb)
        for r in range(rest):
            self._password.append(random.choice(ascii_lowercase))

        random.shuffle(self._password)
        final_password=''.join(self._password)
        return final_password

def reorder_ids():
    conn = sqlite3.connect('C:\\Users\\mamad salimi\\Desktop\\PY\\project\\password generator final\\Passworddata.db')
    cur = conn.cursor()


    cur.execute('''SELECT id, name, password FROM password ORDER BY id''')
    rows = cur.fetchall()


    cur.execute('''DELETE FROM password''')
    conn.commit()


    for new_id, row in enumerate(rows, start=1):
        cur.execute('''INSERT INTO password(id, name, password) VALUES(?, ?, ?)''', (new_id, row[1], row[2]))
    conn.commit()
    conn.close()
def User_input():
    P = input('What do you need this password for?')
    if P == '':
        P = 'Secret'
    L = input('Desired Lenght of Password:')
    try:
        if int(L) < 8 or L == '':
            L = 8
    except:
        L = 8

    U = input('How many Uppercase?')
    try:
        if int(U) < 1 or U == '':
            U = 1
    except:
        U = 1
    S = input('How many Symbols?')
    try:
        if int(S) < 1 or S == '':
            S = 1
    except:
        S = 1
    D = input("How many digits?")
    try:
        if int(D) < 1 or D == '':
            D = 1
    except:
        D = 1
    print('-' * 20)
    return P,L,U,S,D

def View():
    print('-' * 20)
    conn = sqlite3.connect('C:\\Users\\mamad salimi\\Desktop\\PY\\project\\password generator final\\Passworddata.db')
    cur = conn.cursor()
    V=cur.execute(
        '''SELECT * FROM password''',
    )
    New_V=[]
    for i in V:
        New_V.append(i)

    if len(New_V)==0:
        print('No Paswords Ever Created!')
    else:
        for item in New_V:
            print(f'{item[0]}- {item[1]} --> {item[2]}')
    conn.close()
    print('-' * 20)


def Delete():
    print('-' * 20)
    a=input('Which Password Do You Wish To Delete?')
    try:
        int(a)
    except ValueError:
        print('Plz enter the row number!')

    conn = sqlite3.connect('C:\\Users\\mamad salimi\\Desktop\\PY\\project\\password generator final\\Passworddata.db')
    cur = conn.cursor()
    conn.execute('''DELETE FROM password WHERE id=?''',a)
    conn.commit()
    conn.close()
    reorder_ids()
    print('-' * 20)
def program():
    while True:
        task = input('How Can I Help You?\n1.Create Password\n2.View Passwords\n3.Delete Password\nShoot!:').lower()
        if task=='1' or task=='Create Password'.lower():
            print('-' * 20)
            P,L,U,S,D=User_input()
            I=Password_Generator(int(L),int(U),int(S),int(D))
            F=I.generate()
            conn = sqlite3.connect('C:\\Users\\mamad salimi\\Desktop\\PY\\project\\password generator final\\Passworddata.db')
            cur = conn.cursor()
            cur.execute(
                '''INSERT INTO password(name,password) VALUES(?,?)''',(P,F)
            )
            conn.commit()
            conn.close()

            print(f'Here You Go! --> {F}')
            print('-'*20)
        elif task=='2' or task=='View Passwords'.lower() or task=='View'.lower():
            View()

        elif task=='3' or task=='Delete Password'.lower() or task=='Delete'.lower():
            View()
            Delete()

def forgot_password():
    conn = sqlite3.connect('C:\\Users\\mamad salimi\\Desktop\\PY\\project\\password generator final\\Passworddata.db')
    cur = conn.cursor()
    V = cur.execute(
        '''SELECT * FROM user''',
    )
    secq = [i for i in V]
    conn.close()
    shut_count=0
    while True:
        qq=input('Security Question: Whats the last 4 digits of your phone number?')
        if qq==secq[0][3]:
            print(f'Your Password is {secq[0][2]} and your Username is {secq[0][1]}\n Try to remember it this time!')
            print('-'*20)
            user_check()
            break
        else:
            shut_count+=1
            if shut_count>5:
                print('Exiting Program...')
                break





def User_register():
    while True:
        us=input('Choose a UserName:')
        ps=input('Choose a Password:')
        sq=input('Security Question: Enter The Last 4 digits of your Phone Number:')
        if len(us)<8 or len(ps)<8 or len(sq)<4:
            print('Username and Password Must Be 8 Characters or Longer')
        else:
            break

    conn = sqlite3.connect('C:\\Users\\mamad salimi\\Desktop\\PY\\project\\password generator final\\Passworddata.db')
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO user(username,password,securityquestion) VALUES(?,?,?)''', (us,ps,sq)
    )
    conn.commit()
    conn.close()
    print('-' * 20)

def user_login():
    conn = sqlite3.connect('C:\\Users\\mamad salimi\\Desktop\\PY\\project\\password generator final\\Passworddata.db')
    cur = conn.cursor()
    V = cur.execute(
        '''SELECT * FROM user''',
    )
    uc=[i for i in V]
    conn.close()
    count=0
    while True:
        u_l=input('Enter Your Username:')
        p_l=input('Enter Your Password:')

        if u_l==uc[0][1] and p_l==uc[0][2]:
            print("Access Granted!")
            print('-' * 20)

            break
        else:
            print('Access Denied!')
            count+=1
            if count>3:
                print('Too Many Wrong answers!')
                print('-' * 20)
                forgot_password()

            print('-' * 20)




def user_check():
    while True:
        conn = sqlite3.connect(
            'C:\\Users\\mamad salimi\\Desktop\\PY\\project\\password generator final\\Passworddata.db')
        cur = conn.cursor()
        _User = cur.execute(
            '''SELECT * FROM user''',
        )
        UserData=[i for i in _User]

        conn.close()
        if len(UserData)==0:
            User_register()
        else:
            user_login()
            program()

user_check()



