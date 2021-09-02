import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

year = '2021'
m = 6

total = pd.DataFrame([])
loc = ['GWA', 'NST_L', 'OLY', 'YSB', 'NST_H', 'SNU']
coldict = {'GWA':'#1f77b4', 'NST_L':'#ff7f0e', 'OLY':'#2ca02c', 'YSB':'#d62728', 'NST_H':'#9467bd', 'SNU':'#8c564b', 'CO2_Avg':'#e377c2'} #plt default color 

i = 0
fpath = '/home/DATA_ARCHIVE/SIHE/level2/' + loc[i] + '/' + year + '/'
fname = loc[i] + '_level2_' + year + str(m).zfill(2) + '.csv'
data = pd.read_csv(fpath + fname, usecols=['Date', 'Hour', 'CO2', 'CO2_Flag'])
data.loc[data['CO2_Flag'] != 'N', 'CO2'] = np.nan
total[loc[i]] = data['CO2']
#print(data.columns) # Index(['Date', 'Hour', 'CO2', 'CO2_Flag', 'CH4', 'CH4_Flag', 'H2O','H2O_Flag']

for i in range(1,3):
    fpath = '/home/DATA_ARCHIVE/SIHE/level2/' + loc[i] + '/' + year + '/'
    fname = loc[i] + '_level2_' + year + str(m).zfill(2) + '.csv'
    data = pd.read_csv(fpath + fname)
    data.loc[data['Flag'] != 'N', 'CO2'] = np.nan
    total[loc[i]] = data['CO2']
    #print(data.columns) # Index(['Date', 'Hour', 'CO2', 'Flag']
    
for i in range(3,6):
    fpath = '/home/DATA_ARCHIVE/SNUCO2M/level2/' + loc[i] + '/'
    fname = loc[i] + '_level2_' + year + str(m).zfill(2) + '.csv'
    data = pd.read_csv(fpath + fname)
    data.loc[data['Flag'] != 0, 'CO2_Avg'] = np.nan
    total[loc[i]] = data['CO2_Avg']
    #print(data.columns) # ['Date', 'Hour', 'CO2_Avg', 'Flag']

total['CO2_Avg'] = total.mean(axis=1, skipna=True)
total['Date'], total['Hour'] = data['Date'], data['Hour']

# ref : https://jinyes-tistory.tistory.com/70 #
from matplotlib import font_manager, rc
font_path = '/home/xodpwkd/anaconda3/lib/python3.7/site-packages/matplotlib/mpl-data/fonts/ttf/NGULIM.TTF'
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

mean = total[['GWA', 'NST_L', 'OLY', 'YSB', 'NST_H', 'SNU', 'CO2_Avg']].mean()
std = total[['GWA', 'NST_L', 'OLY', 'YSB', 'NST_H', 'SNU', 'CO2_Avg']].std()

# plot 1 # 
plt.plot(total.index, total.CO2_Avg)
plt.title('전체 평균 이산화탄소 농도 ' + year +'년 ' + str(m).zfill(2) +'월')
plt.xticks(np.arange(12,732,24), np.arange(1,31,1))
plt.xlabel('일')
plt.ylabel('CO2 (ppm)')
fpath = '/home/xodpwkd/report/202106/'
plt.savefig(fpath + '전체 평균 이산화탄소 농도 ' + year +'년 ' + str(m).zfill(2) +'월')

# plot 2 #
for i in range(0,6):
    plt.scatter(total.index, total[loc[i]], label=loc[i])
plt.legend()
plt.title('시간 평균 이산화탄소 농도 ' + year +'년 ' + str(m).zfill(2) +'월')
plt.xticks(np.arange(12,755,24), np.arange(1,32,1))
plt.xlabel('일')
plt.ylabel('CO2 (ppm)')
fpath = '/home/xodpwkd/report/202106/'
plt.savefig(fpath + '시간 평균 이산화탄소 농도 ' + year +'년 ' + str(m).zfill(2) +'월')

# plot boxplot graph #
total[['GWA', 'NST_L', 'OLY', 'YSB', 'NST_H', 'SNU', 'CO2_Avg']].boxplot()
plt.ylabel('CO2 (ppm)')
plt.title('Boxplot of CO2_202106')
fpath = '/home/xodpwkd/report/202106/'
plt.savefig(fpath + 'Boxplot of CO2_202106')

# plot daily graph #
daily = total.groupby(['Date'], as_index=False).mean()
daily_std = total.groupby(['Date'], as_index=False).apply(lambda x: x.std())
for i in range(0,6):
    plt.plot(daily.index, daily[loc[i]], label=loc[i])
    plt.fill_between(daily.index, daily[loc[i]] - daily_std[loc[i]], daily[loc[i]] + daily_std[loc[i]], alpha=0.2)
