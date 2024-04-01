import math
import time
from datetime import datetime
import os
import pandas as pd
from openpyxl.chart import (
    LineChart,
    Reference,
)
from rich.pretty import pprint

def number_to_letters(number):
    if number <= 0:
        return ""

    result = ""
    while number > 0:
        remainder = (number - 1) % 26
        result = chr(ord('A') + remainder) + result
        number = (number - 1) // 26

    return result

def get_human_datetime():
    now = datetime.now()
    formatted_datetime = now.strftime("%d %B %Y, %I:%M:%S %p")
    return formatted_datetime

def get_datetime():
    return time.strftime("%Y-%m-%d %H_%M_%S")

def get_datetime_n_sec():
    return time.strftime("%Y-%m-%d %H_%M")

def get_date_n_time():
    return time.strftime("%Y-%m-%d")
def get_time_n_date():
    return time.strftime("%H_%M")

def create_excel(file_path, data_dict, total_round, chart_config):
    sheet_name = get_datetime()
    df = pd.DataFrame(data_dict)
    if os.path.exists(file_path):
        writer = pd.ExcelWriter(file_path, engine='openpyxl', mode='a')
    else:
        writer = pd.ExcelWriter(file_path, engine='openpyxl')
    df.to_excel(writer, sheet_name=sheet_name)

    workbook  = writer.book
    worksheet = writer.sheets[sheet_name]

    chart_cnt = math.ceil(len(data_dict) / 10)

    for chart_num in range(chart_cnt):
        if (chart_num == chart_cnt - 1) and (len(data_dict) % 10 != 0):
            data_point = len(data_dict) % 10 - 1
        else:
            data_point = 10

        # Create a chart
        if data_point <= 0:
            continue

        chart = LineChart()
        chart.title = f"{chart_config['title']} {chart_num}"
        chart.x_axis.title = chart_config['x_axis']
        chart.y_axis.title = chart_config['y_axis']
        chart.style = 10

        for data_num in range(data_point):
            series = Reference(
                worksheet,
                min_col=(chart_num * 10) + data_num + 3,
                min_row=1,
                max_row=total_round + 1,
            )
            chart.add_data(series, titles_from_data=True)

        chart_location = f"{number_to_letters((chart_num * 10) + 1)}{total_round + 3}"
        worksheet.add_chart(chart, chart_location)
        workbook.save(file_path)
    writer.close()

def format_data_to_excel(data_dict, timestamp):
    # Get all model id
    model_ids = []
    for address in data_dict.keys():
        model_id = data_dict[address]["model_id"]
        if model_id not in model_ids:
            model_ids.append(model_id)
    # Create dict from each model id

    sensors_group = {}
    for model_id in model_ids:
        sensors_group[model_id] = {}
        sensors_group[model_id]['timestamp'] = timestamp
        

    for address in data_dict.keys():
        model_id = data_dict[address]["model_id"]
        sensors_group[model_id][address] = data_dict[address]['data']

    return sensors_group
