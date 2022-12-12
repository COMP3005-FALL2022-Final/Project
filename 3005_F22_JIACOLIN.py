import mysql.connector

totalOrder = 0
shoppingCartISBN = []
shoppingCartPrice = []
shoppingCartStockPrice = []
shoppingCartInStock = []
shoppingCartNum = []
month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
currMonth = 11 #December
currYear = 2022
currAcc = "qwe" #TODO None


def userMenu():
    print("\nIt is %d %s" % (currYear, month[currMonth]))
    print("MENU -- Please input number 1 or 5 to select")
    print("1. Find book by book name")
    print("2. Find book by author")
    print("3. Find book by ISBN")
    print("4. Find book by genre")
    print("5. view cart")
    print("6. Check out")
    print("7. Go back menu")

def ownerMenu():
    print("\nIt is %d %s" % (currYear, month[currMonth]))
    print("MENU -- Please input number 1 or 8 to select")
    print("1. add book ")
    print("2. remove book")
    print("3. add publisher info")
    print("4. sales vs. expenditures")
    print("5. sales per genres")
    print("6. sales per author")
    print("7. sales report for last month")
    print("8. Go back menu")

def accMenu():
    print("\nIt is %d %s" % (currYear, month[currMonth]))
    print("MENU -- Please input number 1 or 3 to select")
    print("1. Sign up")
    print("2. Login")
    print("3. Go back menu")

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "password", 
)

mycursor = db.cursor()

#TODO: remove drop database when handing in
mycursor.execute("DROP DATABASE IF EXISTS Bookstore")

#Create database
mycursor.execute("CREATE DATABASE IF NOT EXISTS Bookstore")
mycursor.execute("use Bookstore")


#Create table
mycursor.execute("CREATE TABLE IF NOT EXISTS Book (Bookname VARCHAR(30) NOT NULL UNIQUE, ISBN VARCHAR(13) PRIMARY KEY, Genre VARCHAR(13), Price float(2) NOT NULL, Author VARCHAR(30), PageNumber INT, InStock INT NOT NULL, StockPrice float(2) NOT NULL)")
mycursor.execute("CREATE TABLE IF NOT EXISTS Orders (OrderNumber INT PRIMARY KEY, BillingInfo VARCHAR(30), ShippingInfo VARCHAR(30), TotalPrice float(2) NOT NULL, Date CHAR(7))")
mycursor.execute("CREATE TABLE IF NOT EXISTS Account (ID VARCHAR(30) PRIMARY KEY, BillingInfo VARCHAR(30), ShippingInfo VARCHAR(30))")
mycursor.execute("CREATE TABLE IF NOT EXISTS Publisher (Name VARCHAR(30) PRIMARY KEY, Address VARCHAR(30), Email VARCHAR(30), Phone VARCHAR(10) NOT NULL, BankAccount VARCHAR(10))")
mycursor.execute("CREATE TABLE IF NOT EXISTS TrackSystem (TrackingNum VARCHAR(30) PRIMARY KEY, Position VARCHAR(30) NOT NULL, Status VARCHAR(20) NOT NULL)")

#relation and PK will be set before ending table
mycursor.execute("CREATE TABLE IF NOT EXISTS GetInfo (ISBN VARCHAR(13), OrderNumber INT, Number INT NOT NULL, TotalPrice float(2) NOT NULL, CONSTRAINT PRIMARY KEY (ISBN,OrderNumber))")
#TODO: Percentage need to change in table
mycursor.execute("CREATE TABLE IF NOT EXISTS CalculateIncome (Name VARCHAR(30), ISBN VARCHAR(13), Percentage float(2) NOT NULL, CONSTRAINT PRIMARY KEY (Name,ISBN))")
mycursor.execute("CREATE TABLE IF NOT EXISTS PlaceOrder (ID VARCHAR(30), OrderNumber INT, CONSTRAINT PRIMARY KEY (ID,OrderNumber))")
mycursor.execute("CREATE TABLE IF NOT EXISTS Track (OrderNumber INT, TrackingNum VARCHAR(30), CONSTRAINT PRIMARY KEY (OrderNumber,TrackingNum))")
mycursor.execute("CREATE TABLE IF NOT EXISTS SalesRecord(ISBN VARCHAR(13) PRIMARY KEY, Date CHAR(7), Income float(2) NOT NULL, Expense float(2) NOT NULL)")

