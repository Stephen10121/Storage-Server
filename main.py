from cryptography.fernet import Fernet
import os
def user_stuff_exists():
    isdir = os.path.isdir('user_stuff') 
    if isdir!=True:
        os.mkdir('user_stuff')

def key_exists():
    if os.path.isfile('key.key')!=True:
        key = Fernet.generate_key()
        file = open('key.key', 'wb')
        file.write(key)
        file.close()
user_stuff_exists()
key_exists()
import functions as F
import encrypt as E
from flask import Flask, render_template, request, make_response, redirect, url_for
app = Flask('app')

F.add_def_user('test', 'test', 'test')

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'WOWPOW' in request.cookies:
        if request.cookies['WOWPOW']=='':
            return render_template("index.html", what=[False, True, False])
        else:
            id = int(E.decrypt(request.cookies['WOWPOW'])[1])
            dirpath = 'root'
            if request.method == 'POST':
                if request.form.get('dirpath'):
                    nowpath = request.form.get('dirpath')
                    newpath = request.form.get('chdir')
                    if nowpath=='root':
                        dirpath=''
                        dirpath+=newpath
                        return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath)
                    else:
                        nowpath+='/'+newpath
                        dirpath=nowpath
                        print(nowpath,'wow')
                        return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath)
                elif request.form.get('sharewhat'):
                    what = request.form.get('sharewhat')
                    towho = request.form.get('sendto')
                    if F.user_exists(towho)==True:
                        what = F.share_folder(id, what, F.get_id(towho))
                        if what=='user_has_dir':
                            return render_template("welcome.html", error='That user has a folder named the same as the one your sharing' ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath)
                        elif what==True:
                            return render_template("welcome.html", error='Success', what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath)
                        else:
                            print('error_1')
                            return render_template("welcome.html", error='error_1' ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath)
                    else:
                        return render_template("welcome.html", error="User doesn't exist!" ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath)
                elif request.form.get('rename'):
                    renamewhat=request.form.get('rename')
                    path=request.form.get('renamepath')
                    rename_result = F.rename_folder(path, renamewhat, id)
                    if rename_result==False:
                        return render_template("welcome.html", error='folder_rename_error' ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath)
                    elif rename_result=='rndirexists':
                        return render_template("welcome.html", error='folder_rename_exists' ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath)
                    elif rename_result=='spacebar':
                        return render_template("welcome.html", error='folder_rename_spacebar' ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath)
                    else:
                        return render_template("welcome.html", error='Success', what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath)
                elif request.form.get('delete_folder'):
                    delete = request.form.get('delete_folder')
                    if F.del_folder(delete, id)==True:
                        return render_template("welcome.html", error='Folder Deleted' ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath)
                    else:
                        return render_template("welcome.html", error="Folder didn't delete" ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath)
            return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath)
    else:
        return render_template("index.html", what=[False, True, False])

@app.route('/shared', methods=['GET', 'POST'])
def share_page():
    if 'WOWPOW' in request.cookies:
        if request.cookies['WOWPOW']=='':
            return redirect('/')
        else:
            id=int(E.decrypt(request.cookies['WOWPOW'])[1])
            is_id = F.is_id(id)
            if is_id != None:
                return render_template("shared.html", what=[True, True, F.get_userinfo(id)], folders=F.get_shared_folders(id))
            else:
                res=make_response(redirect('/'))
                res.set_cookie('WOWPOW', '')
                return res
    else:
        return redirect('/')

@app.route('/trash', methods=['GET', 'POST'])
def trash_page():
    if 'WOWPOW' in request.cookies:
        if request.cookies['WOWPOW']=='':
            return redirect('/')
        else:
            id=int(E.decrypt(request.cookies['WOWPOW'])[1])
            is_id = F.is_id(id)
            if is_id != None:
                return render_template("trash.html", what=[True, True, F.get_userinfo(id)], folders=F.get_trash_folders(id))
            else:
                res=make_response(redirect('/'))
                res.set_cookie('WOWPOW', '')
                return res
    else:
        return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup_form():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        rpassword = request.form.get('rpassword')
        email= request.form.get('email')
        jeff = F.signup(username, password, rpassword, name, email)
        if jeff=='userexists':
            return render_template('signup.html', error='userexists', what=[True, False])
        elif jeff=='passwordmatch':
            return render_template('signup.html', error='passwordnotmatch', what=[True, False])
        else:
            user_id=F.get_id(username)[0]
            F.init_folder(user_id)
            res=make_response(redirect('/'))
            res.set_cookie('WOWPOW',E.encrypt(str(F.get_id(username))))
            return res
    else:
        return render_template("signup.html", what=[True, False])

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        info = F.login(username, password)
        if info=='usernotexist':
            return render_template('login.html', error='usernotexist', what=[True, False])
        elif info=='wrongpassword':
            return render_template('login.html', error='wrongpassword', what=[True, False])
        else:
            user_id = F.get_id(username)[0]
            res=make_response(redirect('/'))
            res.set_cookie('WOWPOW', E.encrypt(str(F.get_id(username))))
            return res
    else:
        return render_template("login.html", what=[True, False])

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    res = make_response(render_template("index.html", what=[False, True, False]))
    res.set_cookie('WOWPOW','')
    return res

app.run(host='0.0.0.0', port=8080)
#app.run(host='10.51.33.18', port=8080)
