import json
from random import randint
#users.json ve activation.txt has been used

class System:
    def __init__(self):
        self.status = True
        self.datas = self.getDatas()

    def run(self):
        self.menu()
        choice = self.choicemenu()

        if choice==1:
            self.login()
        if choice==2:
            self.signin()
        if choice==3:
            self.forgotmyPassword()
        if choice==4:
            self.exit()

    def menu(self):
        print("""
1- Log in
2- Sign in
3- I forgot my password
4- Exit
        """)

    def choicemenu(self):
        while True:
            try:
                choice = int(input("Enter your choice: "))
                while choice<1 or choice>4:
                    choice = int(input("Please enter a value between 1-4: "))
                break
            except ValueError:
                print("Please enter an integer!\n")
        return choice

    def getDatas(self):
        try:
            with open("users.json","r") as file:
                datas = json.load(file)
        except FileNotFoundError:
            with open("users.json","w") as file:
                file.write("{}")
            with open("users.json", "r") as file:
                    datas = json.load(file)
        return datas

    def login(self):
        username = input("Enter your user name: ")
        passw = input("Enter your password: ")

        status = self.checkit(username,passw)

        if status:
            self.loginSuccessfull()
        else:
            self.loginFailed("Entered informations are incorrect!")

    def signin(self):
        username = input("Enter your username: ")
        while True:
            passw = input("Enter your password: ")
            apassw = input("Re-enter your password: ")
            if passw == apassw:
                break
            else:
                print("Passwords do not match. Please re-enter.")

        email = input("Enter your e-mail adress: ")

        status = self.isThereRegis(username,email)
        if status:
            print("This username or e-mail is already registered in the system.")
        else:
            activationcode = self.SendACtivationCode()
            actstatus = self.checkActivationC(activationcode)

            if actstatus:
                self.save(username,passw,email)
            else:
                print("Activation invalid!")

    def forgotmyPassword(self):
        email = input("Enter your e-mail adress: ")
        if self.isTheremail(email):
            with open("activation.txt","w")as file:
                activation = str(randint(1000,9999))
                file.write(activation)

            enteract = input("To change your password, enter the activation code we sent: ")
            if enteract == activation:
                while True:
                    newpassw = input("Enter your new password: ")
                    anewpassw = input("Re-enter your new password: ")

                    if newpassw == anewpassw:
                        break
                    else:
                        print("Passwords do not match. Please re-enter.")

            self.datas = self.getDatas()

            for user in self.datas["users"]:
                if user["email"] == email:
                    user["password"] = str(newpassw)

            with open("users.json","w") as file:
                json.dump(self.datas,file)
                print("Password has been changed successfully.")

        else:
            print("There is no such an e-mail registered in our system..")


    def isTheremail(self,email):
        self.datas = self.getDatas()

        for user in self.datas["users"]:
            if user["email"] == email:
                return True
        return False

    def checkit(self,username,passw):
        self.datas = self.getDatas()

        try:
            for user in self.datas["users"]:
                if user["username"] == username and user["password"] == passw and user["timeout"]=="0" and user["activation"]=="Y":
                    return True
        except:
            return False

    def loginFailed(self,reason):
        print(reason)

    def loginSuccessfull(self):
        print("Welcome!")
        self.status = False

    def isThereRegis(self,username,email):
        self.datas = self.getDatas()

        try:
            for user in self.datas["users"]:
                if user["username"] == username and user["email"] == email:
                    return True
        except :
            return False

        return False

    def SendACtivationCode(self):
       with open("activation.txt","w") as file:
           activation = str(randint(1000,9999))
           file.write(activation)

       return activation


    def checkActivationC(self,activation):
        getactcode = input("Enter the activation code: ")
        if activation == getactcode:
            return True
        else:
            return False


    def save(self,username,passw,email):
        self.datas = self.getDatas()

        try:
            self.datas["users"].append({"username": username,"password": passw,"email": email,"activation":"Y","timeout":"0"})
        except KeyError:
            self.datas["users"] = []
            self.datas["users"].append({"username": username,"password": passw,"email": email,"activation":"Y","timeout":"0"})

        with open("users.json","w") as file:
            json.dump(self.datas,file)
            print("The register was created successfully!")


    def exit(self):
        self.status = False



system = System()
while system.status:
    system.run()