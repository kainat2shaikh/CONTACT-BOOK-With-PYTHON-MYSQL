import mysql.connector
from prettytable import PrettyTable
import re

table=PrettyTable()
table.align='l'

conn=mysql.connector.connect(
    host='localhost',
    user='root',
    password='YOUR_MYSQL_PASSWORD',
    port='3306',
    database='ContactBook'
)

cursor=conn.cursor(buffered=True)

def add_contact():
    table.clear()

    print("~~~~~~~~ Adding A Contact In Your Contact Book ~~~~~~~~")        

    while True:
            print('[Press "Enter" Or Type "CANCEL" To Cancel]')
            name=input('Name: ').strip()
            if not name or name.lower()=='cancel':
                print("Cancelled : Name cannot be empty.")
                return
            else:
                break
                
                
    def valid_mobile():
            while True:
                print('[Press "Enter" Or Type "CANCEL" To Cancel]')

                enter_mob=input('Mobile Number (+91):  ').strip()
                if not enter_mob or enter_mob.lower()=='cancel':
                    print("Cancelled : Mobile Number cannot be empty.")
                    return None
                
                else:
                    mobile=enter_mob.replace(" ","").replace("-","")
                                
                    if mobile.startswith("+91") and len(mobile)==13:
                        mobile=mobile[3:]
                    elif mobile.startswith("91") and len(mobile)==12:
                        mobile=mobile[2:]
                    elif mobile.startswith("0") and len(mobile)==11:
                        mobile=mobile[1:]

                    if mobile.isdigit() and len(mobile)==10:
                        return f"(+91){mobile}"    
                    else:
                        print("Enter Valid 10-Digit Mobile Number.")
                        continue
                        

    def valid_email():
        while True:
            print('[Press "Enter" to Skip ]')
            email=input('Email : ').strip()
            if not email:
                return
            
            if re.match(r'^[\w\.-]{2,}@[\w\.-]{2,}\.\w{2,}$',email):
                return email
            else:
                print("Error ! Enter Valid Email. (Example : abc123@gmail.com)")
                continue

            
        
    mob=valid_mobile()
    if not mob:
        return
    
    cursor.execute('select * from contactbook where LOWER(name) = LOWER(%s) or mob=%s',(name,mob))
    dupl=cursor.fetchone()

    if dupl:
        print(f"{dupl[1]} ({dupl[2]}) already exists in Your Contact Book!")

        table.field_names=['ID','Name','Mobile Number','Email','City','Created At']
        cursor.execute('select * from contactbook where lower(name) = lower(%s) and mob=%s;',(name,mob))
        print("\n***** Have a look on your Contact Book *****\n")

        
        table.add_row([dupl[0],dupl[1],dupl[2],dupl[3] or "N/A",dupl[4] or "N/A",dupl[5]])
        print(table)
        return

    email=valid_email()        

    print('[Press "Enter" to Skip ]')
    city=input('City : ').strip() or None
    
    try:
        query='insert into contactbook (name,mob,email,city) values (%s,%s,%s,%s);'
        cursor.execute(query,(name,mob,email,city))
        conn.commit()
        print(f"Contact {name} Saved Successfully! ")
        
    except mysql.connector.IntegrityError as err1:
        print(f"{name} Contact Already Exists in Your Contact Book!")
        print("Error: ",err1)

    except mysql.connector.Error as err2:
        print("Database Error: ",err2)
            

def view_contacts():
    table.clear()
    table.field_names=['ID','Name','Mobile Number','Email','City','Created At']
    query='select * from contactbook order by name ;'
    cursor.execute(query)
    r1=cursor.fetchall()
    if not r1:
        print("\nYour Contact Book is Currently Empty!")
        return
    for i in r1:
        table.title= f"\nMy Contact Book (Total Contacts: {len(r1)})"

        table.add_row([i[0],i[1],i[2],i[3] or "-",i[4]or "N/A",i[5]])
    print(table)
    print("Total Contacts: ",len(r1))


    

