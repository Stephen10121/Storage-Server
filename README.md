# Storage-Server
This is a project I made to try and recreate Google Drive. I felt like it would be cool if I had my own online storage.
This will also probably be an example of what I could do in my resume.


# Important
When cloning this repository and you want to run it, first go to functions.py, line 20(might change) where it shows this:
```bash
cursor.execute("INSERT INTO users (user_name, user_rname, user_password, user_email) VALUES ('"+user_name+"', '"+user_rname+"', '"+user_password+"', '"+user_email+"')")
```
Change that into this:
```bash
cursor.execute("INSERT INTO users (id, user_name, user_rname, user_password, user_email) VALUES (1,'"+user_name+"', '"+user_rname+"', '"+user_password+"', '"+user_email+"')")
```
