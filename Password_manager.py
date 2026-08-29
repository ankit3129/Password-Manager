import json
import pprint
from cryptography.fernet import Fernet
import string
import secrets
Data = []

def keyload():
    try:
        with open("key.key", "rb") as file:
            key = file.read()

    except FileNotFoundError:
        key = Fernet.generate_key()

        with open("key.key", "wb") as file:
            file.write(key)

    return key

def jsondump():
    global Data

    key = keyload()
    fernet = Fernet(key)

    data = json.dumps(Data).encode()
    encrypted = fernet.encrypt(data)

    with open("Enpassdata.json", "wb") as file:
        file.write(encrypted)

def jsonload():
    global Data

    try:
        key = keyload()

        with open("Enpassdata.json", "rb") as file:
            encrypted_data = file.read()
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        Data = json.loads(decrypted_data)

    except FileNotFoundError:
        Data = []
    except Exception:
        print("Could not decrypt the password database.")
        Data = []

def addpass():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    website = input("Enter your website: ")
    passdata = {
        "Username": username,
        "Password": password,
        "Website": website
    }
    Data.append(passdata)
    jsondump()

def viewpass():
    global Data
    ch = int(input("Do you wish to view 1.all pass 2.single pass: "))
    if ch == 1:
        pprint.pprint(Data)
    elif ch == 2:
        ch1 = input("Enter the website name: ")
        found = False
        for pwd in Data:
            if pwd["Website"] == ch1:
                found = True
                print(
                    "website:", pwd["Website"],
                    "username:", pwd["Username"],
                    "password:", pwd["Password"]
                )

        if found == False:
            print("No such data found")


def delete():
    global Data
    ch = input(
        "Enter the website's name whose password you wish to delete: "
    )
    found = False
    for pwd in Data:
        if pwd["Website"] == ch:
            found = True
            Data.remove(pwd)
            jsondump()
            break
    if found == False:
        print("Data doesn't exist")

def generate_pass():
    a = int(input("How long do you need your password: "))
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(
            secrets.choice(alphabet)
            for i in range(a)
        )
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
        ):
            break
    print("Your password is:", password)


def passedit():
    ch = input(
        "Enter the website name whose password you wish to edit: "
    )
    found = False

    for pwd in Data:
        if pwd["Website"] == ch:
            found = True
            chk = input("Enter your new password: ")
            pwd["Password"] = chk
            jsondump()
            break
    if found == False:
        print("No such data found")

def exitpr():
    exit()

jsonload()

while True:

    kimono = int(input('''
What do you wish to do

1. Add password
2. View password
3. Delete password
4. Generate password
5. Edit password
6. Exit program

Your choice: '''))

    if kimono == 1:
        addpass()

    elif kimono == 2:
        viewpass()

    elif kimono == 3:
        delete()

    elif kimono == 4:
        generate_pass()

    elif kimono == 5:
        passedit()

    elif kimono == 6:
        exitpr()

    else:
        print("Wrong input")
        break