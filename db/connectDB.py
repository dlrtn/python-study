import pymysql
import pandas as pd

mydb = pymysql.connect(
    host = "indj-database2.cw7ggpqhhqne.ap-northeast-2.rds.amazonaws.com",
    user = "admin",
    passwd = "indj2020#",
    database = "indj_ai"
)
cnt = 0

mc = mydb.cursor()

for i in range(len(data)):
    # sql = "select * from OM_Artist as oa where oa.ARTIST_NAME = \"{}\"".format(data.iloc[i]['아티스트 이름'])
    sql = """
            update OM_Artist AS oa  
            SET ENG_TO_KOR_NAME = \"{}\"
            WHERE oa.ARTIST_NAME = \"{}\"
            """.format(data.iloc[i]['검수 후'], data.iloc[i]['아티스트 이름'])
    mc.execute(sql)
    result = mc.fetchall()
    mydb.commit()

    cnt += 1