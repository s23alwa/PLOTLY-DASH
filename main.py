import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import jupyter_dash
from wordcloud import WordCloud, STOPWORDS 
import base64
from io import BytesIO
app = jupyter_dash.JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
survey_df = pd.read_csv("https://storage.googleapis.com/hk4403/dashboard-data-latest.csv ")
survey_df.columns = survey_df.columns.str.replace(' ', '_').str.lower()
survey_df['month_year'] = pd.to_datetime(survey_df[['year', 'month']].assign(DAY=1))


"""# Dynamic Bar chart for Number of people surveyed"""

# df = survey_df.copy()
# df = pd.read_csv("https://storage.googleapis.com/hk4403/dashboard-data-latest.csv ")
# df.columns = df.columns.str.replace(' ', '_').str.lower()
# df = df.groupby(['region_code','country','wave'])[['sample_total']].sum()
# df.reset_index(inplace=True)
# print(df[:5])
df = pd.read_csv("https://storage.googleapis.com/hk4403/dashboard-data-latest.csv ")
df.columns = df.columns.str.replace(' ', '_').str.lower()
df = df[(df.urban_rural == 'National') & (df.industry == 'All')]
df = df.groupby(['region_code','wave','indicator_topic'])[['sample_subset']].sum()
df.reset_index(inplace=True)
df = df.sort_values('indicator_topic')
# print(df[:5])

"""# Scatter plot"""

# covid_FS = survey_df[(survey_df.indicator_topic== 'Food Security')& (survey_df.indicator == 'FS_day') &(survey_df.wave == 'WAVE1') & (survey_df.urban_rural == 'National') & (survey_df.industry == 'All')]
covid_FS = survey_df[(survey_df.indicator_topic== 'Food Security')& (survey_df.indicator == 'FS_day')  & (survey_df.urban_rural == 'National') & (survey_df.industry == 'All')]
df2 = pd.DataFrame(covid_FS,columns=['region','country','wave','gdp_pc','sample_total','indicator_val'])
df2=df2.drop_duplicates()

df2['gdp_pc'] = df2['gdp_pc'].fillna(0)
df2.head
fig3 = px.scatter(df2, x="gdp_pc", y="sample_total",animation_frame="wave",animation_group="country",
                 size="indicator_val",color="wave", hover_name="country",
                  log_x=True, 
                  size_max=55, range_x=[800,30000], range_y=[-10,9000])
                #  log_x=True, size_max=60)
#fig3.update_layout(showlegend=False)
# fig3.show()

# # covid_FS = survey_df[(survey_df.indicator_topic== 'Food Security')& (survey_df.indicator == 'FS_day') &(survey_df.wave == 'WAVE1') & (survey_df.urban_rural == 'National') & (survey_df.industry == 'All')]
# covid_FS = survey_df[(survey_df.indicator_topic== 'Food Security')& (survey_df.indicator == 'FS_day')  & (survey_df.urban_rural == 'National') & (survey_df.industry == 'All')]
# df2 = pd.DataFrame(covid_FS,columns=['region','country','wave','gdp_pc','sample_total','indicator_val','income_group'])
# df2=df2.drop_duplicates()

# df2['gdp_pc'] = df2['gdp_pc'].fillna(0)
# df2.head
# fig3 = px.scatter(df2, x="gdp_pc", y="indicator_val",animation_frame="wave",animation_group="country",
#                  size="sample_total",color="region", hover_name="country",
#                   log_x=True, 
#                   size_max=55, range_x=[700,26000], range_y=[-10,100])
#                 #  log_x=True, size_max=60)
# fig3.show()

"""# Word cloud"""

df1 = survey_df.copy()
words = df1.indicator_topic.unique()
plt.subplots(figsize = (8,8))
wordcloud = WordCloud (
                    background_color = 'white',
                    width = 512,
                    height = 384
                        ).generate(' '.join(words))
wc_img1 = wordcloud.to_image()
with BytesIO() as buffer:
    wc_img1.save(buffer, 'png')
    img1 = base64.b64encode(buffer.getvalue()).decode()
fig2 = plt.imshow(wordcloud) # image show
plt.axis('off') # to off the axis of x and y
# plt.show()

words1 = df1.country.unique()
plt.subplots(figsize = (8,8))
wordcloud = WordCloud (
                    background_color = 'white',
                    width = 512,
                    height = 384
                        ).generate(' '.join(words1))
wc_img2 = wordcloud.to_image()
with BytesIO() as buffer:
    wc_img2.save(buffer, 'png')
    img2 = base64.b64encode(buffer.getvalue()).decode()
fig21 = plt.imshow(wordcloud) # image show
plt.axis('off') # to off the axis of x and y
# plt.show()

words2 = df1.region.unique()
plt.subplots(figsize = (8,8))
wordcloud = WordCloud (
                    background_color = 'white',
                    width = 512,
                    height = 384
                        ).generate(' '.join(words2))
wc_img3 = wordcloud.to_image()
with BytesIO() as buffer:
    wc_img3.save(buffer, 'png')
    img3 = base64.b64encode(buffer.getvalue()).decode()
fig22 = plt.imshow(wordcloud) # image show
plt.axis('off') # to off the axis of x and y
# plt.show()

"""# Layout"""

