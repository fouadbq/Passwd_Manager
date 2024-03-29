import hashlib

from sys import argv, exit

from json import dump, load

from colorama import Fore, Style

from string import digits, ascii_letters, punctuation

from random import choice

from getpass import getpass

from re import search

from os import path, mkdir, urandom

from cryptography.hazmat.primitives.ciphers import Cipher

from cryptography.hazmat.primitives.ciphers.algorithms import AES

from cryptography.hazmat.primitives.ciphers.modes import CBC

from cryptography.hazmat.primitives.padding import PKCS7

from cryptography.hazmat.backends import default_backend


PassVault_Root = path.join(path.abspath(path.sep), 'PassVault')


def hash(password):
    # Generate a salt string
    salt = """Est un constructeur générique qui prend comme premier paramètre le nom de l'algorithme désiré (name) . Il existe pour permettre l'accès aux algorithmes listés ci-dessus ainsi qu'aux autres algorithmes que votre librairie OpenSSL peut offrir. Les constructeurs nommés sont beaucoup plus rapides que new() et doivent être privilégiés."""

    # Instanciating a new SHA-512
    sha512 = hashlib.sha512()

    sha512.update((password+salt).encode())

    return sha512.hexdigest()


def Encrypt_Passwrds_Record():

    # Read the key from the file
    with open(path.join(PassVault_Root, 'DateBase', '.key'), 'rb') as key_file:
        key = key_file.read()

    # Generate a random initialization vector
    init_vect = urandom(16)

    # Create the cipher object with CBC mode and PKCS7 padding
    cipher = Cipher(AES(key), CBC(init_vect), backend=default_backend())
    padder = PKCS7(128).padder()

    # Read the contents of the input file and pad it
    with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'rb') as Passwords_Register:
        padded_data = padder.update(
            Passwords_Register.read()) + padder.finalize()

    # Encrypt the padded data
    encryptor = cipher.encryptor()
    Encrypted_Passwords = encryptor.update(padded_data) + encryptor.finalize()

    # Write the encrypted data to a new file
    with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'wb') as Passwords_Register:
        Passwords_Register.write(init_vect + Encrypted_Passwords)


def Decrypt_Password_Record():
    # Read the key from the file
    with open(path.join(PassVault_Root, 'DateBase', '.key'), 'rb') as key_file:
        key = key_file.read()

    # Read the initialization vector and encrypted data from the input file
    with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'rb') as Passwords_Register:
        init_vect = Passwords_Register.read(16)
        Encrypted_Passwords = Passwords_Register.read()

    # Create the cipher object with CBC mode and PKCS7 padding
    cipher = Cipher(AES(key), CBC(init_vect), backend=default_backend())
    unpadder = PKCS7(128).unpadder()

    # Decrypt the encrypted data
    decryptor = cipher.decryptor()
    Decrypted_Passwords = decryptor.update(
        Encrypted_Passwords) + decryptor.finalize()

    # Unpad the decrypted data
    Passwords_List = unpadder.update(Decrypted_Passwords) + unpadder.finalize()

    # Write the decrypted data to a new file
    with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'wb') as Passwords_Register:
        Passwords_Register.write(Passwords_List)


