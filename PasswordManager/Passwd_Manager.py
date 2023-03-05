import random,   string, hashlib, getpass
from sys import argv, exit
from json import dump, load
from colorama import Fore, Style
from cryptography.fernet import Fernet


def hash(password):
    #Generate a salt string
    salt = """Est un constructeur générique qui prend comme premier paramètre le nom de l'algorithme désiré (name) . Il existe pour permettre l'accès aux algorithmes listés ci-dessus ainsi qu'aux autres algorithmes que votre librairie OpenSSL peut offrir. Les constructeurs nommés sont beaucoup plus rapides que new() et doivent être privilégiés."""

    # Instanciating a new SHA-512
    sha512 = hashlib.sha512()

    sha512.update((password+salt).encode())

    return sha512.hexdigest()


def Get_Fernet():
    # Load the secret key from the .key file.
    with open('DateBase/.key', 'rb') as keyfile :
        key = keyfile.read()
    
    return Fernet(key)


def Encrypt_Passwrds_Record():
    fernet= Get_Fernet()
    
    with open('DateBase/Passwords_Register.json', 'rb') as file:        
        Clrear_Data = file.read()
        
    # Encrypt the file data
    encrypted_data = fernet.encrypt(Clrear_Data)


    with open('DateBase/Passwords_Register.json', 'wb') as file:
        file.write(encrypted_data)
        
        
def Decrypt_Password_Record():
    fernet= Get_Fernet()

    with open('DateBase/Passwords_Register.json', 'rb') as file:
        encrypted_data = file.read()
        
    # Decrypt the file data
    decrypted_data = fernet.decrypt(encrypted_data)
        
    with open('DateBase/Passwords_Register.json', 'wb') as file:
        file.write(decrypted_data)
    
# Initialize the necessary files to store the program data 
def init():
    
    UserPassword = getpass.getpass("\n\t>>Please do enter your password   :  ")

    #Store the user authentication password
    with open('DateBase/UserPassword.hash', 'w') as user_password_file:
        user_password_file.write(hash(UserPassword))

    # Create  a passwords register file
    with open('DateBase/Passwords_Register.json', 'w') as password_register:
        dump([], password_register, indent=4)
        
    # Generate a secret key and save it to a hidden file.
    key = Fernet.generate_key()
    with open('DateBase/.key', 'wb') as key_file:
        key_file.write(key)
        
    # Encrypt the password register
    Encrypt_Passwrds_Record()

    print("\nInitialization is done successfully.\n")


def authenticate_user():
    for i in range(3):

        Password = getpass.getpass("\n\t>>Please do enter your password   :  ")

        with open('DateBase/UserPassword.hash', 'r') as user_password_file:
            stored_password_hash = user_password_file.read()

        if stored_password_hash == hash(Password):

            break

        else:
            print(Fore.RED+'\nUnvalid password !! '+Style.RESET_ALL)

        if i == 2:
            exit()


def generate_new_password(len):
    
    # Create a dictionay 
    Dictionary = string.ascii_letters + string.digits + string.punctuation.replace('"', '').replace("'", '').replace('\\', '')
        
    Decrypt_Password_Record()

    passwords_list = []
    with open('DateBase/Passwords_Register.json', 'r') as register_file:
        passwords_list = load(register_file)
        
    Encrypt_Passwrds_Record()
    
    # Check if the password already exists in the password register => Password duplication is not allowed
    while True:
        New_Password = ''.join(random.choice(Dictionary) for i in range(len))

        if not any(New_Password == psswd_record['Password'] for psswd_record in passwords_list):
            break

    return New_Password


def Service_Exists(service):
    
    Decrypt_Password_Record()
    
    with open('DateBase/Passwords_Register.json', 'r') as register_file:
        passwords_list = load(register_file)
        
    Encrypt_Passwrds_Record()

    return any(service == psswd_record['Service'] for psswd_record in passwords_list)


# Retreive the password from the password register
def Get_Password(service):
    
    Decrypt_Password_Record()
    
    with open('DateBase/Passwords_Register.json', 'r') as register_file:
        passwords_list = load(register_file)
        
    Encrypt_Passwrds_Record()

    for password_record in passwords_list:
        if password_record['Service'] == service:
            corresponding_password = password_record['Password']

    return corresponding_password


