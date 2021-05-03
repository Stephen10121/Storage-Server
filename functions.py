import os
import hashlib
import sqlite3
from cryptography.fernet import Fernet
import encrypt as E
from shutil import copytree, copyfile, rmtree

conn = sqlite3.connect('user_db.db', check_same_thread=False)
cursor=conn.cursor()

comm= """CREATE TABLE IF NOT EXISTS
users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    user_rname TEXT,
    user_password TEXT,
    user_email TEXT
)"""
cursor.execute(comm)

comm = """CREATE TABLE IF NOT EXISTS
stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_owner INTEGER,
    stock_name TEXT,
    stock_cost TEXT,
    stock_amount TEXT
)"""

cursor.execute(comm)

def add_def_stock():
    cursor.execute("INSERT INTO stocks (stock_owner, stock_name, stock_cost, stock_amount) VALUES (1, 'TSLA', '9.54', '10')")
    conn.commit()

def get_stock(owner_id):
    getit = cursor.execute("SELECT stock_name FROM stocks WHERE stock_owner="+owner_id+"")
    for i in getit:
        print(i)
    
def add_user(user_name, user_rname ,user_password, user_email):
    cursor.execute("INSERT INTO users (user_name, user_rname, user_password, user_email) VALUES ('"+user_name+"', '"+user_rname+"', '"+user_password+"', '"+user_email+"')")
    conn.commit()

def user_exists(user_name):
    find=cursor.execute("SELECT EXISTS(SELECT user_name FROM users WHERE user_name='%s');"%(user_name))
    for i in find:
        if i[0]==0:
            return False
        else:
            return True

def is_id(id):
    get=cursor.execute("SELECT user_name FROM users WHERE id='%s'"%(str(id)))
    for i in get:
        return i

def add_def_user(user_name, user_rname , user_email):
    if is_id(1)==None:
        def get_pass():
            pass1=input("First account password: ")
            pass2=input('Repeat first account password: ')
            if pass1==pass2:
                return pass1
            else:
                get_pass()
        user_password = get_pass()
        user_password = hashlib.sha224(user_password.encode()).hexdigest()
        cursor.execute("INSERT INTO users (id, user_name, user_rname, user_password, user_email) VALUES (1,'"+user_name+"', '"+user_rname+"', '"+user_password+"', '"+user_email+"')")
        conn.commit()

def get_userinfo(id):
    get=cursor.execute("SELECT id, user_name, user_rname, user_email FROM users WHERE id=%s"%(id))
    for i in get:
        return i

def compare_pass(id, password):
    get=cursor.execute("SELECT user_password FROM users WHERE id='%s'"%(id))
    for i in get:
        if i[0]==hashlib.sha224(password.encode()).hexdigest():
            return True
        else:
            return False

def get_id(user_name):
    get=cursor.execute("SELECT id FROM users WHERE user_name='%s'"%(user_name))
    for i in get:
        return i

def signup(u,p,rp,name,email):
    if user_exists(u)!=True:
        if p==rp:
            p2 =hashlib.sha224(p.encode()).hexdigest()
            add_user(u, name, p2, email)
            id=get_id(u)
            return get_userinfo(id)
        else:
            return 'passwordmatch'
    else:
        return 'userexists'

def login(u,p):
    if user_exists(u)==False:
        return 'usernotexist'
    else:
        id=get_id(u)
        if compare_pass(id, p)==True:
            return get_userinfo(id)
        else:
            return 'wrongpassword'

def init_folder(id):
    print(id)
    eid = str(hashlib.sha224(str(id).encode()).hexdigest())
    os.chdir('user_stuff')
    isdir = os.path.isdir(eid) 
    if isdir!=True:
        os.mkdir(eid)
        os.chdir(eid)
        os.mkdir('trash')
        os.mkdir('shared')
        os.chdir('..')
        os.chdir('..')
    else:
        os.chdir('..')
        return False