def search_contact():
    table.clear()
    table.field_names=['ID','Name','Mobile Number','Email','City','Created At']
    
    user=input('Enter Contact Name or Number to Search: ').strip()

    try:
            if not user:
                print("Search Field Cannot Be Empty!! Type Proper Name Or Number.")
                return
            else:
                cursor.execute('select * from contactbook where LOWER(name) like LOWER(%s) or mob like %s',(f'%{user}%',f'%{user}%'))
                dupl=cursor.fetchall()
                if not dupl:
                    print(f" No '{user}' matching Contact Found in Your Contact Book!")
                    return

                table.title=(f"\nSearch results for '{user}' ({len(dupl)} found)")
                for i in dupl:
                    table.add_row([i[0],i[1],i[2],i[3] or 'N/A',i[4]or 'N/A',i[5]])
                print(table)

    except ValueError as err:
            print("Error: ",err)


def del_contact():
    
    
    def del_one_contact():
        table.clear()
        table.field_names=['ID','Name','Mobile Number','Email','City','Created At']

        user=input('Enter ID | Name | Mobile Number To Delete Contact: ').strip()
        if not user:
            print("Command Not Found!")
            return

        if user.isdigit():
            cursor.execute('select * from contactbook where id=%s or mob like %s',(int(user),f'%{user}%'))
        else:
            cursor.execute('select * from contactbook where lower(name) like lower(%s) or mob like %s',(f'%{user}%',f'%{user}%'))

        info=cursor.fetchall()
        if not info:
            print(f"No Matching Contact Found For '{user}' in Your Contact Book.")
            return
        
        table.title=f'\n Matching Results ({len(info)} Found)'
        for i in info:
            table.add_row([i[0],i[1],i[2],i[3] or '-',i[4] or 'N/A',i[5]])
        print(table)

        if (len(info))>1:
            print(f"\n Multiple Contacts Found For '{user}'! Enter Exact ID To Delete The Specific Contact. ")
            ex_id=input("Enter Exact ID (Or Press 'Enter' To Skip): ")or None
            if not ex_id:
                print("Skipped Deletion")
                return None
            try:
                exact_id=int(ex_id)
            except ValueError:
                print("Error: Enter Valid ID in Digits.")  
                return

            valid_id=[i for i in info if i[0] == exact_id]
            if not valid_id:
                print(f"Error: {exact_id} is Not in the Matching List Above!")
                return
            target_id=valid_id[0]
        else:
            target_id=info[0]
        
        confirmation=print(f'Deleting This Contact From Your Contact Book !')
        table.clear()
        table.title=f'\n Selected Matching Result ({len([target_id])} Found)'
        table.field_names=['ID','Name','Mobile Number','Email','City','Created At']
        table.add_row([target_id[0],target_id[1],target_id[2],target_id[3] or '-',target_id[4] or 'N/A',target_id[5]])
        print(table)

        confirmed=input(f'Are You Sure? Type "Yes" To Confirm, "No" To Cancel. ').strip()
        if confirmed.lower()==('Yes').lower():
            try:
                query='delete from contactbook where id = %s ;'
                cursor.execute(query,(target_id[0],))
                conn.commit()
                    
                print(f"Contact '{target_id[0]}' Deleted successfully!")

                table.clear()
                
                cursor.execute('select * from contactbook;')
                print("\n***** Have a look on your Contact Book *****\n")
                table.title='Your Contact Book'
                table.field_names=['ID','Name','Mobile Number','Email','City','Created At']
                for i in cursor.fetchall():
                        table.add_row([i[0],i[1],i[2],i[3] or '-',i[4] or 'N/A',i[5]])
                print(table)
            except mysql.connector.Error as err:
                print("Error: ",err)

        elif confirmed.lower()==('No').lower():
            print("Cancelled Deletion.")
            return
        else:
            print("Invalid Input! Type 'Yes' or 'No'")
            return

    def del_all_contacts():
        cursor.execute('select count(*) from contactbook;')
        count=cursor.fetchone()[0]        
        if count==0:
            print("\n Your Contact Book Is Already Empty!")
            return
        else:
            print("\nWARNING : You're About To Delete All Contacts From Your Contact Book.")   
            print("Do You Really Want To Delete All Contacts From Your Contact ?")
            table.clear()
                            
            cursor.execute('select * from contactbook;')
            
            print("\n***** Have a look on your Contact Book *****\n")
            table.title='Your Contact Book'
            table.field_names=['ID','Name','Mobile Number','Email','City','Created At']
            for i in cursor.fetchall():
                table.add_row([i[0],i[1],i[2],i[3] or '-',i[4] or 'N/A',i[5]])
            print(table)
                        
            all_confirmation=input("Type 'Confirm' To Confirm, 'Cancel' To Cancel.").strip().lower()
            if not all_confirmation:
                print("Empty Input Doesn't Work!!")
                return

            if all_confirmation=='confirm':
                try:
                    all_q='truncate table contactbook ;'
                    cursor.execute(all_q)
                    conn.commit()
                    print("All Contacts Deleted Successfully And ID Counter Reset to 1.")

                except mysql.connector.Error as err:
                    print("Error:",err)

            elif all_confirmation=='cancel':
                print("Deletion Cancel. Your Contacts are Safe.")
                return
            else:
                print("Invalid Input! Type Proper Option (Confirm/Cancel).")
                return


           

    while True:
        print("~~~~~~~ Delete Contact(s) Menu ~~~~~~~~")
        print("1. Delete A Specific Contact.")
        print("2. Delete All Contacts.")
        print("3. Back to Main Menu.")
        choice=input("Enter Your Choice: ").strip()
                    
        try:
            if not choice:
                print("Empty Command Found!! Choose any one Option For Deletion.")
                continue
                    
            ch=int(choice)
        except ValueError:
            print("Invalid Input! Enter Digits Only. ")
            continue

        if ch==1:
            del_one_contact()
        elif ch==2:
            del_all_contacts()
        elif ch==3:
            print("Returning Back To Main Menu..")
            return
        else:
            print("Invalid Choice! Please Choose Options Between (1 - 3).")

    
    
         
