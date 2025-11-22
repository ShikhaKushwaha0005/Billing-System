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


