# BBS_tkotake
練習のために作成した、簡易掲示板サイトです。

管理者ログイン機能の作成途中のコードが、
コメントアウトしてあります。

環境
Ubuntu    20.04
Apache2   8.0.20
MySQL     2.2.41
Python3   3.8.2


CGIを有効化する
```
$ a2enmod cgi
```

Pythonパッケージインストールと保存先の指定
```
$ python3 -m pip install mysqlclient textwrap3 --target ~/my-space
```