# Initializeialize the necessary files to store the program data
def Initialize():

    if not path.exists(PassVault_Root):

        mkdir(PassVault_Root)
        mkdir(path.join(PassVault_Root, 'DateBase'))

        UserPassword = getpass(
            "\n\t>>Please do enter your authentification password   :  ")

        # Store the user authentication password
        with open(path.join(PassVault_Root, 'DateBase', 'UserPassword.hash'), 'w') as user_password_file:
            user_password_file.write(hash(UserPassword))

        # Create  a passwords register file
        with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'w') as password_register:
            dump([], password_register, indent=4)

        # Generate a 32 bytes <=> 256-bit enc key && storing it in a hidden file
        with open(path.join(PassVault_Root, 'DateBase', '.key'), 'wb') as key_file:
            key_file.write(urandom(32))

        Encrypt_Passwrds_Record()

        print("\nInitialization is done successfully.\n")
    else:
        print('The initialization phaze already took place, do you want to update the whole files ? ')
        print('Note : this would lead to the deletion of your passwords')

        option = input('Update < u > | Overwrite < w > | Cancel < c > :\t')

        if option == 'u' or option == 'w':

            NewUserPassword = getpass(
                "\n\t>>Please do enter your new authentification password   :  ")

            with open(path.join(PassVault_Root, 'DateBase', 'UserPassword.hash'), 'w') as user__password__file:
                user__password__file.write(hash(NewUserPassword))

            if option == 'u':

                Decrypt_Password_Record()

                with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'r') as Passwords_List_File:
                    Passwords_List = load(Passwords_List_File)

                # Regenerate a new 32 bytes <=> 256-bit enc key && storing it in a hidden file
                with open(path.join(PassVault_Root, 'DateBase', '.key'), 'wb') as key_file:
                    key_file.write(urandom(32))

                with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'w') as Passwords_Register:
                    dump(Passwords_List, Passwords_Register, indent=4)

                Encrypt_Passwrds_Record()

            elif option == 'w':

                with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'w') as Passwords__Register:
                    dump([], Passwords__Register, indent=4)

                Encrypt_Passwrds_Record()

                # Regenerate a new 32 bytes <=> 256-bit enc key && storing it in a hidden file
                with open(path.join(PassVault_Root, 'DateBase', '.key'), 'wb') as key_file:
                    key_file.write(urandom(32))

        elif option == 'c':
            exit()
        else:
            print('Unvalid input !')


def authenticate_user():
    for i in range(3):

        Password = getpass("\n\t>>Please do enter your password   :  ")

        with open(path.join(PassVault_Root, 'DateBase', 'UserPassword.hash'), 'r') as user_password_file:
            stored_password_hash = user_password_file.read()

        if stored_password_hash == hash(Password):

            break

        else:
            print(Fore.RED+'\nUnvalid password !! '+Style.RESET_ALL)

        if i == 2:
            exit()


def generate_new_password(len):

    # Create a dictionay
    Dictionary = ascii_letters + digits + \
        punctuation.replace('"', '').replace("'", '').replace('\\', '')

    Decrypt_Password_Record()

    passwords_list = []
    with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'r') as register_file:
        passwords_list = load(register_file)

    Encrypt_Passwrds_Record()

    # Check if the password already exists in the password register => Password duplication is not allowed
    while True:
        New_Password = ''.join(choice(Dictionary) for i in range(len))

        if not any(New_Password == psswd_record['Password'] for psswd_record in passwords_list):
            break

    return New_Password


def Service_Exists(service):

    Decrypt_Password_Record()

    with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'r') as register_file:
        passwords_list = load(register_file)

    Encrypt_Passwrds_Record()

    return any(service == psswd_record['Service'] for psswd_record in passwords_list)


# Retreive the password from the password register
def Get_Password(service):

    Decrypt_Password_Record()

    with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'r') as register_file:
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

        with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'r') as Passwords_Register:
            Password_Record_data = load(Passwords_Register)

        # Add the new password record to the register
        Password_Record_data.append(Password_Record)

        with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'w') as Passwords_Register:

            dump(Password_Record_data, Passwords_Register, indent=4)

        Encrypt_Passwrds_Record()

        print('\nHere is the genarated password for ' +
              argv[3]+'  is : \n\n\t'+Fore.RED+New_Password+Style.RESET_ALL+'\n')

    # In case a password already exists for the service
    else:
        print('You already do have a password for this service !! ')
        option = input('Press :   <'+Fore.YELLOW+' s '+Style.RESET_ALL +
                       '> To see the password  | <'+Fore.YELLOW+' c '+Style.RESET_ALL+'>  To cancel   ')

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

        choice = input('\nPress :   <'+Fore.YELLOW+' y '+Style.RESET_ALL +
                       '> to confirm password update  | <'+Fore.YELLOW+' n '+Style.RESET_ALL+'>  to cancel   ')

        if choice == 'y':

            New_Password = generate_new_password(int(argv[2]))

            Updated_Password_Record = {
                'Service': argv[3],
                'Password': New_Password
            }

            Decrypt_Password_Record()

            Password_Record_data = []
            with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'r') as Passwords_Register:
                Password_Record_data = load(Passwords_Register)

            # Fister the password register to eliminate the old password
            Updated_Password_Record_data = [
                record for record in Password_Record_data if record['Service'] != argv[3]]

            # Add the new password record to the file
            Updated_Password_Record_data.append(Updated_Password_Record)

            with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'w') as Passwords_Register:
                dump(Updated_Password_Record_data,
                     Passwords_Register, indent=4)

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
        option = input('Press :   <'+Fore.YELLOW+' y '+Style.RESET_ALL +
                       '> to create a password  | <'+Fore.YELLOW+' n '+Style.RESET_ALL+'>  to cancel   ')

        if option == 'y':

            Create_New_Password()

        elif option == 'n':

            exit()

        else:

            print(Fore.RED+'\nError : Unvalid input'+Style.RESET_ALL)


