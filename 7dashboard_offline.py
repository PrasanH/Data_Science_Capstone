# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

## To run this file on vs code, type py (tab) then type your filename and run 

#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"


# Read the spacex data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

uniquelaunchsites = spacex_df['Launch Site'].unique().tolist()
lsites = []
lsites.append({'label': 'All Sites', 'value': 'All Sites'})
for site in uniquelaunchsites:
 lsites.append({'label': site, 'value': site}) 

succ_launch=spacex_df.groupby(['Launch Site'])['class'].sum().reset_index()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color':'#d62728' ,
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown documentation here----https://dash.plotly.com/dash-core-components/dropdown

                                  dcc.Dropdown(id='Launch Site',
                                                options= lsites,
                                                value='ALL',
                                                placeholder="Select Launch Site(s)",
                                                searchable=True,
                                                style = {'color': 'Blue'}
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload Range (Kg):", style={'color': 'blue', 'fontSize': 20}),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min=0, max= 12000, step=1000, id='payload-slider', value=[min_payload, max_payload]), #value defines the initial load range
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='Success-payload-scatter-chart')),
                                html.Br(),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='Launch Site', component_property='value'))



def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['class'] == 1]
    if entered_site == 'All Sites':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site',                        #names are the labels which we want
        title='Total Successful launches by Site')
        return fig
    else:
        df_filter1= spacex_df[spacex_df['Launch Site']== entered_site]              #filter df by selected launchSite
        df_filter1= df_filter1.groupby('class').size().reset_index(name='counts')   #gives the counts of class column 
        fig = px.pie(df_filter1, values='counts', 
        names='class', 
        title=f'Total Successful launches for {entered_site}')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='Success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='Launch Site', component_property='value'), Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, payload_slider):
    
    if entered_site == 'All Sites':
        low, high = payload_slider
        mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(spacex_df[mask], x='Payload Mass (kg)' , y='class', color='Booster Version Category')
        fig.update_layout(title='Correlation between Payload and Success for all Sites', title_font=dict(color='blue', size=16))
        return fig
    
    else:
        df_filter1= spacex_df[spacex_df['Launch Site']== entered_site]              #filter df by selected launchSite
        low, high = payload_slider
        mask = (df_filter1['Payload Mass (kg)'] > low) & (df_filter1['Payload Mass (kg)'] < high)
        fig = px.scatter(df_filter1[mask], x='Payload Mass (kg)' , y='class', color='Booster Version Category')
        fig.update_layout(title=f'Correlation between Payload and Success for {entered_site}', title_font=dict(color='blue', size=16))
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
  