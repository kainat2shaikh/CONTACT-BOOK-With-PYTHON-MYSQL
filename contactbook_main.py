
import ContactBook

while True:
    print("\n---------- MENU ------------\n")
    print("1. Add a Contact in Your Contact Book.")
    print("2. View Your Contact Book.")
    print("3. Search for a Contact in Your Contact Book.")
    print("4. Delete a Contact from Your Contact Book.")
    print("5. Update a Contact Details in Your Contact Book.") 
    print("6. Exit")
    choice=input("Enter Your Choice:  ").strip()
            
    try:
        if not choice:
            print("Empty Command Entered!!")
            continue
                
        ch=int(choice)
    except ValueError:
        print("Invalid Input! Enter Digits Only..")
        continue

    if ch==1:
        ContactBook.add_contact()
    elif ch==2:
        ContactBook.view_contacts()
    elif ch==3:
        ContactBook.search_contact()
    elif ch==4:
        ContactBook.del_contact()
    elif ch==5:
        ContactBook.upd_contact()
    elif ch==6:
        print('Exiting...')
        break
    else:
        print("Invalid Option! Choose Options between (1-5).")    

ContactBook.cursor.close()
ContactBook.conn.close()
