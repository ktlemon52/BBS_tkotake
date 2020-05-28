#!/usr/bin/python3

#コメントアウトしているコードは、管理者ログイン機能を実装しようとして
#、実装しきれなかったものです。

import io
import sys

sys.path.append('../my-space')

import MySQLdb
import cgi
import cgitb
import datetime
import textwrap


global method, view_name, bbs_message, id
# フォームの値の受け取り
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
form  = cgi.FieldStorage(keep_blank_values = True)
method = form.getvalue('method', '')
view_name = form.getvalue('view_name', '')
bbs_message = form.getvalue('bbs_message', '')
adminname = form.getvalue('adminname')
password = form.getvalue('password')
loginFlg = form.getvalue('loginFlg')

#メッセージ表示機能(メッセージボード）
def posts():
        cur= con.cursor()
        sql = "select * from bbs_info order by date desc"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            post_text=("""
            <div id='bbs_main'>
               <a id='bbs_name'>{name}</a> 
               <a id='bbs_date'> [{date}]</a> 
               <p id='bbs_text'>{message}</p>
                """).format(
                        id = row[0],
                        message = row[1],
                        name = row[2],
                        date = row[3]
            )
            print(post_text)
#            if(loginFlg == 1):
            source = textwrap.dedent("""
                    <form id = 'bbs_form' method="post" action="" />
                    <input type="hidden" name="method" value="delete" />
                    <input type="hidden" name="id" value={id} />
                    <input id='delete_button' type="submit"  value="削除" />
                    </form>
                    """).format(id = row[0])
            print(source)
            print("""</div>""")
# 削除機能
def delete():
            id = form['id'].value
            sql = 'delete from bbs_info where id = %s'
            cur.execute(sql, (id,))
            con.commit()
# BDデータ登録機能
def register():
            view_name = form['view_name'].value
            message = form['bbs_message'].value
            sql = "insert into bbs_info(message, name) values (%s, %s)"
            cur.execute(sql, (message, view_name))
            con.commit()
#ログイン機能
#def login():
#        adminname = form['adminname'].value
#        password = form['password'].value
#        sql = "select * from admin where adminname=%s and password=%s"
#        try:
#            cur.execute(sql, (adminname, password))
#            rows = cur.fetchall()
#            for row in rows:
#                    adminname = row['adminname']
#                    password = row['password']
#        except mysql.connector.Error as err:
#                    print('いろいろ間違っています')
#        if(not adminname == "" and not password == ""):
#                sql = "update admin set loginFlg = 1 where adminname=%s and password=%s"
#                cur.execute(sql, (adminname, password))
#                con.commit();
#                global loginFlg
#                loginFlg = row['loginFlg']
#ログアウト機能
#def logout():
#                sql = "update admin set loginFlg = 0 where loginFlg=1"
#                cur.execute(sql)
#                con.commit();

#メインHTML表示
def header():
        print("Content-Type: text/html; charset=utf-8\n")

def main_html():
            source = textwrap.dedent("""
            <html lang="ja">
            <head>
               <title>ひと言掲示板</title>
               <link rel="stylesheet" href="style.css">
               <meta http-equiv=\"Content-Type\" content=\ 
               "text/htmlcharset=UTF-8\" / >
            </head>

              <div id='header_container'>
                <h1 id='header_title'>ひと言掲示板</h1>
                <p id='header_text'>なんでも自由に書き込んでください</p> 
              <div>

              <div id='content_container'>
                <div >
                  <form action=""  method="post">
                    <input type="hidden" name="method" value="post">
                    <label class='input_text'>表示名</label>
                    <input id="view_name" type="text" 
                        name="view_name" value=""
                        place_holder="名前"/>
                </div>
                <div>
                    <label class="input_text">ひと言メッセージ</label>
                    <textarea rows="5" cols="50"  
                    id='bbs_message' name="bbs_message" 
                    placeholder="メッセージ"></textarea>
                </div>
                <input id='register_button' 
                    type="submit" name="btn_submit" value="書き込む" />
               </form>
              </div>
            """)
            print(source)

#ログインフォーム表示機能
#def login_form():
#                source = textwrap.dedent("""
#                <form method="post" action="">
#                    <div>
#                    <input type="hidden" name="method" value="login" />
#                    <div>
#                        <label>ユーザー名</label><input type="text" name="adminname" value="" />
#                    </div>
#                    <div>
#                        <label>パスワード</label><input type="password" name="password" value="" />
#                    </div>
#                    <input type="submit" value="ログイン" />
#                    </div>
#                </form>
#                """)
#                print(source)

#def logout_button():
#                source = textwrap.dedent("""
#                <form method="post" action="">
#                <input type="hidden" name="method" value="logout" />
#                <input type="submit" value="ログアウト" />
#                </form>
#                """)
#                print(source)


#DB接続の分岐機能
def db_conection():
            method = form.getvalue('method')
            if(method == 'post' and not view_name == "" and not bbs_message == ""):
                register()
                redirect()
            elif(method == 'post' and (view_name == "" or bbs_message == "")):
                print("""
                <p id='error_message'>
                表示名かメッセージが入力されていません</p>
                """)
            elif(method == 'delete'):
                delete()
 #           elif(method == 'login'):
 #               login()
 #               redirect()
 #           elif(method == 'logout'):
 #               logout()

#投稿後のページリフレッシュ機能
def redirect():
            source = textwrap.dedent( '''
            <html>
                <head>
                    <meta http-equiv="refresh" content=0; url=./test.py">
                </head>
                <body>
                    メッセージの登録に成功しました。
                </body>
            </html>
            ''' )
            print(source)

#メイン
def main():
        header()
        global con, cur, loginFlg
        loginFlg = 0
        con = MySQLdb.connect(
            user='test',
            passwd='test',
            host='127.0.0.1',
            db='bbs_db',
            charset="utf8")
        cur = con.cursor(MySQLdb.cursors.DictCursor)
        db_conection()
#        if(loginFlg == 0):
#            login_form()
#        elif(loginFlg == 1):
#            logout_button()
#        print(loginFlg)
        main_html()
        posts()

if __name__ == "__main__":
    main()


