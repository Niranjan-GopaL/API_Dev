> EXTREMELY IMPORTANT :-
You can commit SECTIONS OF CODE ; like this :- 

1. DELETE pycache and restart the server ;
2. If you have an orphaned process that is running the server :
    - try `netstat -ano | findstr :8000` finding if the port is being used
    - if you can't kill it ; try from taskbar
    - if you still can't ; REBOOT
3. DON'T FORGET TO WRITE returning *; after UPDATE, INSERT, DELETE otherwise IT WILL GIVE
    INTERNAL SERVER ERROR; and give a `Nothing to fetch` error

> So if the result of a .fetchall() is empty, REMEMBER IT IS `[]`
> if updated_post == []  <--- correct way
> if not updated_post    <--- safest way
print(  None is [] ) =========> False
print(  None == [] ) =========> False


superuser password : 123 (Lol!)
- Installation Directory: C:\Program Files\PostgreSQL\16
- Server Installation Directory: C:\Program Files\PostgreSQL\16
- Data Directory: C:\Program Files\PostgreSQL\16\data
- Database Port: 5432
- Database Superuser: postgres
- Operating System Account: NT AUTHORITY\NetworkService
- Database Service: postgresql-x64-16
- Command Line Tools Installation Directory: C:\Program Files\PostgreSQL\16
- pgAdmin4 Installation Directory: C:\Program Files\PostgreSQL\16\pgAdmin 4
- Installation Log: C:\Users\HP\AppData\Local\Temp\install-postgresql.log