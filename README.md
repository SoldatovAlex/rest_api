# akvelon_python_internship_3_alex_soldatov
Tasks description
Task 1: Would need to build a REST API for storing user and transactions information. 
Task 2: Implement a function which will return n’th number of Fibonacci sequence.
# Solution
To implement the first task(to build a REST API), the following frameworks were chosen: flask, flask_restful,sqlalchemy. As DBMS was chosen sqlite3. The solution to the first task is contained in the files: 'rest_api', 'setup_db'

To implement the second task(return n’th number of Fibonacci sequence) were used standard library tools. In file 'utils' contained 2 solutions.

# Rest api implementation

Was used 2 view which contained get, put, delete methods. One view per entity: User, Transaction. Methods takes id(user or transaction) as an input parameter. Methods are responsible for functionality as the name suggests. 

Was used 2 view which contained post method. One view per entity: User, Transaction. Methods takes parameter for creating new user or transaction from requests body. Methods are create new user or transaction in database. 

Also 4 functions were created
1) user_trans_amount_sort(user_id)
This func takes input parameter - user id. In response, all user's transactions sorted.
2) define_transaction_type(id)
This func takes input parameter - transaction id. In response, type of transaction.
3) group_by_date(user_id)
This func takes input parameter - user id. In response, sum all user's transactions group by date. This method can helps to understand, was day with posite or negative balance.
4) users_transaction(user_id)
This func takes input parameter - user id. In response, all user's transaction.

# How create requests 

Requests are created according to the following rules:

Post methods: http://127.0.0.1:8000/user or http://127.0.0.1:8000/transaction
Post request must have parameters for creating new entity in body. For example, for creating new user3's transaction in request's body must be in

Put methods: http://127.0.0.1:8000/user/<int:id> or http://127.0.0.1:8000/transaction/<int:id>
Put methods like a post methods, must have params in request's body

Get, Delete methods from Views: http://127.0.0.1:8000/user/<int:id> or http://127.0.0.1:8000/transaction/<int:id>

GET methods with following path: 
1. http://127.0.0.1:8000//transactionamountsort/<int:user_id>
2. http://127.0.0.1:8000//transactiontype/<int:id>
3. http://127.0.0.1:8000//sumbydate/<int:user_id>
4. http://127.0.0.1:8000//userstransaction/<int:user_id>

Author used "Postman" software for testing application: 

![image](https://user-images.githubusercontent.com/52040568/121198324-b731ed80-c87a-11eb-910a-d63a2d5104fb.jpg)
