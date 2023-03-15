&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Capture d'écran 2023-03-04 153033](https://user-images.githubusercontent.com/120426068/222917504-48e3e6be-a161-4be9-b57e-c1f4ab7ca587.png)

# Passwd-Manager

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This program is a password manager, where the user can store and manage passwords for different services. It allows the user to generate new passwords, change and delete current ones, and examine stored passwords for specific services, all while keeping passwords private and safe.<br/><br/>

## Run Locally

Clone the project

```bash
 https://github.com/fouadbq/Passwd_Manager.git
```

Install the required packages on your local machine

```bash
pip install -r requirements.txt
```

Start the password manager

```bash
py Passwd_Manager.py --init
```

## Usage

&nbsp;&nbsp;&nbsp;To initialize the Password_Manager, run the script with the command :
```bash
py Passwd_Manager.py --init
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;>This will allow the user to set their password for the passwords manager program, then creates the necessary files where to store the passwords.

&nbsp;&nbsp;&nbsp;To create a new password for a specific service, run the script with the command 
```bash
py Passwd_Manager.py --new < password length >  < service >
``` 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;>This will generate a random password of the given length and store it to the passwords record.
        
&nbsp;&nbsp;&nbsp;To update an existing password, run the script with the command 
```bash
py Passwd_Manager.py --update < password length >  < service >
``` 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;>This will generate a new random password of the given length and replace the old password with the new one.

&nbsp;&nbsp;&nbsp;To see an existing password, run the script with the command 
```bash
py Passwd_Manager.py --show   < service >
``` 

&nbsp;&nbsp;&nbsp;To delete an existing password, run the script with the command 
```bash
py Passwd_Manager.py --delete   < service >
``` 

&nbsp;&nbsp;&nbsp;To display the existing accounts/services, run the script with the command 
```bash
py Passwd_Manager.py --ss   
``` 

&nbsp;&nbsp;&nbsp;To change the password of the password manager, run the script with the command 
```bash
py Passwd_Manager.py --change_password  
``` 

&nbsp;&nbsp;&nbsp;To show the help page of the password manager, run the script with the command 
```bash
py Passwd_Manager.py --help  
``` 
<br/><br/>
## Feedback

If you have any feedback, please do reach out to me at fouadelbaqqaly@gmail.com