def get_folders(id, path):
    eid = str(hashlib.sha224(str(id).encode()).hexdigest())
    os.chdir('user_stuff')
    isdir = os.path.isdir(eid) 
    if isdir==True:
        os.chdir(eid)
        if os.path.isdir('shared')!=True:
            os.mkdir('shared')
        if os.path.isdir('trash')!=True:
            os.mkdir('trash')
        if path == 'root':
            give=[]
            for i in os.walk('./'):
                w=i[0][2:]
                if w!='':
                    give.append(w)
            os.chdir('..')
            os.chdir('..')
            return give
        else:
            dirs = 0
            for i in path.split('/'):
                os.chdir(i)
                dirs+=1
            give=[]
            for i in os.walk('./'):
                w=i[0][2:]
                if w!='':
                    give.append(w)
            for i in range(dirs):
                os.chdir('..')
            os.chdir('..')
            os.chdir('..')
            return give
    else:
        os.mkdir(eid)
        os.chdir('..')
        return False

def get_shared_folders(id):
    eid = str(hashlib.sha224(str(id).encode()).hexdigest())
    os.chdir('user_stuff')
    isdir = os.path.isdir(eid) 
    if isdir==True:
        os.chdir(eid)
        os.chdir('shared')
        give=[]
        for i in os.walk('./'):
            w=i[0][2:]
            if w!='':
                give.append(w)
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        return give
    else:
        os.mkdir(eid)
        os.chdir('..')
        return False

def get_trash_folders(id):
    eid = str(hashlib.sha224(str(id).encode()).hexdigest())
    os.chdir('user_stuff')
    isdir = os.path.isdir(eid) 
    if isdir==True:
        os.chdir(eid)
        os.chdir('trash')
        give=[]
        for i in os.walk('./'):
            w=i[0][2:]
            if w!='':
                give.append(w)
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        return give
    else:
        os.mkdir(eid)
        os.chdir('..')
        return False

def del_folder(what, id):
    eid = str(hashlib.sha224(str(id).encode()).hexdigest())
    os.chdir('user_stuff')
    isdir = os.path.isdir(eid) 
    if isdir==True:
        os.chdir(eid)
        isdeldir = os.path.isdir(what)
        if isdeldir==True:
            os.rmdir(what)
            os.chdir('..')
            os.chdir('..')
            return True
        else:
            os.chdir('..')
            os.chdir('..')
            return False 
    else:
        os.chdir('..')
        return False

def rename_folder(what, renameto, id):
    eid = str(hashlib.sha224(str(id).encode()).hexdigest())
    os.chdir('user_stuff')
    isdir = os.path.isdir(eid) 
    if isdir==True:
        os.chdir(eid)
        if '/' in what:
            what2 = what.split('/')
            for i in what2[::-1][1:][::-1]:
                os.chdir(i)
            isdir= os.path.isdir(what2[::-1][0])
            if isdir==True:
                existrndir=os.path.isdir(renameto)
                if existrndir==True:
                    for i in what2[::-1][1:][::-1]:
                        os.chdir('..')
                    os.chdir('..')
                    os.chdir('..')
                    return 'rndirexists'
                else:
                    if ' ' in renameto:
                        for i in what2[::-1][1:][::-1]:
                            os.chdir('..')
                        os.chdir('..')
                        os.chdir('..')
                        return 'spacebar'
                    else:
                        os.rename(what2[::-1][0], renameto)
                        for i in what2[::-1][1:][::-1]:
                            os.chdir('..')
                        os.chdir('..')
                        os.chdir('..')
                        return True
            else:
                for i in what2[::-1][1:][::-1]:
                    os.chdir('..')
                os.chdir('..')
                os.chdir('..')
                return False             
        else:
            isdir = os.path.isdir(what)
            if isdir==True:
                existrndir=os.path.isdir(renameto)
                if existrndir==True:
                    os.chdir('..')
                    os.chdir('..')
                    return 'rndirexists'
                else:
                    if ' ' in renameto:
                        os.chdir('..')
                        os.chdir('..')
                        return 'spacebar'
                    else:
                        os.rename(what, renameto)
                        os.chdir('..')
                        os.chdir('..')
                        return True
            else:
                os.chdir('..')
                os.chdir('..')
                return False
    else:
        os.chdir('..')
        return False