#adding foreign key
mycursor.execute("ALTER TABLE GetInfo ADD FOREIGN KEY (ISBN) REFERENCES Book(ISBN)")
mycursor.execute("ALTER TABLE GetInfo ADD FOREIGN KEY (OrderNumber) REFERENCES Orders(OrderNumber)")
mycursor.execute("ALTER TABLE CalculateIncome ADD FOREIGN KEY (ISBN) REFERENCES Book(ISBN)")
mycursor.execute("ALTER TABLE CalculateIncome ADD FOREIGN KEY (Name) REFERENCES Publisher(Name)")
mycursor.execute("ALTER TABLE PlaceOrder ADD FOREIGN KEY (ID) REFERENCES Account(ID)")
mycursor.execute("ALTER TABLE PlaceOrder ADD FOREIGN KEY (OrderNumber) REFERENCES Orders(OrderNumber)")
mycursor.execute("ALTER TABLE Track ADD FOREIGN KEY (TrackingNum) REFERENCES TrackSystem(TrackingNum)")
mycursor.execute("ALTER TABLE Track ADD FOREIGN KEY (OrderNumber) REFERENCES Orders(OrderNumber)")


#TODO: debug=========================================================================================

mycursor.execute("INSERT INTO Publisher(Name, Address, Email, Phone, BankAccount) VALUES ('Colin','carleton university','Colin@carleton.ca', '6119998888', '778899')")
mycursor.execute("INSERT INTO Publisher(Name, Address, Email, Phone, BankAccount) VALUES ('Jia','carleton university','Jia@carleton.ca', '6119991234', '112233')")

mycursor.execute("INSERT INTO Book (Bookname, ISBN, Genre, Price, Author, PageNumber, InStock, StockPrice) VALUES ('Book of University','1234','education', 50.99 , 'Jia', 155, 20, 19.99)")
mycursor.execute("INSERT INTO CalculateIncome(Name, ISBN, Percentage) VALUES ('Colin','1234', '0.2')")

mycursor.execute("INSERT INTO Book (Bookname, ISBN, Genre, Price, Author, PageNumber, InStock, StockPrice) VALUES ('Book of Carleton','2345','education', 50.99 , 'Colin', 120, 30, 19.99)")
mycursor.execute("INSERT INTO CalculateIncome(Name, ISBN, Percentage) VALUES ('Colin','2345', '0.1')")

mycursor.execute("INSERT INTO Book (Bookname, ISBN, Genre, Price, Author, PageNumber, InStock, StockPrice) VALUES ('COMP 3005','4789','education', 100.00 , 'Colin', 120, 30, 90.0)")
mycursor.execute("INSERT INTO CalculateIncome(Name, ISBN, Percentage) VALUES ('Jia','4789', '0.1')")

mycursor.execute("INSERT INTO SalesRecord(ISBN, Date, Income, Expense) VALUES ('4789','2022-11', 868.90, 400.00)")
mycursor.execute("INSERT INTO SalesRecord(ISBN, Date, Income, Expense) VALUES ('1234','2022-11', 500.90, 400.90)")
mycursor.execute("INSERT INTO SalesRecord(ISBN, Date, Income, Expense) VALUES ('2345','2022-11', 50.99, 40.00)")

mycursor.execute("INSERT INTO Account(ID, BillingInfo, ShippingInfo) VALUES ('qwe','carl', 'uni')")
#TODO: debug=========================================================================================


