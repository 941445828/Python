import csv
import easygui as g

msg = '生成统计崩溃率SQL'
title = '生成统计崩溃率SQL'
filenames = ['选择你的文件路径']
file_value = g.buttonbox(msg,title,filenames)
file_path = g.fileopenbox(default='*.csv')

# 打开文件读取测试
with open(file_path, 'r') as f:
    reader = csv.reader(f)
    csv_list = [row for row in reader]

    #判断list里是否有空字符串，如果有就将空字符串删除
    clear_csv_list = [row for row in csv_list if any(row)]

    # 读取最后一行（最新的版本号)
    last_row = clear_csv_list[-1]

    # 读取项目
    platform = csv_list[2]

    # 读取应用标识
    appid_row = csv_list[1]

    # 删除 应用标识的 appid和项目的 日期
    del appid_row[0]
    del platform[0]

    # 判断appversion中的元素是否有, 如果就就将其分割成元祖
    appversion = [tuple(x.split(',')) if ',' in x else x for x in last_row]


   # 对列表appversion中的每个元素进行处理，如果元素是字符串类型，则将其中的\n替换为空字符串，
   # 否则将元组中的每个元素进行相同的替换操作，并返回一个新的列表new_appversion。
   # 然后，对于new_appversion中的每个元素，如果它是字符串类型，则将其保留不变，否则将元组中的每个元素用','连接起来，并用单引号包裹，
   # 返回一个新的列表new_list。这个操作可能是将元组转换为字符串的目的。
    new_appversion = [x.replace('\n', '') if isinstance(x, str) else tuple(item.replace('\n', '') for item in x) for x in appversion]
    new_list = [x if isinstance(x, str) else "','".join(x) for x in new_appversion]


    # 格式化日期
    date_parts = last_row[0].split('年')[1].split('月')
    year = last_row[0].split('年')[0]
    month = date_parts[0].zfill(2)
    day = date_parts[1].split('日')[0].zfill(2)
    formatted_date = '-'.join([year, month, day])

    # 目标sql
    sql_template = """select to_date(`date`) as dt,'{}' as platform,count(distinct if(event='AppCrashed' and `$app_id`='{}',uuid,null))/count(distinct if(event='$AppStart' and `$app_id`='{}',uuid,null)) * 100 as rate from events where event in ('AppCrashed','$AppStart') and `date` = '{}' and `$app_version` in ('{}') group by to_date(`date`) """

    # 生成不同项目下的sql123123123
    win_and_mac_sql = sql_template.format(platform[0], appid_row[0], appid_row[0], formatted_date, new_list[1]).replace('uuid','$device_id')
    x64_sql = sql_template.format(platform[1], appid_row[1], appid_row[1], formatted_date, new_list[2]).replace('uuid','$device_id')
    x_sql = sql_template.format(platform[2], appid_row[2], appid_row[2], formatted_date, new_list[3]).replace('uuid','$device_id')
    arm_sql = sql_template.format(platform[3], appid_row[3], appid_row[3], formatted_date, new_list[4]).replace('uuid','$device_id')
    ios_sql = sql_template.format(platform[4], appid_row[4], appid_row[4], formatted_date, new_list[5]).replace('uuid','$device_id')
    android_sql = sql_template.format(platform[5], appid_row[5], appid_row[5], formatted_date, new_list[6]).replace('uuid','$device_id')

    # 对最终sql拼装，并格式化下
    sql = " \n\n union all \n\n".join([win_and_mac_sql , x64_sql , x_sql, arm_sql, ios_sql, android_sql])

    #将结果回调
    g.textbox("文件",text = sql,codebox = True)