def trash_folder(id, what):
    eid = str(hashlib.sha224(str(id).encode()).hexdigest())
    os.chdir('user_stuff')
    isdir = os.path.isdir(eid)
    if isdir==True:
            os.chdir(eid)
            if '/' in what:
                what2 = what.split('/')
                dest=''
                for i in what2[::-1][1:][::-1]:
                    os.chdir(i)
                    dest+='../'
                copytree(what2[::-1][0], dest+'/trash/'+what2[::-1][0])
                rmtree(what2[::-1][0])
                for i in what2[::-1][1:][::-1]:
                    os.chdir('..')
                os.chdir('..')
                os.chdir('..')
                return True
            else:
                copytree(what, 'trash/'+what)
                rmtree(what)
                os.chdir('..')
                os.chdir('..')
                return True
    else:
        os.chdir('..')
        return 'user_not_exists'

def share_folder(id, what, towhom):
    eid = str(hashlib.sha224(str(towhom[0]).encode()).hexdigest())
    myid = str(hashlib.sha224(str(id).encode()).hexdigest())
    os.chdir('user_stuff')
    isdir = os.path.isdir(eid)
    if isdir==True:
        myisdir = os.path.isdir(myid)
        if myisdir==True:
            os.chdir(eid)
            os.chdir('shared')
            iswhatdir = os.path.isdir(what)
            if iswhatdir==True:
                os.chdir('..')
                os.chdir('..')
                os.chdir('..')
                return 'user_has_dir'
            else:
                os.chdir('..')
                os.chdir('..')
                src='./'+myid+'/'+'Pics/2019'
                dest=''
                if '/' in what:
                    what2=what.split('/')[::-1][0]
                    dest='./'+eid+"/shared/"+what2
                else:
                    dest='./'+eid+"/shared/"+what
                copytree(src, dest)
                os.chdir('..')
                return True
        else:
            os.chdir('..')
            return False
    else:
        os.chdir('..')
        return 'share_user_not_exists'

def share_file(id, what, towhom):
    eid = str(hashlib.sha224(str(towhom).encode()).hexdigest())
    myid = str(hashlib.sha224(str(id).encode()).hexdigest())
    os.chdir('user_stuff')
    isdir = os.path.isdir(eid)
    if isdir==True:
        myisdir = os.path.isdir(myid)
        if myisdir==True:
            copyfile('./'+myid+'/'+what, './'+eid+"/shared/"+what)
            return True
        else:
            os.chdir('..')
            return 'share_user_not_exists'
    else:
        os.chdir('..')
        return 'share_user_not_exists'

def move_dir(id, what, where):
    eid = str(hashlib.sha224(str(id).encode()).hexdigest())
    os.chdir('user_stuff')
    isdir = os.path.isdir(eid)
    if isdir==True:
        os.chdir(eid)
        iswhatdir = os.path.isdir(what)
        if iswhatdir==True:
            iswheredir=os.path.isdir(where)
            if iswheredir==True:
                if '/' in what:
                    what2=what.split('/')[::-1][0]
                    copytree(what, where+"/"+what2)
                else:
                    copytree(what, where+"/"+what)
                rmtree(what)
                os.chdir('..')
                os.chdir('..')
                return True
            else:
                os.chdir('..')
                os.chdir('..')
                return 'move_place_none'
        else:
            os.chdir('..')
            os.chdir('..')
            return 'error_4'
    else:
        os.chdir('..')
        return 'error_3'
        
#Testing

def testing(id):
    get=cursor.execute("SELECT user_name FROM users WHERE id='%s'"%(str(id)))
    for i in get:
        return i