app.layout = html.Div(children=[

    html.H1('',
            style={'text-align': 'center', 'font-style': 'cursive'}),
    dbc.Row([
        dbc.Col(html.H1(html.B("COVID-19 impact survey data analysis"), style={'text-align': 'center',"border":"2px black solid"}
                        )
        )
    ]),
  html.Br(),
  html.Hr(),
  #****************************
  #Card layout
  #**************************** 
  html.Hr(),
  html.Br(),
  dbc.Row(
            [
            dbc.Col(card1, width="auto"),
            dbc.Col(card2, width="auto"),
            dbc.Col(card3, width="auto"),
            dbc.Col(card4, width="auto"),
            ],
            
            justify="center",
  ),
    html.Hr(),
    #
    html.Br(),
    html.Div(children=[



   html.H1("Survey statistics by country", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_region",
                 options=[
                     {"label": "East Asia and Pacific", "value": "EAP"},
                     {"label": "Sub Saharan Africa", "value": "SSA"},
                     {"label": "Middle East & North Africa", "value": "MNA"},
                     {"label": "Latin America & Caribbean", "value": "LAC"},
                     {"label": "Europe & Central Asia", "value": "ECA"}
                     ],
                 multi=False,
                 value="EAP",
                 style={'width': "40%"}
                 ),
    dcc.Dropdown(id="slct_wave",
                 options=[
                                 {"label": "WAVE1", "value": "WAVE1"},
                                 {"label": "WAVE2", "value": "WAVE2"},
                                 {"label": "WAVE3", "value": "WAVE3"},
                                 {"label": "WAVE4", "value": "WAVE4"},
                                 {"label": "WAVE5", "value": "WAVE5"},
                                 {"label": "WAVE6", "value": "WAVE6"},
                                 {"label": "WAVE7", "value": "WAVE7"},
                                 {"label": "WAVE8", "value": "WAVE8"},
                                 {"label": "WAVE9", "value": "WAVE9"},
                                 {"label": "WAVE10", "value": "WAVE10"},
                                 {"label": "WAVE11", "value": "WAVE11"},
                                 {"label": "WAVE12", "value": "WAVE12"},
                                 {"label": "WAVE13", "value": "WAVE13"},
                                 {"label": "WAVE14", "value": "WAVE14"},
                                 {"label": "WAVE15", "value": "WAVE15"},
                                 {"label": "WAVE16", "value": "WAVE16"},
                                 {"label": "WAVE17", "value": "WAVE17"}
                             ],
                 multi=False,
                 value="WAVE1",
                 style={'width': "40%"}
                 ),

    dcc.Graph(id='survey_size_map', figure={}),

   ], style={"border":"2px black solid"}#style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-around'}
   ),

    #  html.Div(children=[

    #         html.H2('Income group distribution across various countrieds and  waves  in the survey samples'),

    #         html.Div(children='''
                 
    #           '''),

    #         html.Br(),

    #         dcc.Graph(
    #             id='fig2',
    #             figure=fig2
    #         ),
    #     ], style={'width': '45%'}),
        
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        # html.Div(children=[
        #             html.Img(src="data:image/png;base64," + img1,style={"border":"2px black solid",'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-around'})
        #         ]) ,

        html.Div([

        dcc.Tabs([

        # First tab
        dcc.Tab(label='Indicators Surveyed', children=[

            # First graph
            html.Img(src="data:image/png;base64," + img1,style={
                    "border":"2px black solid",
                    # 'display': 'inline-block',
                    'vertical-align': 'bottom',
                    'width': '33%',
                     "align-items": "center"
                        })]),
               
dcc.Tab(label='Countries Surveyed', children=[
            # Second graph
            html.Img(src="data:image/png;base64," + img2,style={
                    "border":"2px black solid",
                    'width': '33%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center',"align":"center"}
                  #  'display': 'inline-block',
                  #   'align-items': 'center', 'justify-content': 'center',
                  #  'width': '30%',
                        # }
                     )]),

            # Third graph
dcc.Tab(label='Regions Surveyed', children=[
            html.Img(src="data:image/png;base64," + img3,style={
                    "border":"2px black solid",
                    # 'display': 'inline-block',
                    'vertical-align': 'bottom',
                    'width': '33%',
                    "align":"right"
                        })])
            
            ], style={'width': '33%',"align-items": "center", "justify-content": "center"})

        ]),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),

        html.Div(children=[
                    dcc.Graph(
        id='scatter plot',
        figure=fig3
    )
                ], style={"border":"2px black solid"}) ,
                

   html.Br(),
   html.Br(),
   html.Br(),
   html.Br(),

]
, style={'backgroundColor': 'white'}
)

"""# Callback"""

@app.callback(
    Output(component_id='survey_size_map', component_property='figure'),
    [Input(component_id='slct_region', component_property='value'),
     Input(component_id='slct_wave', component_property='value')]
)
def update_graph(option_slctd,option1_slctd):
    print(option_slctd)
    print(type(option_slctd))

    dff = df.copy()
    dff = dff[(dff["region_code"] == option_slctd) & (dff["wave"] == option1_slctd)]
    dff = dff.sort_values("indicator_topic")
    figure = px.bar(
        data_frame=dff,
        x='indicator_topic',
        y='sample_subset',
        hover_data=['indicator_topic', 'sample_subset']
        ,labels={'indicators': 'total ppl surveyed'}
        ,template='seaborn'
    )

    return figure

"""# App execution"""

if __name__ == '__main__':
    app.run_server( port=8080, debug=True)
