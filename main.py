from cryptography.fernet import Fernet
import os
from flask.helpers import send_file
import hashlib

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
from flask import Flask, render_template, request, make_response, redirect, url_for, jsonify
app = Flask('app')

F.add_def_user('test', 'test', 'test')

@app.errorhandler(404)
def page_not_found(e):
    if request.method == 'POST':
        if request.form.get('home'):
            return redirect('/')
    return render_template('404.html'), 404

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.cookies['WOWPOW']=='':
            return redirect(url_for('/'))
    else:
        id = int(E.decrypt(request.cookies['WOWPOW'])[1])
        eid = str(hashlib.sha224(str(id).encode()).hexdigest())
        if request.method == 'POST':
            if request.form.get('download'):
                dfile = request.form.get('download')
                dpath = request.form.get('dpath')
                if dpath == 'root':
                    return send_file('user_stuff\\'+eid+'\\'+dfile, attachment_filename=dfile, as_attachment=True)
                else:
                    return send_file('user_stuff\\'+eid+'\\'+dpath+'\\'+dfile, attachment_filename=dfile, as_attachment=True)
            else:
                return redirect(url_for('/'))
        else:
            return redirect(url_for('/'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.cookies['WOWPOW']=='':
        return redirect(url_for('/'))
    else:
        id = int(E.decrypt(request.cookies['WOWPOW'])[1])
        setting = F.get_settings(id)[2:]
        if request.method == 'POST':
            req = request.get_json()
            upref = {
                'share': req['Eshare'],
                'account': req['Eaccount'],
                'lightmode': req['Elightmode'],
                'stocks': req['Estocks'],
                'notify': req['Enotify'],
                'trash': req['Etrash'],
                'encrypt': req['Eencrypt'],
                'auth': req['Eauth'],
                '2auth': req['E2auth']
            }
            if upref['auth']==False:
                F.res_2pass(id)
            if F.save_settings(id, upref) != True:
                res = make_response(jsonify({'message':'Error!'}), 200)
                return res
            else:
                setting = F.get_settings(id)[2:]
                res = make_response(jsonify({'message':'Settings changed!', 'settings': F.get_settings(id)[2:]}), 200)
                return res
        else:
            return render_template("settings.html", what=[True, True, F.get_userinfo(id)], settings=setting)

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'WOWPOW' in request.cookies:
        if request.cookies['WOWPOW']=='':
            return render_template("index.html", what=[False, True, False])
        else:
            id = int(E.decrypt(request.cookies['WOWPOW'])[1])
            setting = F.get_settings(id)[2:]
            dirpath = 'root'
            if request.method == 'POST':
                if request.form.get('delete_file'):
                    delete = request.form.get('delete_file')
                    path=dirpath
                    if '/' in delete:
                        d2 = delete.split('/')[::-1][1:][::-1]
                        fin = ''
                        for i in d2:
                            fin+='/'+i
                        path=fin[1:]
                    if F.del_file(delete, id)==True:
                        return render_template("welcome.html", error='Folder Deleted' ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, path), path=path, files=F.get_files(id, path), settings=setting)
                    else:
                        return render_template("welcome.html", error="Folder didn't delete" ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                if request.form.get('add-file-path'):
                    path = request.form.get('add-file-path')
                    add_file = request.files['add-file']
                    seeif = F.add_file(id, path, add_file)
                    if seeif==True:
                        return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], error="Success!", folders=F.get_folders(id, path), path=path, files=F.get_files(id, path), settings=setting)
                    elif seeif==False:
                        return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], error="No file was selected!", folders=F.get_folders(id, path), path=path, files=F.get_files(id, path), settings=setting)
                elif request.form.get('file-menu'):
                    file_menu = request.form.get('file-menu')
                    file_menu_path = request.form.get('file-menu-path')
                    return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, file_menu_path), path=file_menu_path, files=F.get_files(id, file_menu_path), showfilemenu=file_menu, settings=setting)
                elif request.form.get('cdir'):
                    cdir = request.form.get('cdir')[::-1][1:][::-1]
                    cdirpath = request.form.get('cdirpath')
                    newpath=''
                    j=False
                    if '/' in cdirpath:
                        for i in cdirpath.split('/'):
                            if i==cdir:
                                newpath+=i+'/'
                                j=True
                            else:
                                if j==False:
                                    newpath+=i+'/'
                        newpath=newpath[::-1][1:][::-1]
                    else:
                        return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, cdirpath), path=cdirpath, files=F.get_files(id, cdirpath), settings=setting)
                    return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, newpath), path=newpath, files=F.get_files(id, newpath), settings=setting)
                elif request.form.get('createfolderpath'):
                    path = request.form.get('createfolderpath')
                    fname = request.form.get('foldername')
                    create_folder = F.create_folder(id, path, fname)
                    if create_folder==True:
                        return render_template("welcome.html", error="Success!", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, path), path=path, files=F.get_files(id, path), settings=setting)
                    elif create_folder=='folder_exist':
                        return render_template("welcome.html",error="That folder already exists!" ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, path), path=path, files=F.get_files(id, path), settings=setting)
                    else:
                        return render_template("welcome.html",error="ERROR" ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, path), path=path, files=F.get_files(id, path), settings=setting)
                elif request.form.get('goback'):
                    npath = request.form.get('goback').split('/')[::-1][1:][::-1]
                    path=''
                    for i in npath:
                        path+='/'+i
                    path = path[1:] if path!='' else 'root'
                    return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, path), path=path, files=F.get_files(id, path), settings=setting)
                elif request.form.get("moveto"):
                    moveto = request.form.get('moveto')
                    movewhat = request.form.get('movepath')
                    moveit = F.move_dir(id, movewhat, moveto)
                    if moveit=='cant_move_past_root':
                        return render_template("welcome.html", error="You can't move directory past your root folder.", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                    elif moveit=='move_place_none':
                        return render_template("welcome.html", error="The place you're moving the folder to doesn't exist.", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                    elif moveit=='error_3':
                        return render_template("welcome.html", error="error_3", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                    elif moveit=='error_4':
                        return render_template("welcome.html", error="error_4", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                    else:
                        return render_template("welcome.html", error="Success!", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                elif request.form.get('cancel'):
                    return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                elif request.form.get('movefolder'):
                    what = request.form.get('movefolder')
                    if '/' in what:
                        what2=what.split('/')
                        return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, movefolder=[what, what2[::-1][0]], files=F.get_files(id, dirpath), settings=setting)
                    else:
                        return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, movefolder=[False, what], files=F.get_files(id, dirpath), settings=setting)
                elif request.form.get('trashwhat'):
                    what=request.form.get('trashwhat')
                    trash_it = F.trash_folder(id, what)
                    if trash_it==True:
                        return render_template("welcome.html", error='Success', what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                    elif trash_it=='user_not_exists':
                        return render_template("welcome.html", error='error_2', what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                elif request.form.get('dirpath'):
                    nowpath = request.form.get('dirpath')
                    newpath = request.form.get('chdir')
                    if nowpath=='root':
                        dirpath=''
                        dirpath+=newpath
                        return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                    else:
                        nowpath+='/'+newpath
                        dirpath=nowpath
                        return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                elif request.form.get('sharewhat'):
                    what = request.form.get('sharewhat')
                    towho = request.form.get('sendto')
                    if F.user_exists(towho)==True:
                        what = F.share_folder(id, what, F.get_id(towho))
                        if what=='user_has_dir':
                            return render_template("welcome.html", error='That user has a folder named the same as the one your sharing' ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                        elif what==True:
                            return render_template("welcome.html", error='Success', what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                        elif what=='share_user_not_exists':
                            return render_template("welcome.html", error="User doesn't exist.", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                        else:
                            return render_template("welcome.html", error='error_1' ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                    else:
                        return render_template("welcome.html", error="User doesn't exist!" ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                elif request.form.get('rename'):
                    renamewhat=request.form.get('rename')
                    path=request.form.get('renamepath')
                    rename_result = F.rename_folder(path, renamewhat, id)
                    if rename_result==False:
                        return render_template("welcome.html", error='folder_rename_error' ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                    elif rename_result=='rndirexists':
                        return render_template("welcome.html", error='folder_rename_exists' ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                    elif rename_result=='spacebar':
                        return render_template("welcome.html", error='folder_rename_spacebar' ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                    else:
                        return render_template("welcome.html", error='Success', what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                elif request.form.get('delete_folder'):
                    delete = request.form.get('delete_folder')
                    if F.del_folder(delete, id)==True:
                        return render_template("welcome.html", error='Folder Deleted' ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
                    else:
                        return render_template("welcome.html", error="Folder didn't delete" ,what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
            return render_template("welcome.html", what=[True, True, F.get_userinfo(id)], folders=F.get_folders(id, dirpath), path=dirpath, files=F.get_files(id, dirpath), settings=setting)
    else:
        return render_template("index.html", what=[False, True, False])

@app.route('/shared', methods=['GET', 'POST'])
def share_page():
    if 'WOWPOW' in request.cookies:
        if request.cookies['WOWPOW']=='':
            return redirect('/')
        else:
            id=int(E.decrypt(request.cookies['WOWPOW'])[1])
            setting = F.get_settings(id)[2:]
            if setting[0]==0:
                return redirect('/')
            else:
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
        nallowed = [' ', '/']
        for i in nallowed:
            if i in username:
                return render_template('signup.html', error='forbidchar', what=[True, False])
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
        if request.form.get('sec-password'):
            return render_template('login.html', error='wrongpassword', what=[True, False])
        else:
            username = request.form.get('username')
            password = request.form.get('password')
            info = F.login(username, password)
            if info=='usernotexist':
                return render_template('login.html', error='usernotexist', what=[True, False])
            elif info=='wrongpassword':
                return render_template('login.html', error='wrongpassword', what=[True, False])
            else:
                user_id = F.get_id(username)[0]
                if F.get_2auth(user_id)[0]=="None":
                    res=make_response(redirect('/'))
                    res.set_cookie('WOWPOW', E.encrypt(str(F.get_id(username))))
                    return res
                else:
                    return render_template('2auth.html', info=[username, password], what=[True, False])
    else:
        return render_template("login.html", what=[True, False])

@app.route('/login2', methods=['POST'])
def login2_form():
    if request.method == 'POST':
        if request.form.get('sec-password'):
            username = request.form.get('username')
            password = request.form.get('password')
            sec_password = request.form.get('sec-password')
            info = F.login(username, password)
            if info=='usernotexist':
                return render_template('login.html', error='usernotexist', what=[True, False])
            elif info=='wrongpassword':
                return render_template('login.html', error='wrongpassword', what=[True, False])
            else:
                user_id = F.get_id(username)[0]
                if F.get_2auth(user_id)[0]=="None":
                    res=make_response(redirect('/'))
                    res.set_cookie('WOWPOW', E.encrypt(str(F.get_id(username))))
                    return res
                else:
                    id = F.get_id(username)
                    pass2_encrypt = hashlib.sha224(sec_password.encode()).hexdigest()
                    if F.get_2auth(user_id)[0]==pass2_encrypt:
                        res=make_response(redirect('/'))
                        res.set_cookie('WOWPOW', E.encrypt(str(F.get_id(username))))
                        return res
                    else:
                        return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    res = make_response(redirect('/'))
    res.set_cookie('WOWPOW','')
    return res

@app.route('/services')
def services():
    return render_template('service.html', what=[False, True, False])

@app.route('/arduino', methods=['POST', 'GET'])
def arduino():
    return render_template('arduino.html')

app.run(host='0.0.0.0', port=80, debug=True)
