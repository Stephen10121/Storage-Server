# Storage-Server
A server that is basically like google drive. Still under development.


# Important
When cloning this repository and you want to run it, first go to functions.py, line 20(might change) where it shows this:
```bash
cursor.execute("INSERT INTO users (user_name, user_rname, user_password, user_email) VALUES ('"+user_name+"', '"+user_rname+"', '"+user_password+"', '"+user_email+"')")
```
Change that into this:
```bash
cursor.execute("INSERT INTO users (id, user_name, user_rname, user_password, user_email) VALUES (1,'"+user_name+"', '"+user_rname+"', '"+user_password+"', '"+user_email+"')")
```
Run the script and signup once. After signing up, revert back to the original line and save the file.
Also make a key.key file.
