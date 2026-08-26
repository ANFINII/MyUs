import os
import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd


# DB情報の設定
con = mysql.connector.connect(
    host = os.environ["MYSQL_HOST"],
    port = int(os.environ["MYSQL_PORT"]),
    user = os.environ["MYSQL_USER"],
    password = os.environ["MYSQL_PASSWORD"],
    database = os.environ["MYSQL_DATABASE"],
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
