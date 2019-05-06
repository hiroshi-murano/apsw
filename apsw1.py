import apsw
import json
from pprint import pprint
import random
import datetime


# DB_FILE='db_apsw.sqlite3'
DB_NAME = 'example3.sqlite3'


def create_table():
    """
    tableを作成する
    """

    sql = """
        create table tbl1(
            id int not null primary key,
            name text,
            age int,
            weight real,
            json json
        )
    """

    connection = apsw.Connection(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(sql)


def insert_data():
    """
    データを一件、挿入する
    """

    dctData = {}
    dctData['名前'] = '斉藤'
    dctData['年齢'] = 25
    dctData['体重'] = 54.3
    dctData['入社日'] = '1995-09-15'
    json_text = json.dumps(dctData, ensure_ascii=False)

    connection = apsw.Connection(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("insert into tbl1 values(?,?,?,?,?)",
                   (2, '鹿児島', 23, 54.3, json_text))


def insert_data_mary():
    """
    データを配列でまとめて、挿入する
    """

    dctData = {}
    dctData['名前'] = '斉藤'
    dctData['年齢'] = 25
    dctData['体重'] = 54.3
    dctData['入社日'] = '1995-09-15'
    json_text = json.dumps(dctData, ensure_ascii=False)

    lstData = [
        [3, '東京', 23, 44.3, json_text],
        [4, '大阪', 53, 64.3, json_text],
        [5, '福岡', 63, 74.3, json_text],
    ]

    connection = apsw.Connection(DB_NAME)
    cursor = connection.cursor()
    cursor.executemany("insert into tbl1 values(?,?,?,?,?)", lstData)


def insert_dict():
    """
    辞書を一件、挿入する
    """

    dctData = {}
    dctData['名前'] = '斉藤'
    dctData['年齢'] = 25
    dctData['体重'] = 54.3
    dctData['入社日'] = '1995-09-15'
    json_text = json.dumps(dctData, ensure_ascii=False)

    dctTemp = {}
    dctTemp['id'] = 6
    dctTemp['name'] = '北九州市'
    dctTemp['age'] = 21
    dctTemp['weight'] = 53.9
    dctTemp['json'] = json_text

    connection = apsw.Connection(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(
        "insert into tbl1 values(:id, :name, :age, :weight, :json)", dctTemp)


def insert_dict_mary():
    """
    辞書を配列でまとめて、挿入する
    """

    base_date = datetime.date(2017, 11, 12)

    lstData = []
    for cnt in range(0, 100):

        day = base_date + datetime.timedelta(days=random.randint(0, 1000))

        # print(day)

        dctData = {}
        dctData['名前'] = '斉藤'
        dctData['年齢'] = random.randint(10, 99)
        dctData['体重'] = round(random.random()*100, 1)
        dctData['入社日'] = day.strftime("%Y-%m-%d")
        json_text = json.dumps(dctData, ensure_ascii=False)

        dctTemp = {}
        dctTemp['id'] = cnt
        dctTemp['name'] = '名前{}'.format(cnt)
        dctTemp['age'] = random.randint(10, 99)
        dctTemp['weight'] = round(random.random()*100, 1)
        dctTemp['json'] = json_text
        lstData.append(dctTemp)

    connection = apsw.Connection(DB_NAME)
    cursor = connection.cursor()
    cursor.executemany(
        "insert into tbl1 values(:id, :name, :age, :weight, :json)", lstData)


def select_rows():
    """
    データ select
    """

    connection = apsw.Connection(DB_NAME)
    cursor = connection.cursor()
    cmd = "SELECT * FROM tbl1 WHERE age>50 "

    for row in cursor.execute(cmd):
        pprint(row)


def select_rows_json():
    """
    データ select (json内の特定keyで検索)
    """

    connection = apsw.Connection(DB_NAME)
    cursor = connection.cursor()
    # cmd = "SELECT * FROM tbl1 WHERE json_extract(tbl1.json, '$.名前') like '斉藤%' "
    # cmd = "SELECT * FROM tbl1 WHERE json_extract(tbl1.json, '$.年齢')>50 "
    cmd = ("SELECT * FROM tbl1 WHERE"
           " json_extract(tbl1.json, '$.入社日')>'2020-01-01' ")

    for row in cursor.execute(cmd):
        json_text = row[4]
        dctData = json.loads(json_text)  # jsonを辞書に変換
        pprint(dctData)


if __name__ == '__main__':

    a = [3, 4, 5, 5]
    # base_date=datetime.date(2017, 11, 12)
    # for cnt in range(70,80):
    #     day=base_date + datetime.timedelta(days=random.randint(0,1000))
    #     print(base_date)
    #     print(day)

    # sys.exit()

    # select_data()

    # create_table()
    # insert_data()
    # insert_data_mary()
    # insert_dict()

    # insert_dict_mary()
    select_rows_json()
