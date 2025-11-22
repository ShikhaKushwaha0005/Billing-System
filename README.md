# Inventory Management & Customer Billing System<br>

•••PROJECT TITLE••• <br>
Inventory Management & Customer Billing System
<br>


•••OVERVIEW OF THE PROJECT•••<br>
This software project is developed to automate the functionalities of a CUSTOMER BILLING SYSTEM.
Customer Billing System Project is a basic console application created to show the actual use of the Python programming language and its capabilities as well as to develop an application that can be used to charge customers in any department store, shop, cafe, etc. We may use this program to keep track of our frequent customers' billing information such as item number, item name, quantity taken, total amount, and so on. We may also add and update details at any moment if we have a new client.<br>


•••PROGRAM CODE•••<br>
import mysql.connector
import csv

def get_db_connection():
    return mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="tiger", 
        database="inventory_db"
    )

def stock():
    def displayall():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stock")
            rows = cursor.fetchall()
            print("Item No     Item Name     Quantity     Unit Price")
            for row in rows:
                print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        input("Press Any Key to continue ")

    def addstock():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            while True:
                itemno = int(input("Enter item number: "))
                itemname = input("Enter item name: ")
                quantity = int(input("Enter quantity: "))
                unitprice = float(input("Enter unit price: "))
                cursor.execute("INSERT INTO stock (item_no, item_name, quantity, unit_price) VALUES (%s, %s, %s, %s)", 
                               (itemno, itemname, quantity, unitprice))
                conn.commit()
                chadd = input("Do you want to add more? (y/Y/n/N): ")
                if chadd in ['n', 'N']:
                    break
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        input("Press Any Key to continue ")

    def delstock():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            ino = input("Enter item number to search and delete: ")
            cursor.execute("SELECT * FROM stock WHERE item_no = %s", (ino,))
            row = cursor.fetchone()
            if row:
                print(f"Item Found: {row}")
                ch3 = input("Do you want to delete this item? (y/Y/n/N): ")
                if ch3 in ['y', 'Y']:
                    cursor.execute("DELETE FROM stock WHERE item_no = %s", (ino,))
                    conn.commit()
                    print("Deleted.")
                else:
                    print("Item not deleted.")
            else:
                print("Item not found.")
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        input("Press Any Key to continue ")

    def modstock():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            ino = input("Enter item number to search and modify: ")
            cursor.execute("SELECT * FROM stock WHERE item_no = %s", (ino,))
            row = cursor.fetchone()
            if row:
                print(f"Item Found - {row}")
                ch3 = input("Do you want to modify this item? (y/Y/n/N): ")
                if ch3 in ['y', 'Y']:
                    ch31 = input("Change name? (y/Y/n/N): ")
                    if ch31 in ['y', 'Y']:
                        new_name = input("New item name: ")
                        cursor.execute("UPDATE stock SET item_name = %s WHERE item_no = %s", (new_name, ino))
                    ch32 = input("Change quantity? (y/Y/n/N): ")
                    if ch32 in ['y', 'Y']:
                        new_qty = int(input("New quantity: "))
                        cursor.execute("UPDATE stock SET quantity = %s WHERE item_no = %s", (new_qty, ino))
                    ch33 = input("Change unit price? (y/Y/n/N): ")
                    if ch33 in ['y', 'Y']:
                        new_price = float(input("New unit price: "))
                        cursor.execute("UPDATE stock SET unit_price = %s WHERE item_no = %s", (new_price, ino))
                    conn.commit()
                    print("Item updated.")
            else:
                print("Item not found.")
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        input("Press Any Key to continue ")

    def display():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            ino = input("Enter item number to search and display: ")
            cursor.execute("SELECT * FROM stock WHERE item_no = %s", (ino,))
            row = cursor.fetchone()
            if row:
                print(f"Item Found - Item No: {row[0]}, Name: {row[1]}, Quantity: {row[2]}, Unit Price: {row[3]}")
            else:
                print("Item not found.")
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        input("Press Any Key to continue ")

    while True:
        print("\n1. Display All Stock Details\n2. Add New Stock\n3. Delete Stock\n4. Modify Stock\n5. Display Single Item\n6. Return to Main Menu")
        try:
            ch1 = int(input("Enter choice: "))
            if ch1 == 1:
                displayall()
            elif ch1 == 2:
                addstock()
            elif ch1 == 3:
                delstock()
            elif ch1 == 4:
                modstock()
            elif ch1 == 5:
                display()
            elif ch1 == 6:
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Enter a number between 1 and 6.")

