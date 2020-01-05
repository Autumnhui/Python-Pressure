from flask import Flask, render_template, request
import pandas as pd
import cufflinks as cf
import plotly as py
import plotly.graph_objs as go
import plotly.express as px
import os


app = Flask(__name__)
path_file = os.path.dirname(__file__)
path_file_abs = os.path.dirname(os.path.abspath(__file__))
path_cwd_pre = os.getcwd()
path_cwd_post = os.getcwd()
os.chdir(path_cwd_post)

## 数据整理
pressure_measure = pd.read_csv("./pressure_plotly/mental.csv",encoding='gbk')
pressure = pd.read_csv('./pressure_plotly/mental_health_poll_updated.csv',encoding='gbk').dropna().set_index('问题')

## 扇形图下拉框点击选项
element1 = list(set(pressure.index))

## 扇形图数据整理

pressure1 = pressure[~pressure['洲'].str.contains('(not set)')]
pressure2 = pressure1[~pressure1['城市'].str.contains('(not set)')]
most = pressure2.loc['最让您感到压力的是什么？']

## 地图
jinwei = pd.read_excel('./pressure_plotly/jinweidu.xlsx')

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
print(list4)
combin_do['占比'] = [a/b for a,b in zip(list3,list4)]
combin_do = combin_do.drop('num',axis=1)
combin_do = combin_do.reset_index()




app = Flask(__name__)

## first page
@app.route('/',methods = ['GET'])
## 在只有get没有post，点击"Do it"之后为404
def pressure_most():
    title1 = "您多久受到一次压力？"
    ## 扇形图分析
    ### 表格呈现数据
    data_pie =  pd.DataFrame(pressure2.loc['您多久受到一次压力？']['分类'].value_counts())
    ## 呈现问题表格
    data_pie1 = data_pie.T.to_html()
    pie1_list = [num for num in data_pie['分类']]
    labels = [index for index in data_pie.index]
    ### 设置扇形图下拉框
    element1_available = element1
    ### 绘制扇形图
    fig1 = {
  "data": [
    {
      "values": pie1_list,
      "labels": labels,
      "domain": {"x": [0, .5]},
      "name": '您多久受到一次压力？',
      "hoverinfo":"label+percent+name",
      "hole": .5, ## 同心圆宽度
      "type": "pie",

    },],
  "layout": {
        'title':{
        'text':'您多久受到一次压力？' ,
        'y':0.9,
        'x':0.5,
        'font':{'family':'SimHei', 'size':25},
            'xanchor': 'center',
            'yanchor': 'top'},
        'margin':{'l':60,'r':60,'b':50,'t':100,'pad':0},
        'paper_bgcolor':'rgba(0,0,0,0)',
        "annotations": [
            { "font": { "size": 20},
              "showarrow": False,
              "text": "",
                "x": 0.20,
                "y": 1
            },
        ]
    }
}
    py.offline.plot(fig1, filename="example1.html",auto_open=False)
    with open('example1.html',encoding='utf8',mode='r') as f:
        plot_all1 =''.join(f.readlines())



    title3 = "压力等级分布"
    consult3 = '压力大小计算：利用压力频率，将“一直”设置为0.6、“有时候”设置为0.2、“很少”设置为0.15、“从不”设置为0.05算权重。将压力等级分为四个等级，下面是每个等级分布的地区。'
    element3_available =element3
    fig3 = go.Figure(data=go.Choropleth(
        locations=pressure_jinwei['代码'],
        z=pressure_jinwei['压力程度'].astype(float),
        locationmode='USA-states',
        colorscale='purpor',
        autocolorscale=False, # hover text
        marker_line_color='white', # line markers between states
        colorbar_title="压力等级",
        hovertext=pressure_jinwei['洲']
    ))

    fig3.update_layout(
         title={
        'text':'各地区压力等级' ,
        'y':0.9,
        'x':0.5,
        'font':{'family':'SimHei', 'size':25},
             'xanchor': 'center',
             'yanchor': 'top'},
        geo = dict(
            scope='usa',
            projection=go.layout.geo.Projection(type = 'albers usa'),
            showlakes=True, # lakes
            lakecolor='rgb(255, 255, 255)'),
    )
    py.offline.plot(fig3, filename="example3.html",auto_open=False)
    with open('example3.html',encoding='utf8',mode='r') as f:
        plot_all3 =''.join(f.readlines())


    element_available = element
    title2 ='压力等级与不同角色施加压力的关系'
    fig = px.scatter(pressure_mostpre,x='压力程度',y='父母',marginal_x='histogram' ,marginal_y='histogram',trendline="ols",template="plotly",
                     )
    fig.update_layout(
         title={
        'text':'压力等级与父母施加压力的关系',
        'y':0.9,
        'x':0.5,
        'font':{'family':'SimHei', 'size':25},


       'xanchor': 'center',
        'yanchor': 'top'},
        margin=go.Margin(l=60,r=60,b=50,t=100,pad=0),


    )
    py.offline.plot(fig, filename="example.html",auto_open=False)
    with open('example.html',encoding='utf8',mode='r') as f:
        plot_all =''.join(f.readlines())

    ## 折线
    title4 = '在压力大时您最想做什么?'
    fig4 = px.line(combin_do, x="洲", y="占比", animation_frame="分类",
            hover_name="占比",range_y =[0,0.5]
            )
    fig4.update_layout(
        title={
        'text':'各地区减轻压力方式' ,
        'y':0.9,
        'x':0.5,
        'font':{'family':'SimHei', 'size':25},
        'xanchor': 'center',
        'yanchor': 'top'},


        margin=go.Margin(l=60,r=60,b=50,t=100,pad=0))
    py.offline.plot(fig4, filename="example4.html",auto_open=False)
    with open('example4.html',encoding='utf8',mode='r') as f:
        plot_all4 =''.join(f.readlines())
    return render_template('first.html',
                           the_title1 = title1,
                           the_title2 = title2,
                           the_plot_all1 = plot_all1,
                           the_data_pie1 = data_pie1,
                           the_consult3 = consult3,
                           the_plot_all3 = plot_all3,
                          the_select_element3 = element3_available,
                          the_title3=title3,
                          the_select_element1 = element1_available,
                          the_select_element = element_available,
                          the_plot_all = plot_all,
                           the_title4 = title4,
                           the_plot_all4 = plot_all4
                          )