selection = ""
while(selection != 0):

    print("\nIt is %d %s" % (currYear, month[currMonth]))
    print("Current Account: %s" % (currAcc))
    print("Enter 'm' or 'M' to go to next month")
    #TODO NEXT Month and calculate prevousely month report to sale record
    print("MENU -- Please input number 1 or 4 to select")
    print("1. User menu")
    print("2. Owner menu")
    print("3. Account menu")
    print("4. Quit")
    print("5. ==debug session==")
    selection = input("Enter select: ")

    if(selection == "1"):
        if(currAcc == None):
            print("Need to login by seleting 3")
            continue

        print("User menu selected")

        #while quit is not selected
        while(selection != -1):
            bookFound = 0
            userMenu()
            selection = input("Enter select: ")

            if(selection == "1"):
                bookname = input("Enter book name: ")
                mycursor.execute("SELECT Bookname, Book.ISBN, Author, Name, PageNumber, Price, InStock, StockPrice, Genre FROM Book NATURAL INNER JOIN CalculateIncome WHERE Bookname = %s", (bookname,) )

            elif(selection == "2"):
                author = input("Enter Author name: ")
                mycursor.execute("SELECT Bookname, Book.ISBN, Author, Name, PageNumber, Price, InStock, StockPrice, Genre FROM Book NATURAL INNER JOIN CalculateIncome WHERE Author = %s", (author,) )

            elif(selection == "3"):
                isbn = input("Enter ISBN: ")
                mycursor.execute("SELECT Bookname, Book.ISBN, Author, Name, PageNumber, Price, InStock, StockPrice, Genre FROM Book NATURAL INNER JOIN CalculateIncome WHERE Book.ISBN = %s", (isbn,) )

            elif(selection == "4"):
                genre = input("Enter genre: ")
                mycursor.execute("SELECT Bookname, Book.ISBN, Author, Name, PageNumber, Price, InStock, StockPrice, Genre FROM Book NATURAL INNER JOIN CalculateIncome WHERE Genre = %s", (genre,) )

            elif(selection == "5"):
                print("viewing cart")
                for i, num in zip (shoppingCartISBN, shoppingCartNum):
                    mycursor.execute("SELECT Bookname, Book.ISBN, Author, Name, PageNumber, Price, InStock, StockPrice FROM Book NATURAL INNER JOIN CalculateIncome WHERE Book.ISBN = %s", (i,) )
                    print("Book name;   ISBN;   Author;     Publisher;  Page #;     Price;   number in cart")
                    for x in mycursor:
                        print("%s;   %s,   %s,   %s,   %s,   $%.2f,   %d" %(x[0], x[1], x[2], x[3],  x[4], float(x[5]), num))

            elif(selection == "6"):
                print("Checking out from you shopping cart")
                bill = input("Billing Adress: ")
                ship = input("Shipping Adress: ")
                totalprice = 0.0

                #creating order
                totalOrder = totalOrder+1
                currDate = str(currYear)+ "-"+str(currMonth+1)
                try:
                    mycursor.execute("INSERT INTO Orders(OrderNumber, BillingInfo, ShippingInfo, TotalPrice, Date) VALUES (%s,%s,%s, %s, %s)", (totalOrder, bill, ship, 0.0, currDate))
                except:
                    print("Adding order failed")

                #add book info
                for num, p, book, stock, sprice in zip(shoppingCartNum, shoppingCartPrice, shoppingCartISBN, shoppingCartInStock, shoppingCartStockPrice):
                    try:
                        price = float(str(round(num*p, 2)))
                        #user purchase book
                        mycursor.execute("INSERT INTO GetInfo(ISBN, OrderNumber, Number , TotalPrice) VALUES (%s,%s,%s, %s)", (book, totalOrder, num, (price)))

                        #check if stock is still have more than 10 book
                        if(stock-num < 10):
                            #owner purchase book
                            stockprice = float(str(round(sprice * 10, 2))) 
                            mycursor.execute("INSERT INTO SalesRecord(ISBN, Date, Income, Expense) VALUES (%s,%s,%s, %s)", (book, currDate, price, stockprice))
                            #update book num TODO
                            mycursor.execute("UPDATE Book SET InStock = %s WHERE ISBN = %s", (stock-num+10, book))

                        totalprice = totalprice + price
                    except:
                        print("Book with %s ISBN purchase failed")
                totalprice = float(str(round(totalprice, 2)))
                
                try:
                    mycursor.execute("INSERT INTO PlaceOrder(ID, OrderNumber) VALUES (%s,%s)", (currAcc, totalOrder))
                    mycursor.execute("UPDATE Orders SET TotalPrice = %s WHERE OrderNumber = %s", (totalprice, totalOrder))
                    mycursor.execute("INSERT INTO TrackSystem(TrackingNum, Position, Status) VALUES (%s,%s,%s)", (totalOrder, "bookstore", "in progress"))
                    mycursor.execute("INSERT INTO Track(TrackingNum, OrderNumber) VALUES (%s,%s)", (totalOrder, totalOrder))
                except:
                    print("update order fail")
                print("Order complete")

            elif(selection == "7"):
                print("going back to menu")
                selection = -1 

            else:
                print("Enter the correct option please")
            
            #if user trys to find book
            if(selection == "1" or selection == "2" or selection == "3" or selection == "4" ):
                
                print("Finding books:")
                print("Book name;   ISBN;   Author;     Publisher;  Page #;     Price;      Genre")
                bookFound = 0
                for x in mycursor:
                    print("%s;   %s,   %s,   %s,   %s,   $%.2f,   %s" %(x[0], x[1], x[2], x[3],  x[4], float(x[5]), x[8]))
                    item = str(x[1])
                    itemprice = float(x[5])
                    iteminstock = int(x[6])
                    itemstockprice = float(x[7])
                    bookFound = bookFound +1

                if(bookFound == 0):
                    print("0 book found")
                elif(bookFound == 1):
                    print("Do you wants to add to shopping cart")
                    while not(selection == "y" or selection == "Y" or selection == "n" or selection == "N"):
                        selection = input("Enter Y or N: ")

                    #add to cart
                    if(selection == "y" or selection == "Y"):
                        itemNum = 0
                        while (itemNum <= 0 or itemNum > 10):
                            itemNum = input("Enter number book (max 10 book): ")
                            try:
                                itemNum = int(itemNum)
                            except:
                                print("Not a number")

                        shoppingCartISBN.append(item)
                        shoppingCartNum.append(itemNum)
                        shoppingCartPrice.append(float(itemprice))
                        shoppingCartInStock.append(iteminstock)
                        shoppingCartStockPrice.append(itemstockprice)
                        print("item have added to shopping cart")
                    

    elif(selection == "2"):
        print("Owner menu selected")
        while(selection != -2):
            ownerMenu()
            selection = input("Enter select: ")

            #adding book to store
            if(selection == "1"):
                publisher = input("Publisher of the book: ")
                print("A number for 0 to 1 in 2 decimal place where 1 is excluded ")
                percentage = input("Publisher portion of profit for the book: ")
                bookname = input("Book name: ")
                isbn = input("ISBN: ")
                genre = input("Genre: ")
                author = input("Author: ")
                pages = input("Number of pages: ")
                stock = input("Number of book in stock: ")
                print("Price must input with decimal in example 22.0 or 22.00, but not 22 or 22.000")
                price = input("Price (2 decimal place ): ")
                stockprice = input("Stock price (2 decimal place): ")
                #TODO: mycursor
                # try:

                #check number
                print("checking if pages number and in stock number is a number")
                pages = int(pages)
                stock = int(stock)
                print("pages and in stock checked")

                #check decimal
                print("checking if stock price, percentage of profit, and price is a number with at most 2 decimal place")
                if (len(price.rsplit('.')[-1]) > 2 or len(stockprice.rsplit('.')[-1]) > 2 or len(percentage.rsplit('.')[-1]) > 2 ):
                    print("Maximum 2 decimal place only please")
                    continue
                price = float(str(round(float(price), 2)))
                stockprice = float(str(round(float(stockprice), 2)))
                percentage = float(str(round(float(percentage), 2)))
                print("stock price, percentage of profit, and price is a number checked")

                print("checking if percentage of profit is from 0 to 1 (and it can not be 1)")
                if (percentage < 0 or percentage >= 1 ):
                    continue
                print("percentage checked")
                # price = str(price)
                # stockprice = str(stockprice)
                # percentage = str(percentage)

                #check publisher
                print("Check if publisher exist ")
                mycursor.execute("SELECT Name FROM Publisher WHERE Name = %s", (publisher,))
                print("Publisher found ")
                
                #TODO: DEBUG UNKNOW ERROR
                #trying to add book
                print("trying to add book")
                print("(%s,%s,%s, %s, %s, %s,%s,%s)" %(bookname, isbn, genre, price, author, pages, stock, stockprice))
                mycursor.execute("INSERT INTO Book (Bookname, ISBN, Genre, Price, Author, PageNumber, InStock, StockPrice) VALUES (%s,%s,%s, %s, %s, %s,%s,%s)", (bookname, isbn, genre, price, author, pages, stock, stockprice))
                #mycursor.execute("INSERT INTO Book(Bookname, ISBN, Genre, Price, Author, PageNumber, InStock, StockPrice))
                #mycursor.execute("INSERT INTO CalculateIncome(Name, ISBN, Percentage) VALUES (%s,%s, %f)", (publisher, isbn, percentage))

                # except:
                #     print("Checking failed, adding book fail. ")
                #     print("If the adding book process failed when trying to add book, this may cause by dupilcate book name or ISBN.")

            #removing book to store
            elif(selection == "2"):
                isbn = input("Please input the book isbn to remove book: ")
                mycursor.execute("DELETE FROM CalculateIncome WHERE ISBN = %s", (isbn, ))
                mycursor.execute("DELETE FROM Book WHERE ISBN = %s", (isbn, ))
                print("Removing book complete")

            #adding publisher
            elif(selection == "3"):
                name = input("Publisher name: ")
                address = input("Address: ")
                email = input("Email: ")
                phone = input("Phone: ")
                bank = input("Bank account: ")
                try:
                    mycursor.execute("INSERT INTO Publisher(Name, Address, Email, Phone, BankAccount) VALUES (%s,%s,%s, %s, %s)", (name, address, email, phone, bank))
                    print("adding publisher complete")
                except:
                    print("You have enter duplicate publisher name or something is wrong")

            #sales and expenses report
            elif(selection == "4"):
                print("Total sales and expenditure:")
                try:
                    mycursor.execute("SELECT sum(Income) FROM SalesRecord" )
                    for x in mycursor:
                        income = float(x[0])

                    #mycursor.execute("SELECT cast( sum(Expense) as float(2)) FROM SalesRecord")
                    mycursor.execute("SELECT sum(Expense) FROM SalesRecord")
                    for x in mycursor:
                        expense = int(x[0])

                    print("Total sale is $%.2f"% income)
                    print("Total expense is $%.2f"% expense)
                    print("Total profit is $%.2f"% (income -expense))

                except:
                    print("Unknown error")

            #genres sales
            elif(selection == "5"):
                print("Total sales by genres")
                try:
                    mycursor.execute("SELECT Genre, sum(Income) FROM SalesRecord NATURAL INNER JOIN Book GROUP BY Book.Genre " )
                    for x in mycursor:
                        print("Total sales for %s is $%.2f" %(x[0], float(x[1])))

                except:
                    print("Unknown error")

            #author sales
            elif(selection == "6"):
                print("Total sales by author")
                try:
                    mycursor.execute("SELECT Author, sum(Income) FROM SalesRecord NATURAL INNER JOIN Book GROUP BY Book.Author " )
                    for x in mycursor:
                        print("Total sales for %s is $%.2f" %(x[0], float(x[1])))

                except:
                    print("Unknown error")

            #last months report
            elif(selection == "7"):
                print("Report for last month only")
                try:
                    mycursor.execute("SELECT Date, sum(Income), sum(Expense) FROM SalesRecord GROUP BY Date " )
                    for x in mycursor:
                        print(str(x[0])[0:7] + " report")
                        print("Income for the month is $%.2f" %(float(x[1])))
                        print("Expense for the month is $%.2f" %(float(x[2])))
                        print("Profit for the month is $%.2f" %(float(x[1]) -float(x[2])))

                except:
                    print("Unknown error")

            elif(selection == "8"):
                print("Going back to menu")
                selection = -2

            else:
                print("Enter the correct option please")

    elif(selection == "3"):
        while(selection != -3):
            accMenu()
            selection = input("Enter select: ")

            if(selection == "1"):
                print("Sign up selected")
                user = input("User: ")
                bill = input("Billing Adress: ")
                ship = input("Shipping Adress: ")
                try:
                    mycursor.execute("INSERT INTO Account(ID, BillingInfo, ShippingInfo) VALUES (%s, %s,%s)" , (user, bill, ship))
                    print("Adding account complete")
                    currAcc = user

                except:
                    print("Duplicate user id")

            if(selection == "2"):
                print("Switching account will empty the shopping cart, and item in carts will not be saved")
                user = input("User: ")
                try:
                    mycursor.execute("SELECT IFNULL( (SELECT ID FROM Account WHERE ID = %s LIMIT 1), 'User not found' )", (user, ))
                    for x in mycursor:
                        if(str(x[0]) == user):
                            currAcc = user
                            print("Logged in")
                            shoppingCartInStock = []
                            shoppingCartISBN =[]
                            shoppingCartNum=[]
                            shoppingCartPrice=[]
                            shoppingCartStockPrice=[]
                        else:
                            print(x[0])

                except:
                    print("Unknown error")

            if(selection == "3"):
                selection = -3



    elif(selection == "4"):
        print("Quitting")
        selection = 0