def billing():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock")
        stock_list = cursor.fetchall()

        with open("bill.csv", "w", newline='') as bill_file:
            bill_writer = csv.writer(bill_file, delimiter=',')
            cname = input("Enter customer name: ")
            bill_items = []
            while True:
                ino = int(input("Enter item number: "))
                item_found = False
                for item in stock_list:
                    if item[0] == ino:
                        item_name = item[1]
                        stock_qty = int(item[2])
                        unit_price = float(item[3])
                        item_found = True
                        break

                if not item_found:
                    print("Item not found.")
                    continue

                qty = int(input(f"Enter quantity (Available: {stock_qty}): "))
                if qty > stock_qty:
                    print("Error: Insufficient stock.")
                    continue

                total_price = qty * unit_price
                bill_items.append([cname, ino, item_name, qty, unit_price, total_price])

                cursor.execute("UPDATE stock SET quantity = %s WHERE item_no = %s", (stock_qty - qty, ino))
                conn.commit()

                more = input("Do you want to purchase more? (y/Y/n/N): ")
                if more in ['n', 'N']:
                    break

            bill_writer.writerows(bill_items)

        print("\n--- BILL ---")
        print(f"Customer: {cname}")
        grand_total = 0
        for item in bill_items:
            print(f"{item[1]} {item[2]} {item[3]} {item[4]} {item[5]}")
            grand_total += item[5]
        print(f"Grand Total: {grand_total}")

        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

while True:
    print("\n1. Stock Maintenance\n2. Customer Billing\n3. Exit")
    try:
        choice = int(input("Enter choice: "))
        if choice == 1:
            stock()
        elif choice == 2:
            billing()
        elif choice == 3:
            break
        else:
            print("Invalid choice. Try again.")
    except ValueError:
        print("Invalid input. Enter a number between 1 and 3.")


•••FEATURES•••<br>
The objective of the software project is to develop a computerized MIS and to automate the functions of a CUSTOMER BILLING SYSTEM. This software project is also aimed to enhance the current record keeping system, which will help managers to retrieve the up-to-date information at right time in right shape.<br>

Major features:<br>
1. Stock maintaing<br>
        Sub-Featues:<br>
           1. Display all stock details<br>
           2.Add new stock<br>
           3. Delete Stock<br>
           4. Modify Stock<br>
           5. Display Single Item<br>
           6. Return to Main Menu<br>
2. Customer billing <br>
3. Exit
         
Understanding MySQL–Python integration <br>
Implementing CRUD operations <br>
File handling using CSV module <br>
Error handling and modular programming <br>
Real-world problem-solving through coding <br>
  

•••TECNOLOGIES/TOOLS USED••• <br>
1. Hardware used: <br>
   •	PC with Intel Core i5-2400S processor having 4.00 GB RAM, <br>
   •	32/64-bit Operating System, <br>
   •	SVGA and other required devices.  <br>

2. Software used: <br>
   • Microsoft Windows 10 Pro as Operating System.  <br>
   • Python 3.7.2 as Front-end Development environment.  <br>
   • MS-Word 2019 for documentation <br>
   • CSV- It is used to handle csv file.  <br>
         Module contains functions like :- <br>
         •	reader() <br>
         •	writer() <br>
         •	writerow() <br>
         •	writerows() <br>
   


•••STEPS TO INSTALL & RUN THE PROJECT••• <br>
Use python, github, MySQL to run the project. <br>
The project has 101 to 150 item in stock enter any numbee between these to run all and any part of the billing system. <br>


•••INSTRUCTIONS FOR TESTING••• <br>
1.While running the program keep in mind that thr inventory only has items listed from 101 to 150.
2.To add any item choose any number apart from 101-150. <br>


•••SCREENSHOTS••• <br>

![WhatsApp Image 2025-11-22 at 21 49 41_bf115bdf](https://github.com/user-attachments/assets/1f159977-9a98-44b4-8a4b-a8e852772740)

![WhatsApp Image 2025-11-22 at 21 58 29_d428e056](https://github.com/user-attachments/assets/d2177c69-3bc4-4668-b12c-79491d462211)

![WhatsApp Image 2025-11-22 at 21 59 56_d0043cb0](https://github.com/user-attachments/assets/619ce86b-6e81-4394-ba7a-214d7c130419)

![WhatsApp Image 2025-11-22 at 22 01 24_6c6cce71](https://github.com/user-attachments/assets/6c3f3b3b-fa6f-45cd-8573-1fc66525b326)

![WhatsApp Image 2025-11-22 at 22 03 52_e0764cb2](https://github.com/user-attachments/assets/4075e30c-a478-4aed-8079-9cf7e002b378)

![WhatsApp Image 2025-11-22 at 22 05 38_38a9a6e5](https://github.com/user-attachments/assets/531a9575-8fde-4868-bc0a-c69723046ce4)

![WhatsApp Image 2025-11-22 at 22 06 16_9276032e](https://github.com/user-attachments/assets/3652cd25-a2b3-4ba7-9e78-47f3852f7ad0)

![WhatsApp Image 2025-11-22 at 22 10 20_fc650c90](https://github.com/user-attachments/assets/ab4b804b-d4dc-45aa-8a15-00ad420c542d)

<img width="979" height="370" alt="image" src="https://github.com/user-attachments/assets/42af5071-7fb3-41ba-8c68-1a8f7653e221" />

<img width="979" height="406" alt="image" src="https://github.com/user-attachments/assets/1f5ff0db-412f-4905-8037-fa584f6ee6a5" />

<img width="518" height="415" alt="image" src="https://github.com/user-attachments/assets/5e333a81-1f46-4dbf-9384-df0da71cd372" />

![WhatsApp Image 2025-11-22 at 22 14 09_29b48df8](https://github.com/user-attachments/assets/c73e0108-d930-4af5-820f-d7eaa7248b77)