def Create_New_Password():
    
    # Check if a password already exists for the given service
    if not Service_Exists(argv[3]):

        New_Password = generate_new_password(int(argv[2]))

        Password_Record = {
            'Service': argv[3],
            'Password': New_Password
        }

        Password_Record_data = []
        
        Decrypt_Password_Record()
        
        with open('DateBase/Passwords_Register.json', 'r') as Passwords_Register:
            Password_Record_data = load(Passwords_Register)

        # Add the new password record to the register
        Password_Record_data.append(Password_Record)

        with open('DateBase/Passwords_Register.json', 'w') as Passwords_Register:

            dump(Password_Record_data, Passwords_Register, indent=4)
            
        Encrypt_Passwrds_Record()

        print('\nHere is the genarated password for ' +
              argv[3]+'  is : \n\n\t'+Fore.RED+New_Password+Style.RESET_ALL+'\n')

    # In case a password already exists for the service
    else:
        print('You already do have a password for this service !! ')
        option = input('Press :   <'+Fore.YELLOW+' s '+Style.RESET_ALL + '> To see the password  | <'+Fore.YELLOW+' c '+Style.RESET_ALL+'>  To cancel   ')

        if option == 's':

            print('\nHere is your password for ' +
                  argv[3]+' : \n\n\t'+Fore.RED + Get_Password(argv[3]) + Style.RESET_ALL+'\n')

        elif option == 'c':
            exit()
        else:
            print(Fore.RED+'\nError : Unvalid input'+Style.RESET_ALL)


def Update_password():
    
    # Check fisrt if a password already exists for the given service
    if Service_Exists(argv[3]):

        choice = input('\nPress :   <'+Fore.YELLOW+' y '+Style.RESET_ALL +'> to confirm password update  | <'+Fore.YELLOW+' n '+Style.RESET_ALL+'>  to cancel   ')

        if choice == 'y':

            New_Password = generate_new_password(int(argv[2]))

            Updated_Password_Record = {
                'Service': argv[3],
                'Password': New_Password
            }

            Decrypt_Password_Record()
            
            Password_Record_data = []
            with open('DateBase/Passwords_Register.json', 'r') as Passwords_Register:
                Password_Record_data = load(Passwords_Register)

            # Fister the password register to eliminate the old password
            Updated_Password_Record_data = [record for record in Password_Record_data if record['Service'] != argv[3]]

            # Add the new password record to the file 
            Updated_Password_Record_data.append(Updated_Password_Record)

            with open('DateBase/Passwords_Register.json', 'w') as Passwords_Register:
                dump(Updated_Password_Record_data,Passwords_Register, indent=4)
                
                
            Encrypt_Passwrds_Record()
            

            print('\nYour password has been updated successfully\n')
            print('Your updated password for  '+Fore.GREEN +
                  argv[3]+Style.RESET_ALL+'  is : \n\n\t'+Fore.RED+New_Password+Style.RESET_ALL+'\n')

        elif choice == 'n':
            exit()
        else:
            print(Fore.RED+'\nError : Unvalid input'+Style.RESET_ALL)

    # In case the user does not posess a password for this provided service >> allow the creation of one
    else:
        print('\n\tYou do not have a password for the spesified service !! \n')
        option = input('Press :   <'+Fore.YELLOW+' y '+Style.RESET_ALL +'> to create a password  | <'+Fore.YELLOW+' n '+Style.RESET_ALL+'>  to cancel   ')

        if option == 'y':

            Create_New_Password()

        elif option == 'n':

            exit()

        else:

            print(Fore.RED+'\nError : Unvalid input'+Style.RESET_ALL)


def Create_New_Password_V2():
    
    print('\n\tYou do not have a password for the spesified service !! \n')
    option = input('Press :   <'+Fore.YELLOW+' y '+Style.RESET_ALL +'> to create a password  | <'+Fore.YELLOW+' n '+Style.RESET_ALL+'>  to cancel   ')

    if option == 'y':
    
        len = int(input('Enter the length of the password  :  '))
        
        
        New_Password = generate_new_password(len)

        Password_Record = {
            'Service': argv[2],
            'Password': New_Password
        }
        
        
        Decrypt_Password_Record()

        Password_Record_data = []
        with open('DateBase/Passwords_Register.json', 'r') as Passwords_Register:
            
            Password_Record_data = load(Passwords_Register)

        Password_Record_data.append(Password_Record)

        with open('DateBase/Passwords_Register.json', 'w') as Passwords_Register:

            dump(Password_Record_data, Passwords_Register, indent=4)
            
        Encrypt_Passwrds_Record()

        print('\nHere is the genarated password for '+   argv[2]+'  is : \n\t'+Fore.RED+New_Password+Style.RESET_ALL+'\n')
    
    elif option == 'n':

            exit()

    else:
            print(Fore.RED+'\nError : Unvalid input'+Style.RESET_ALL)
                    
    
