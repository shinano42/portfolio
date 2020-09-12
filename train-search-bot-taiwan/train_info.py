import requests
from requests.auth import HTTPBasicAuth
import json
from pprint import pprint 


def format_response_lb(data):
    result = []
    for i in range(len(data)):
        emt = 'No. {train_no}--{endsta}--{departure_time}--{train_type}'.format(train_no=data[i]['TrainNo'], endsta=data[i]['EndingStation']['Zh_tw'], departure_time=data[i]['ScheduledDepartureTime'][:5], train_type=data[i]['TrainTypeName']['Zh_tw'][:2])
        result.append(emt)
    return result
def format_response_tt(data):
    result = []
    for i in range(len(data)):
        emt = 'No. {train_no}--{endsta}--{departure_time}--{train_type}'.format(train_no=data[i]['DailyTrainInfo']['TrainNo'], endsta=data[i]['DailyTrainInfo']['EndingStationName']['Zh_tw'], departure_time=data[i]['OriginStopTime']['DepartureTime'][:5], train_type=data[i]['DailyTrainInfo']['TrainTypeName']['Zh_tw'][:2])
        result.append(emt)
    return result


def match_n_or_s(direction):
    if direction == 's':
        result = 1
    elif direction == 'n':
        result = 0
    else:
        result = -1
    return result
    
def filter_n_or_s(direction):
    def make_filter(x):
        if x['Direction'] == direction:
            return True
        else:
            return False
    return make_filter

def get_stations_data():
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#     res = requests.get('https://raw.githubusercontent.com/banqhsia/TRA-Info/master/static/stations.json', headers=headers)
#     stations_data = res.json()
    with open('stations.json', encoding="UTF-8") as f:
        stations_data = json.load(f)
    return stations_data

def get_index(str_to_encode, mapping_data):
    index = -1
    for i in range(len(mapping_data)):
        if(mapping_data[i]['Station_Name'] == str_to_encode):
            index = i
    return index


def get_live_boardingTrain(station_code):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    res = requests.get('https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/LiveBoard/Station/{}?$format=JSON'.format(station_code), headers=headers)
    data = res.json()
    result = []
    for i in range(len(data)):
        tmp = {'TrainNo': data[i]['TrainNo'], 'EndingStation': data[i]['EndingStationName'],'Direction': data[i]['Direction'], 'ScheduledDepartureTime': data[i]['ScheduledDepartureTime'], 'TrainTypeName': data[i]['TrainTypeName']}
        result.append(tmp)
    return result


def get_timetable_all_day(fromWhere, toWhere, date):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    res = requests.get('https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/DailyTimetable/OD/{fromWhere}/to/{toWhere}/{date}?$orderby=OriginStopTime%2FArrivalTime%20asc&$format=JSON'.format(fromWhere=fromWhere, toWhere=toWhere, date=date), headers=headers)
    return res.json()

def get_timetable_present_time(fromWhere, toWhere, date, presentTime):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    res = requests.get('https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/DailyTimetable/OD/{fromWhere}/to/{toWhere}/{date}?$filter=OriginStopTime/DepartureTime gt \'{presentTime}\'&$orderby=OriginStopTime/DepartureTime asc&$top=4&$format=JSON'.format(fromWhere=fromWhere, toWhere=toWhere, date=date, presentTime=presentTime), headers=headers)
    return res.json()