@app.route('/first',methods=['POST'])
def most_cor():

    ## 筛选扇形图
    the_element1 = request.form['the_element1_selected']
    print(the_element1)
    element1_available = element1
    ## 表格
    data_pie =  pd.DataFrame(pressure2.loc[the_element1]['分类'].value_counts())
    ## 转置，呈现表格
    data_pie1 = data_pie.T.to_html()
    ## 标题
    title1 = the_element1
    ## 扇形图要素
    pie1_list = [num for num in data_pie['分类']]
    labels = [index for index in data_pie.index]
    ## 绘制扇形图
    fig1 = {
  "data": [
    {
      "values": pie1_list,
      "labels": labels,
      "domain": {"x": [0, .5]},
      "name":the_element1 ,
      "hoverinfo":"label+percent+name",
      "hole": .5, ## 同心圆宽度
      "type": "pie",

    },],
  "layout": {
         'title':{
        'text':the_element1 ,
        'y':0.9,
        'x':0.5,
        'font':{'family':'SimHei', 'size':25},
        'xanchor': 'center',
        'yanchor': 'top'},

        'paper_bgcolor':'rgba(0,0,0,0)',

        "annotations": [
            { "font": { "size": 20},
              "showarrow": False,
              "text": '',
                "x": 0.20,
                "y": 1
            },
        ]
    }
}
    py.offline.plot(fig1, filename="example1.html",auto_open=False)
    with open('example1.html',encoding='utf8',mode='r') as f:
        plot_all1 =''.join(f.readlines())

   ## 图表2
    the_element3 = request.form['the_element3_selected']
    print(the_element3)
    element3_available = element3
    if the_element3 =='压力较小':
        the_level = 压力较小
    elif the_element3 =='压力一般':
        the_level = 压力一般
    elif the_element3 =='压力较大':
        the_level = 压力较大
    else:
        the_level = 压力很大

    fig3 = go.Figure(data=go.Choropleth(
        locations=the_level['代码'],
        z=the_level['压力程度'].astype(float),
        locationmode='USA-states',
        colorscale='purpor',
        autocolorscale=False, # hover text
        marker_line_color='white', # line markers between states
        colorbar_title="压力等级",
        zmin=0,
        zmax=100,
        hovertext=the_level['洲']
    ))

    fig3.update_layout(
        title={
        'text':'各地区压力等级' ,
        'y':0.9,
        'x':0.5,
        'font':{'family':'SimHei', 'size':25},


        'xanchor': 'center',
        'yanchor': 'top'},
        geo = dict(
            scope='usa',
            projection=go.layout.geo.Projection(type = 'albers usa'),
            showlakes=True,# lakes
            lakecolor='rgb(255, 255, 255)'),
    )
    py.offline.plot(fig3, filename="example3.html",auto_open=False)
    with open('example3.html',encoding='utf8',mode='r') as f:
        plot_all3 =''.join(f.readlines())

    title3 = the_element3
    consult3 = '压力大小计算：利用压力频率，将“一直”设置为0.6、“有时候”设置为0.2、“很少”设置为0.15、“从不”设置为0.05算权重。将压力等级分为四个等级，下面是每个等级分布的地区。'

    ## 图表三
    the_element = request.form['the_element_selected']
    print(the_element)
    fig = px.scatter(pressure_mostpre,x='压力程度',y=the_element,marginal_x='histogram',marginal_y='histogram',trendline="ols",template="plotly",color_continuous_scale=px.colors.sequential.Magenta)
    fig.update_layout(
         title={
        'text':'压力等级与'+the_element+'施加压力的关系'  ,
        'y':0.9,
        'x':0.5,
        'font':{'family':'SimHei', 'size':25},


       'xanchor': 'center',
        'yanchor': 'top'},
        margin=go.Margin(l=60,r=60,b=50,t=100,pad=0),


    )
    py.offline.plot(fig, filename="example.html",auto_open=False)
    with open('example.html',encoding='utf8',mode='r') as f:
        plot_all =''.join(f.readlines())
    element_available = element
    title2 ='压力等级与不同角色施加压力的关系'


    ## 图表四
    title4 = '在压力大时您最想做什么?'
    fig4 = px.line(combin_do, x="洲", y="占比", animation_frame="分类",
            hover_name="占比",range_y =[0,0.5]

            )
    fig4.update_layout(
        title={
        'text':'各地区减轻压力方式' ,
        'y':0.9,
        'x':0.5,
        'font':{'family':'SimHei', 'size':25},
        'xanchor': 'center',
        'yanchor': 'top'},

        margin=go.Margin(l=60,r=60,b=50,t=100,pad=0))
    py.offline.plot(fig4, filename="example4.html",auto_open=False)
    with open('example4.html',encoding='utf8',mode='r') as f:
        plot_all4 =''.join(f.readlines())

    return render_template('first.html',
                            the_title1 = title1,
                            the_select_element1 = element1_available,
                            the_data_pie1 = data_pie1,
                            the_plot_all = plot_all,
                            the_plot_all1 = plot_all1,
                            the_plot_all3 = plot_all3,
                            the_select_element3=element3_available,
                            the_title3 = title3,
                            the_consult3 = consult3,
                            the_select_element=element_available,
                            the_title2 = title2,
                            the_title4 = title4,
                           the_plot_all4 = plot_all4)


if __name__ == '__main__':

    app.run(debug=True)
