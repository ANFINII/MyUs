import pandas as pd
import pandas.io.sql as psql
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import mysql.connector

from sklearn import datasets, svm
from django.db import connections
from urllib.parse import urlparse
from pprint import pprint

# DB情報の設定
url = urlparse("mysql://anfinii:A5656gu3y!@127.0.0.1:3306/myus_db")
con = mysql.connector.connect(
    host = url.hostname,
    port = url.port,
    user = url.username,
    password = url.password,
    database = url.path[1:],
)
cur = con.cursor()


# form で送られた情報を変数に入れるようにする
table_name = "myusapp_videomodel"

cur.execute("SELECT * FROM " + table_name)
column_list = [column[0] for column in cur.description]
tag_list = cur.fetchall()
tag_df = pd.DataFrame(tag_list, columns=column_list)

# pprint(tag_df)
tag_df.plot(kind="bar", x="created", y="read")
plt.show()

# データベースへコミット。これで変更が反映される。
con.commit()
con.close()
