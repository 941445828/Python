import csv
import easygui as g

msg = '生成统计崩溃率SQL'
title = '生成统计崩溃率SQL'
filenames = ['选择你的文件路径']
file_value = g.buttonbox(msg,title,filenames)
file_path = g.fileopenbox(default='*.csv')

csv_list = None
clear_list = None
count = 0
pt = 0
version = None
formatter_dates = None



sql_template = """select to_date(`date`) as dt,'{}' as platform,count(distinct if(event='AppCrashed' and `$app_id`='{}',$device_id,null))/
count(distinct if(event='$AppStart' and `$app_id`='{}',$device_id,null)) * 100 as rate from events where event in ('AppCrashed','$AppStart') 
and `date` = '{}' and `$app_version` in ('{}') group by to_date(`date`) """


# 打开文件读取
def open_csv(file_path):
   with open(file_path, 'r') as f:
        global csv_list
        reader = csv.reader(f)
        csv_list = [row for row in reader]
        return csv_list




#     #判断list里是否有空字符串，如果有就将空字符串删除
def get_clear_list(csv_list):
    global clear_list
    clear_list = [row for row in csv_list if any(row)]
    return clear_list

#     # 读取从项目开始直到最后一行的数据)
def get_version_row(clear_list):
    global last_row
    last_row1 = clear_list[3:]
    last_row = last_row1
    return last_row


#     #读取platform
def get_platfrom(csv_list):
    platfrom = csv_list[2]
    return platfrom


   #  # 读取应用标识
def get_appid(csv_list):
    global appid
    appid_row = csv_list[1]
    return appid_row



    #获取日期列去除年 月 日 然后返回最后的日期
def get_date_list(clear_list):
    global formatter_dates
    formatted_dates = []
    column_data = [row[0] for row in clear_list[2:]]
    column_data1 = column_data[1:]
    for data_str in column_data1:
        date_parts = data_str.split('年')[1].split('月')
        year = data_str.split('年')[0]
        month = date_parts[0].zfill(2)
        day = date_parts[1].split('日')[0].zfill(2)
        formatted_date = '-'.join([year, month, day])
        formatted_dates.append(formatted_date)
    return formatted_dates


def genrate_sql(pt,appid,last_row):
    global statements
    sql_statements = []
    for i, date in enumerate(last_row):
        win_and_mac_sql = sql_template.format(pt[0], appid[0], appid[0], date[0].replace('年', '-').replace('月', '-').replace('日', ''), date[1].replace(',', "','"))
        x64_sql = sql_template.format(pt[1], appid[1], appid[1], date[0].replace('年', '-').replace('月', '-').replace('日', ''), date[2].replace(',',"','"))
        x_sql = sql_template.format(pt[2], appid[2], appid[2], date[0].replace('年', '-').replace('月', '-').replace('日', ''), date[3].replace(',', "','"))
        arm_sql = sql_template.format(pt[3], appid[3], appid[3], date[0].replace('年', '-').replace('月', '-').replace('日', ''), date[4].replace(',', "','"))
        ios_sql = sql_template.format(pt[4], appid[4], appid[4], date[0].replace('年', '-').replace('月', '-').replace('日', ''), date[5].replace(',', "','"))
        android_sql = sql_template.format(pt[5], appid[5], appid[5], date[0].replace('年', '-').replace('月', '-').replace('日', ''), date[6].replace(',', "','"))
        #判定是否是最后一次执行 如果是的话那么在去掉ios_sql后的'\nunion all\n'
        if i == len(last_row) - 1:
            sql_statements.append((win_and_mac_sql, '\nunion all\n', x_sql, '\nunion all\n', x64_sql, '\nunion all\n',
                               android_sql, '\nunion all\n', arm_sql, '\nunion all\n', ios_sql))
        else:
            sql_statements.append((win_and_mac_sql, '\nunion all\n', x_sql, '\nunion all\n', x64_sql, '\nunion all\n',
                               android_sql, '\nunion all\n', arm_sql, '\nunion all\n', ios_sql, '\nunion all\n'))

    statements = '\n'.join(['\n'.join(statement) for statement in sql_statements])
    return statements


csv_list = open_csv(file_path)
pt = get_platfrom(csv_list)
del pt[0]
clear_list = get_clear_list(csv_list)

last_row = get_version_row(clear_list)

appid = get_appid(csv_list)

formatter_dates = get_date_list(clear_list)

del appid[0]

statements = genrate_sql(pt,appid,last_row,)
g.textbox("文件",text = statements,codebox = True)

