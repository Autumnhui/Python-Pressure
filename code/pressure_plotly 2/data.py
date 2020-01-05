

import pandas as pd
#py.offline.init_notebook_mode()
# 数据整理
pressure_measure = pd.read_csv("./mental.csv",encoding='gbk')
pressure = pd.read_csv('./mental_health_poll_updated.csv',encoding='gbk').dropna().set_index('问题')

## 扇形图下拉框点击选项
element1 = list(set(pressure.index))

## 扇形图数据整理

pressure1 = pressure[~pressure['洲'].str.contains('(not set)')]
pressure2 = pressure1[~pressure1['城市'].str.contains('(not set)')]
most = pressure2.loc['最让您感到压力的是什么？']

## 地图
jinwei = pd.read_excel('./jinweidu.xlsx')

pressure_jinwei = pressure_measure.merge(jinwei,left_on='洲',right_on='Region').drop('Region',axis=1)

压力较小=pressure_jinwei[(pressure_jinwei["压力程度"]>0)&(pressure_jinwei["压力程度"]<=25)]
压力一般=pressure_jinwei[(pressure_jinwei["压力程度"]>25)&(pressure_jinwei["压力程度"]<=50)]
压力较大=pressure_jinwei[(pressure_jinwei["压力程度"]>50)&(pressure_jinwei["压力程度"]<=70)]
压力很大=pressure_jinwei[(pressure_jinwei["压力程度"]>70)&(pressure_jinwei["压力程度"]<=100)]

element3=['压力较小','压力一般','压力较大','压力很大']




## 得出最有可能导致压力的6个因素
element = list(set(most['分类']))
combin_most = pd.pivot_table(most,index=['洲','分类'],values=['分类'],aggfunc='count').rename(columns = {'城市':'数量'})
list1 = list(combin_most['数量'])
most_count = list((most.groupby(['洲'])['分类'].count()))
list2 = []
for i in range(len(most_count)):
    list2.append(most_count[i])
    list2.append(most_count[i])
    list2.append(most_count[i])
    list2.append(most_count[i])
    list2.append(most_count[i])
    list2.append(most_count[i])
combin_most['百分比'] = [a/b for a,b in zip(list1,list2)]
pressure_mostpre = pressure_measure.merge(combin_most.unstack()['百分比'],left_on='洲',right_on='洲').drop(['一直','从不','很少','有时'],axis=1).set_index('洲')

##折线图

do = pressure2.loc['在压力大时你最想做什么']
combin_do = pd.pivot_table(do,index=['洲','分类'],values=['分类'],aggfunc='count').rename(columns = {'城市':'num'})
list3 = list(combin_do['num'])
num_count = list((do.groupby(['洲'])['分类'].count()))
list4=[]
for i in range(len(num_count)):
    list4.append(num_count[i])
    list4.append(num_count[i])
    list4.append(num_count[i])
    list4.append(num_count[i])
    list4.append(num_count[i])
    list4.append(num_count[i])
# print(list4)
combin_do['占比'] = [a/b for a,b in zip(list3,list4)]
combin_do = combin_do.drop('num',axis=1)
combin_do = combin_do.reset_index()