def Show_Password():

    if Service_Exists(argv[2]):
        
        print('\nHere is your password for ' +argv[2]+' : \n\n\t'+Fore.RED + Get_Password(argv[2]) + Style.RESET_ALL+'\n')
        
    else:
        Create_New_Password_V2()


def Delete_Password():
    
    # Check fisrt if a password for the provided service exists
    if Service_Exists(argv[2]):
        
        Decrypt_Password_Record()        
        
        Password_Record_data = []
        with open('DateBase/Passwords_Register.json', 'r') as Passwords_Register:
            Password_Record_data = load(Passwords_Register)

        Updated_Password_Record_data = [record for record in Password_Record_data if record['Service'] != argv[2]]


        with open('DateBase/Passwords_Register.json', 'w') as Passwords_Register:
            dump(Updated_Password_Record_data,Passwords_Register, indent=4)
            
        Encrypt_Passwrds_Record()

        print('\nThe password has been deleted successfully\n')
    
    #If not allow the user to create new one    
    else:
        
        Create_New_Password_V2()


def Change_User_Password():   
    
    # Authenticate the user
    for i in range(3):

        OldPassword = getpass.getpass("\n\t>>Please do enter your old password   :  ")

        with open('DateBase/UserPassword.hash', 'r') as user_password_file:
            stored_password_hash = user_password_file.read()

        if stored_password_hash == hash(OldPassword):

            break

        else:
            print(Fore.RED+'\nUnvalid password !! '+Style.RESET_ALL)

        if i == 2:
            exit()
    
    # Retreive the new password
    NewPassword = getpass.getpass("\n\t>>Please do enter a new password   :  ")
    
    
    with open('DateBase/UserPassword.hash', 'w') as user_password_file:
        user_password_file.write(hash(NewPassword))

    with open('DateBase/UserPassword.hash', 'w') as user_password_file:
        user_password_file.write(hash(NewPassword))


    print("\nYour password has been updated successfully.\n")
    

def Display_Author():
    print(Fore.GREEN+r"""
                 _____                     _    _____   _   _                             _
                |  ___|__  _   _  __ _  __| |  | ____| | | | |      __   __ _  __ _  __ _| |_   _
                | |_ / _ \| | | |/ _` |/ _` |  |  _|   | | | '_ \ / _` |/ _` |/ _` |/ _` | | | | |
                |  _| (_) | |_| | (_| | (_| |  | |___  | | | |_) | (_| | (_| | (_| | (_| | | |_| |
                |_|  \___/ \__,_|\__,_|\__,_|  |_____| |_| |_.__/ \__,_|\__, |\__, |\__,_|_|\__, |
                                                                           |_|   |_|        |___/
    """+Style.RESET_ALL)


def Display_Help_Page():
    print("""
          
          
            Description :
                This program is a password manager, where the user can store and manage passwords for different services. It allows the user
            to create new passwords, update and delete existing ones, and view saved passwords for specific services.

            Usage:
            python Passwd_Manager.py [option] [length_of_password] [service_name]

            options:
                -i, --init: Initializes the password manager by creating a file to store the user's password and a file to store password records
            for different services.
            
                -n, --new: Creates a new password for the specified service.
                
                -u, --update: Updates an existing password for the specified service.
                
                -s, --show: Retrieves the password for the specified service.
                
                -d, --delete: Deletes the password of the specified service.
                
                --change_password : Allows the user to change its password of the PasswordManager program.
                
                -h, --help: Displays this help page.
                
            Usage example :
            
                    >>  py Passwd_Manager.py -init
                    
                    >>  py Passwd_Manager.py -n 120 gmail
                    
                    >>  py Passwd_Manager.py -s  gmail
            
            
            
    """)


if __name__ == '__main__':

    if argv[1] == '-i' or argv[1] == '--init':
        
        Display_Author()
        
        init()

    elif argv[1] == '-n' or argv[1] == '-u' or argv[1] == '--update' or argv[1] == '--new':

        if len(argv) == 4:
            if argv[1] == '-n' or argv[1] == '--new':
                
                Display_Author()

                authenticate_user()

                Create_New_Password()

            else:

                Display_Author()
                
                Update_password()
                pass

        else:
            print('Error : Unsufficient arguments !! ')

    elif argv[1] == '-s' or argv[1] == '--show':
        
        Display_Author()
        
        Show_Password()

    elif argv[1] == '-d' or argv[1] == '--delete':
        
        Delete_Password()        
        
    elif argv[1] == '--change_password':
        
        Change_User_Password()
        
    elif argv[1] == '-h' or argv[1] == '--help':
        
        Display_Help_Page()
        
    else:
        print('Error : Unvalid arguments !! ')
        print('Check the help page  : py Passwd_Manager.py -h ')