def Create_New_Password_V2():

    print('\n\tYou do not have a password for the spesified service !! \n')
    option = input('Press :   <'+Fore.YELLOW+' y '+Style.RESET_ALL +
                   '> to create a password  | <'+Fore.YELLOW+' n '+Style.RESET_ALL+'>  to cancel   ')

    if option == 'y':

        len = int(input('Enter the length of the password  :  '))

        New_Password = generate_new_password(len)

        Password_Record = {
            'Service': argv[2],
            'Password': New_Password
        }

        Decrypt_Password_Record()

        Password_Record_data = []
        with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'r') as Passwords_Register:

            Password_Record_data = load(Passwords_Register)

        Password_Record_data.append(Password_Record)

        with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'w') as Passwords_Register:

            dump(Password_Record_data, Passwords_Register, indent=4)

        Encrypt_Passwrds_Record()

        print('\nHere is the genarated password for ' +
              argv[2]+'  is : \n\t'+Fore.RED+New_Password+Style.RESET_ALL+'\n')

    elif option == 'n':

        exit()

    else:
        print(Fore.RED+'\nError : Unvalid input'+Style.RESET_ALL)


def Show_Password():

    if Service_Exists(argv[2]):

        print('\nHere is your password for ' +
              argv[2]+' : \n\n\t'+Fore.RED + Get_Password(argv[2]) + Style.RESET_ALL+'\n')

    else:
        Create_New_Password_V2()


def Delete_Password():

    # Check fisrt if a password for the provided service exists
    if Service_Exists(argv[2]):

        Decrypt_Password_Record()

        Password_Record_data = []
        with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'r') as Passwords_Register:
            Password_Record_data = load(Passwords_Register)

        Updated_Password_Record_data = [
            record for record in Password_Record_data if record['Service'] != argv[2]]

        with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'w') as Passwords_Register:
            dump(Updated_Password_Record_data, Passwords_Register, indent=4)

        Encrypt_Passwrds_Record()

        print('\nThe password has been deleted successfully\n')

    # If not allow the user to create new one
    else:

        Create_New_Password_V2()


def Change_User_Password():

    # Authenticate the user
    for i in range(3):

        OldPassword = getpass("\n\t>>Please do enter your old password   :  ")

        with open(path.join(PassVault_Root, 'DateBase', 'UserPassword.hash'), 'r') as user_password_file:
            stored_password_hash = user_password_file.read()

        if stored_password_hash == hash(OldPassword):

            break

        else:
            print(Fore.RED+'\nUnvalid password !! '+Style.RESET_ALL)

        if i == 2:
            exit()

    # Retreive the new password
    NewPassword = getpass("\n\t>>Please do enter a new password   :  ")

    with open(path.join(PassVault_Root, 'DateBase', 'UserPassword.hash'), 'w') as user_password_file:
        user_password_file.write(hash(NewPassword))

    with open(path.join(PassVault_Root, 'DateBase', 'UserPassword.hash'), 'w') as user_password_file:
        user_password_file.write(hash(NewPassword))

    print("\nYour password has been updated successfully.\n")


def Display_Author():
    print(Fore.GREEN+'\n\n\t    ____                 _    __            ____ ')
    print('\t   / __ \____ __________| |  / /___ ___  __/ / /_')
    print('\t  / /_/ / __ `/ ___/ ___/ | / / __ `/ / / / / __/')
    print('\t / ____/ /_/ (__  |__  )| |/ / /_/ / /_/ / / /_')
    print('\t/_/    \__,_/____/____/ |___/\__,_/\__,_/_/\__/')

    print(Fore.BLUE+'\n\t\t Made by Fouad El-Baqqaly\n\n'+Style.RESET_ALL)


