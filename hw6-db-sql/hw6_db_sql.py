'''
Name: Shengnan Duan
Uniqname: elenore
'''

import sqlite3 
from tabulate import tabulate 
import datetime
from dateutil.parser import parse

def connect_db(query):
    conn = sqlite3.connect('Northwind_small.sqlite')
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
    conn.close()
    return result

def question0():
    ''' Constructs and executes SQL query to retrieve
    all fields from the Region table
    
    Parameters
    ----------
    None
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = sqlite3.connect("Northwind_small.sqlite")
    cursor = connection.cursor()
    query = "SELECT * FROM Region"
    result = cursor.execute(query).fetchall()
    connection.close()
    return result

def question1():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements
    
    Parameters
    ----------
    None
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''

    query1 = "SELECT * FROM Territory"
    return connect_db(query1)


def question2():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements
    
    Parameters
    ----------
    None
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    query2 = "SELECT COUNT (Id) FROM Employee"
    return connect_db(query2)

def question3():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements
    
    Parameters
    ----------
    None
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    query3 = "SELECT * FROM Product ORDER BY Id DESC LIMIT 10"
    return connect_db(query3)

def question4():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements
    
    Parameters
    ----------
    None
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    query4 = "SELECT ProductName, UnitPrice FROM Product ORDER BY UnitPrice DESC LIMIT 3"
    return connect_db(query4)

def question5():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements
    
    Parameters
    ----------
    None
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    query5 = "SELECT ProductName, UnitPrice, UnitsInStock FROM Product WHERE UnitsInStock BETWEEN 60 AND 100"
    return connect_db(query5)

def question6():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements
    
    Parameters
    ----------
    None
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    query6 = "SELECT ProductName FROM Product WHERE UnitsInStock < ReorderLevel"
    return connect_db(query6)

def question7():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements
    
    Parameters
    ----------
    None
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    query7 = "SELECT Id FROM [Order] WHERE ShipCountry ='France' AND ShipPostalCode LIKE '%04'"
    return connect_db(query7)

def question8():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements
    
    Parameters
    ----------
    None
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    query8 = "SELECT CompanyName, ContactName FROM Customer WHERE Country='UK' AND Fax IS NOT NULL"
    return connect_db(query8)

def question9():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements
    
    Parameters
    ----------
    None
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    query9 = "SELECT Product.ProductName, Product.UnitPrice FROM Product JOIN Category ON Product.CategoryId=Category.Id WHERE Product.CategoryId=1"
    return connect_db(query9)

def question10():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements
    
    Parameters
    ----------
    None
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    query10 = "SELECT Product.ProductName FROM Product JOIN Category ON Product.CategoryId=Category.Id WHERE Product.CategoryId=6 AND Product.Discontinued=1"
    return connect_db(query10)

def question11():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements
    
    Parameters
    ----------
    None
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    query11 = "SELECT [Order].Id, Employee.FirstName, Employee.LastName FROM [Order] jOIN Employee ON [Order].EmployeeId=Employee.Id Where [Order].ShipCountry='Germany'"
    return connect_db(query11)

def question12():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements
    
    Parameters
    ----------
    None
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    query12 = "SELECT [Order].Id, [Order].OrderDate, Customer.CompanyName FROM [Order] JOIN Customer on [Order].CustomerId=Customer.Id WHERE [Order].OrderDate <= '2012-07-10'"
    return connect_db(query12)



#################################################################
########################  ECs start here  #######################
#################################################################

#########
## EC1 ##
#########

def print_query_result(raw_query_result):
    ''' Pretty prints raw query result
    
    Parameters
    ----------
    list 
        a list of tuples that represent raw query result
    
    Returns
    -------
    None
    '''
    print(tabulate(raw_query_result, tablefmt='psql'))


if __name__ == "__main__":
    '''WHEN SUBMIT, UNCOMMENT THE TWO LINES OF CODE
    BELOW IF YOU COMPLETED EC1'''

    result = question9()
    print_query_result(result)
 

#########
## EC2 ##
#########
    
    while True:
        user_input = input("Please enter a Order Date and a Ship Country seperated by space (e.g. 2012-07-04 France), or 'exit' to quit: ")
        user_input_split = user_input.split()

        if user_input =='exit':
            exit()
        elif len(user_input_split)==2:
            query_test = f"SELECT Employee.FirstName, Employee.LastName FROM Employee JOIN [Order] ON Employee.Id=[Order].EmployeeId WHERE [Order].OrderDate = '{user_input_split[0]}' AND [Order].ShipCountry ='{user_input_split[1]}'" 
            if len(connect_db(query_test)) == 0:
                print('Sorry! Your search returns no results.') 
            else:
                print_query_result(connect_db(query_test))
        else:
            print('Invalid Input. Please enter a Order Date and a Ship Country seperated by space: ')
    
        