def upd_contact():
    table.clear()
    cursor.execute('select count(*) from contactbook;')
    count=cursor.fetchone()[0]        
    if count==0:
        print("\n Your Contact Book Is Currently Empty! Insert Contact Details To Update.")
        return
       
    enter_id=(input('Enter ID | Name | Mobile Number To Update Details: ')).strip()        
    if not enter_id:
        print("ID Not Found! Empty Input Doesn't Work.")
        return

    if enter_id.isdigit():
        cursor.execute('select * from contactbook where id=%s or mob like %s',(int(enter_id),f'%{enter_id}%'))
    else:
        cursor.execute('select * from contactbook where lower(name) like lower(%s) or mob like %s',(f'%{enter_id}%',f'%{enter_id}%'))
            
    upd_info=cursor.fetchall()
    if not upd_info:
        print(f"No Matching Contact Found For '{enter_id}' in Your Contact Book.")
        return
                
    table.clear()
    print (f"Updating ({enter_id}'s) Details Below .")
    table.field_names=['ID','Name','Mobile Number','Email','City','Created At']
    for i in upd_info:
        table.add_row([i[0],i[1],i[2],i[3] or '-',i[4] or 'N/A',i[5]])
    print(table)

    if (len(upd_info))>1:
        print(f"\n Multiple Contacts Found For '{enter_id}'! Enter Exact ID To Update The Specific Contact. ")
        check_id=input("Enter Exact ID (Or Press 'Enter' To Skip): ")or None
        if not check_id:
            print("Skipped Updation")
            return None
        try:
            exact_id=int(check_id)
        except ValueError:
            print("Error: Enter Valid ID in Digits.")  
            return
        valid_id=[i for i in upd_info if i[0] == exact_id]
        if not valid_id:
            print(f"Error: {exact_id} is Not in the Matching List Above!")
            return
        target_id = exact_id
    else:
        target_id = upd_info[0][0]

    while True:

        print("\nWhat do you want to Update: ")
        print("1. Name.\n2. Mobile Number.\n3. Email.\n4. City.\n5. Exit\n")
        choice=(input("Enter your choice:")).strip()
        if not choice:
            print("Command Not Found!")
            continue

        try:
            ch=int(choice)
        except ValueError:
            print("Invalid Input! Enter Digits only.")
            continue

        if ch==1:
            name=input('Enter New Name: ').strip()
            if not name:
                print("Sorry! Blank Names Cannot Be Updated !")
                continue

            if name:
                cursor.execute('update contactbook set name=%s where id = %s',(name,target_id))
                conn.commit()
                print(f" Successfully Updated {enter_id}'s Name Details.")

        elif ch==2:
            mob=input('Enter New Mobile Number(+91): ').strip()
            try:
                if not mob:
                    print("No Mobile Number Found! Cancelling Mobile Number Update.")
                    continue

                if mob:
                    mobile = mob.replace(" ","").replace("-","")
                                                            
                    if mobile.startswith("+91") and len(mobile)==13:
                        mobile= mobile[3:]
                                
                    elif mobile.startswith("91") and len(mobile)==12:
                        mobile=mobile[2:]
                                
                    elif mobile.startswith("0") and len(mobile)==11:
                        mobile= mobile[1:]

                    if mobile.isdigit() and len(mobile)==10:
                        mobile= f'(+91){mobile}' 
                        
                    else:
                        print("Enter Valid 10-Digit Mobile Number!")
                        continue
                                    
                cursor.execute('select id from contactbook where mob=%s and id != %s',(mobile, target_id),)
                if cursor.fetchall():
                    print(f'Error! {mobile} already belongs to another contact in your Contact Book.')
                    continue  
                else:
                    cursor.execute('update contactbook set mob=%s where id = %s',(mobile,target_id),)
                    conn.commit()
                    print(f" Successfully Updated {target_id}'s Mobile Number.")
            except ValueError as err:
                print("Error: ",err)                    

        elif ch==3:
            upd_email=input('Enter New Email: ').strip()
            if not upd_email:
                print("No Email Found! Skipping Email Update.")
                continue
            else:
                if re.match(r'^[\w\.-]{2,}@[\w\.-]{2,}\.\w{2,}$',upd_email):

                    cursor.execute('update contactbook set email=%s where id = %s',(upd_email,target_id))
                    conn.commit()
                    print(f" Successfully Updated ID {target_id}'s Email .")
                        
                else:
                    print("Error ! Enter Valid Email. (Example : abc123@gmail.com)")
                    continue
            

        elif ch==4:
            upd_city=input('Enter New City: ').strip()
            if not upd_city:
                print("No City Found! Skipping City Update.")
                continue

            if upd_city:

                cursor.execute('update contactbook set city=%s where id = %s',(upd_city,target_id))
                conn.commit()
                print(f" Successfully Updated ID {target_id}'s City .")

                
        elif ch==5:
            print("Updation Cancelled.")
            break

        else:
            print("Invalid Choice! Enter Valid Choice (between 1 - 5)")
            continue

        table.clear()
        table.title="------ UPDATED CONTACT BOOK ------"
        print("\n***** Have a look on your Contact Book *****\n")
        table.field_names=['ID','Name','Mobile Number','Email','City','Created At']
        cursor.execute('select * from contactbook;')
        tab=cursor.fetchall()
        for i in tab:
            table.add_row([i[0],i[1],i[2],i[3] or '-',i[4] or 'N/A',i[5]])
        print(table)
                