def Display_Help_Page():
    print("""
          
          
            Description :
                This program is a password manager, where the user can store and manage passwords for different services. It allows the user
            to create new passwords, update and delete existing ones, and view saved passwords for specific services.

            Usage:
            python Passwd_Manager.py [option] [length_of_password] [service_name]

            options:
                -i, --init: Initializeializes the password manager by creating a file to store the user's password and a file to store password records
            for different services.
            
                -n, --new          : Creates a new password for the specified service.
                
                -u, --update       : Updates an existing password for the specified service.
                
                -s, --show         : Retrieves the password for the specified service.
                
                -d, --delete       : Deletes the password of the specified service.
                
                -a, --add          : Allows adding a user customized password.
                
                --change_password  : Allows the user to change its password of the PasswordManager program.
                
                -h, --help         : Displays this help page.
                
            Usage example :
            
                    >>  py Passwd_Manager.py -Init
                    
                    >>  py Passwd_Manager.py -n 120 gmail
                    
                    >>  py Passwd_Manager.py -s  gmail
            
            
            
    """)


def Display_Services():

    Decrypt_Password_Record()

    with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'r') as register_file:
        passwords_list = list(load(register_file))

    Encrypt_Passwrds_Record()

    print('\n\n>> Here is the list of services in which you are subscribed :\n')

    for password_record in passwords_list:

        print('\n\t-->  ', Fore.GREEN, password_record['Service'], Fore.WHITE, '\t[',
              Fore.YELLOW, passwords_list.index(password_record)+1, Fore.WHITE, ' ]\n')

    try:
        option = int(input(
            'To select a service, enter the corresponding number. Press Enter to skip : '))
    except Exception:
        print('\n\tError : Unvalid input ! ')

    if option > 0 and option <= len(passwords_list):

        print('\t>>  Your password is :  ')
        print('\t\t', Fore.RED,
              passwords_list[option-1]['Password'], Style.RESET_ALL)

    elif option == '':
        pass

    else:
        print('\n\tError : Unvalid input ! ')


def Add_User_Customized_Password(password):

    strength = 100

    print('Your password < {} >  is : '.format(password))

    if len(password) <= 50:
        print('\t\t-> is not long enough')
        strength -= 10

    if not bool(search(r'[A-Z]', password)):
        print('\t-> does not contain any capital letters')
        strength -= 10

    if not bool(search(r'\d', password)):
        print('\t-> does not contain any numbers')
        strength -= 40

    if not bool(search(r'[^\w\s]', password)):
        print('\t-> does not contain any symbols')
        strength -= 40

    print('\nYour password strength is about {}/100\n'.format(strength))

    option = input(
        'Are you sure that you want to add this password to your PassVault  ?  yes : < y > | no : < n >\t')

    if option == 'y':
        service = input('Please enter the service name  :\t')

        Password_Record = {
            'Service': service,
            'Password': password
        }

        Password_Record_data = []

        Decrypt_Password_Record()

        with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'r') as Passwords_Register:
            Password_Record_data = load(Passwords_Register)

        # Add the new password record to the register
        Password_Record_data.append(Password_Record)

        with open(path.join(PassVault_Root, 'DateBase', 'Passwords_Register.json'), 'w') as Passwords_Register:

            dump(Password_Record_data, Passwords_Register, indent=4)

        Encrypt_Passwrds_Record()

        print(f'Your password for the {service}  service is  {password}\n\n')

    exit()


if __name__ == '__main__':

    Display_Author()

    # authenticate_user()

    if argv[1] == '-i' or argv[1] == '--init':

        Initialize()

    elif argv[1] == '-n' or argv[1] == '-u' or argv[1] == '--update' or argv[1] == '--new':

        if len(argv) == 4:
            if argv[1] == '-n' or argv[1] == '--new':

                Create_New_Password()

            else:

                Update_password()
                pass

        else:
            print('Error : Unsufficient arguments !! ')

    elif argv[1] == '-s' or argv[1] == '--show':

        Show_Password()

    elif argv[1] == '-d' or argv[1] == '--delete':

        Delete_Password()

    elif argv[1] == '-ss' or argv[1] == '--show_services':

        Display_Services()

    elif argv[1] == '-a' or argv[1] == '--add':

        Add_User_Customized_Password(argv[2])

    elif argv[1] == '--change_password':

        Change_User_Password()

    elif argv[1] == '-h' or argv[1] == '--help':

        Display_Help_Page()

    else:
        print('Error : Unvalid arguments !! ')
        print('Check the help page  : py Passwd_Manager.py -h ')