plt.legend()
plt.title('Daily mean CO2_' + year + str(m).zfill(2))
plt.xticks(np.arange(0,30,1), np.arange(1,31,1))
plt.xlabel('Date')
plt.ylabel('CO2 (ppm)')
fpath = '/home/xodpwkd/report/202106/'
plt.savefig(fpath + 'Daily mean CO2_' + year + str(m).zfill(2),bbox_inches='tight')
#plt.yticks([420,440,460,480,500,520,540])

# plot daily anomaly graph #
anomaly = total.copy()
loc2 = ['NST_L', 'OLY', 'YSB', 'NST_H', 'SNU']
for name in loc2:
    anomaly[name] = total[name] - total['GWA']
ano_daily = anomaly.groupby(['Date'], as_index=False).mean()
ano_std = anomaly.groupby(['Date'], as_index=False).apply(lambda x: x.std())

for name in loc2:
    plt.plot(ano_daily.index, ano_daily[name], label=name, color = coldict[name])
    plt.fill_between(ano_daily.index, ano_daily[name] - ano_std[name], ano_daily[name] + ano_std[name], alpha=0.2, color = coldict[name])
plt.margins(x=0)
plt.legend()
plt.title('Anomaly of CO2_' + year + str(m).zfill(2))
plt.xticks(np.arange(0,30,1), np.arange(1,31,1))
plt.xlabel('Date')
plt.ylabel('CO2 (ppm)')
fpath = '/home/xodpwkd/report/202106/'
plt.savefig(fpath + 'Anomaly of CO2_' + year + str(m).zfill(2),bbox_inches='tight')


### plot weekdays ###
days = ['월','화','수','목','금','토','일']
daily['datetime'] = pd.to_datetime(daily.Date + '-00-00-00')
daily['day'] = 0
for i in range(30):
    daily.loc[i, 'day'] = days[daily.loc[i,'datetime'].weekday()]
weekdays = daily.groupby(['day'], as_index=False).mean()
weekdays_array = pd.DataFrame([])

for day in days:
    weekday = weekdays[weekdays.day == day]
    weekdays_array = weekdays_array.append(weekday)
weekdays = weekdays_array.reset_index(drop=True)

loc2 = ['NST_L', 'OLY', 'YSB', 'NST_H', 'SNU']
for name in loc:
    plt.plot(weekdays.day, weekdays[name], label=name, marker='o', color = coldict[name])
plt.legend(loc='upper right')
plt.title('요일별 CO2 농도_202106')
plt.ylabel('CO2 (ppm)')
fpath = '/home/xodpwkd/report/202106/'
plt.savefig(fpath + '요일별 CO2 농도_202106')

###
days = ['월','화','수','목','금','토','일']
ano_daily['datetime'] = pd.to_datetime(ano_daily.Date + '-00-00-00')
ano_daily['day'] = 0
for i in range(30):
    ano_daily.loc[i, 'day'] = days[ano_daily.loc[i,'datetime'].weekday()]
weekdays = ano_daily.groupby(['day'], as_index=False).mean()
weekdays_array = pd.DataFrame([])

for day in days:
    weekday = weekdays[weekdays.day == day]
    weekdays_array = weekdays_array.append(weekday)
weekdays = weekdays_array.reset_index(drop=True)
weekdays_std = ano_daily.groupby(['day'], as_index=False).apply(lambda x: x.std())

loc2 = ['NST_L', 'OLY', 'YSB', 'NST_H', 'SNU']
for name in loc2 :
    plt.plot(weekdays.day, weekdays[name], marker='o', label=name, color = coldict[name])
    #plt.fill_between(weekdays.day, weekdays[name] - weekdays_std[name], weekdays[name] + weekdays_std[name], alpha=0.2, color = coldict[name])
plt.legend(loc='upper right')
plt.title('요일별 CO2 농도 차이_202106')
plt.ylabel('CO2 (ppm)')
fpath = '/home/xodpwkd/report/202106/'
plt.savefig(fpath + '요일별 CO2 농도 차이_202106')

### Diurnal graph ###
diurnal = total.groupby(['Hour'], as_index=False).mean()
for i in range(0,6):
    plt.plot(diurnal.Hour, diurnal[loc[i]], label=loc[i])
plt.legend(loc='upper right')
plt.title('시간별 이산화탄소 농도_202106')
plt.ylabel('CO2 (ppm)')
plt.xticks(np.arange(0,24,1))
plt.xlabel('시간')
fpath = '/home/xodpwkd/report/202106/'
plt.savefig(fpath + '시간별 이산화탄소 농도_202106')