#TODO: delete after debug finish
    elif(selection == "5"):
        print("debug session")
        print("1. display all book")
        print("2. display all publisher")
        print("3. display all Account")
        print("4. display all order")
        print("5. display all TrackSystem")
        print("6. display all OrderInfo")
        print("7. display all CalculateIncome")
        print("8. display all PlaceOrder")
        print("9. display all Tracking")
        print("10. display all SalesRecord")

        selection = input("Enter select: ")
        if(selection == "1"):
            #mycursor= db.cursor(buffered=True)
            mycursor.execute("SELECT * FROM Book")
            for x in mycursor:
                print(x)

        elif(selection == "2"):
            mycursor.execute("SELECT * FROM Publisher")
            for x in mycursor:
                print(x)

        elif(selection == "3"):
            mycursor.execute("SELECT * FROM Account")
            for x in mycursor:
                print(x)

        elif(selection == "4"):
            mycursor.execute("SELECT * FROM Orders")
            for x in mycursor:
                print(x)

        elif(selection == "5"):
            mycursor.execute("SELECT * FROM TrackSystem")
            for x in mycursor:
                print(x)

        elif(selection == "6"):
            mycursor.execute("SELECT * FROM GetInfo")
            for x in mycursor:
                print(x)

        elif(selection == "7"):
            mycursor.execute("SELECT * FROM CalculateIncome")
            for x in mycursor:
                print(x)

        elif(selection == "8"):
            mycursor.execute("SELECT * FROM PlaceOrder")
            for x in mycursor:
                print(x)

        elif(selection == "9"):
            mycursor.execute("SELECT * FROM Track")
            for x in mycursor:
                print(x)

        elif(selection == "10"):
            mycursor.execute("SELECT * FROM SalesRecord")
            for x in mycursor:
                print(x)

    elif(selection == "M" or selection == "m" ):
        if(currMonth == 11):
            currMonth = 0
        else:
            currMonth = currMonth+1

    else:
        print("Enter the correct option please")

#TODO:remove
#mycursor.execute("SELECT * FROM Book")
mycursor.execute("DESCRIBE Book")
for x in mycursor:
    print(x)

# db.commit() # to save it to db
print("Hello, World!")