import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from pandas_datareader import data as web
from datetime import datetime as dt
import pandas as pd
data1 = pd.read_csv('./mental_health_poll_updated.csv',encoding='utf-8').set_index('问题')


app = dash.Dash(__name__)
app.layout =html.Div([
    dcc.Dropdown(
    id='my-dropdown',
    options=[
        {'label': '您多久受到一次压力？', 'value': '您多久受到一次压力？'}, 
        {'label': "您使用什么资源来帮助您减轻压力", 'value': "您使用什么资源来帮助您减轻压力"},
        {'label':'在压力大时你最想做什么','value':'在压力大时你最想做什么'},
        {'label': '最让您感到压力的是什么？': '最让您感到压力的是什么？'}
        
        ],
        value='How often are you stressed'),
    html.Div(
        id='output-data-upload',
        style={'marginTop':'30'}),
    html.Div(
        dcc.Graph(id='my-graph')
    ),
     html.Div([
        html.P(id='text'
              )]),

],
    style={'width': '70%'}
)
    

    
@app.callback(dash.dependencies.Output('output-data-upload','children'), [dash.dependencies.Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    df = pd.DataFrame(data1.loc[selected_dropdown_value]['分类'].value_counts()).T.rename(index={'分类':selected_dropdown_value})
    return html.Div([
        dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows") )
    ] 
    )
@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph1(selected_dropdown_value):
    
    return {
        'data': [{
           
            'x': pd.DataFrame(data1.loc[selected_dropdown_value]['分类'].value_counts()).index,
            'y': list(data1.loc[selected_dropdown_value]['分类'].value_counts()),
            'type':'bar'
        }],
        'layout': {'margin': {'l': 40, 'r': 0, 't': 100, 'b': 30}}
    }

@app.callback(Output('text', 'children'), [Input('my-dropdown', 'value')])
def update_text(selected_dropdown_value):
    if selected_dropdown_value=='您多久受到一次压力？':
        return html.P(
            id='text',
            children='从此图表可以看出大多数人长时间承担着压力的，只有少部分从来没有压力。')
    elif selected_dropdown_value=="在压力大时你最想做什么":
        return html.P(
            id='text',
            children='当压力大时大多数人希望告诉朋友或者吃饭。')
    elif selected_dropdown_value=='您使用什么资源来帮助您减轻压力':
        return html.P(
            id='text',
            children='当压力大时大多数人选择玩手机上网排解压力，而不是去咨询心理医生。')
    elif selected_dropdown_value=='最让您感到压力的是什么？':
        return html.P(
            id='text',
            children='情侣施加的压力比父母、老师多，父母与老师施加压力性质相同。')

if __name__ == '__main__':
    app.run_server(port=8015)
