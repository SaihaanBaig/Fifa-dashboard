import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Create dataset
data = [
    {"year": 1930, "winner": "Uruguay", "runner_up": "Argentina"},
    {"year": 1934, "winner": "Italy", "runner_up": "Czechoslovakia"},
    {"year": 1938, "winner": "Italy", "runner_up": "Hungary"},
    {"year": 1950, "winner": "Uruguay", "runner_up": "Brazil"},
    {"year": 1954, "winner": "Germany", "runner_up": "Hungary"},
    {"year": 1958, "winner": "Brazil", "runner_up": "Sweden"},
    {"year": 1962, "winner": "Brazil", "runner_up": "Czechoslovakia"},
    {"year": 1966, "winner": "England", "runner_up": "Germany"},
    {"year": 1970, "winner": "Brazil", "runner_up": "Italy"},
    {"year": 1974, "winner": "Germany", "runner_up": "Netherlands"},
    {"year": 1978, "winner": "Argentina", "runner_up": "Netherlands"},
    {"year": 1982, "winner": "Italy", "runner_up": "Germany"},
    {"year": 1986, "winner": "Argentina", "runner_up": "Germany"},
    {"year": 1990, "winner": "Germany", "runner_up": "Argentina"},
    {"year": 1994, "winner": "Brazil", "runner_up": "Italy"},
    {"year": 1998, "winner": "France", "runner_up": "Brazil"},
    {"year": 2002, "winner": "Brazil", "runner_up": "Germany"},
    {"year": 2006, "winner": "Italy", "runner_up": "France"},
    {"year": 2010, "winner": "Spain", "runner_up": "Netherlands"},
    {"year": 2014, "winner": "Germany", "runner_up": "Argentina"},
    {"year": 2018, "winner": "France", "runner_up": "Croatia"},
    {"year": 2022, "winner": "Argentina", "runner_up": "France"}
]

df = pd.DataFrame(data)
df.replace({'winner': {'West Germany': 'Germany'}, 'runner_up': {'West Germany': 'Germany'}}, inplace=True)
winner_counts = df['winner'].value_counts().reset_index()
winner_counts.columns = ['country', 'wins']

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # This is what gunicorn needs!

# Layout
app.layout = html.Div(style={'backgroundColor': '#111111', 'color': 'white', 'padding': '20px'}, children=[
    html.H1("FIFA World Cup Winners & Runner-Ups", style={"textAlign": "center"}),

    dcc.Graph(id='choropleth',
              figure=px.choropleth(winner_counts,
                                   locations="country",
                                   locationmode='country names',
                                   color="wins",
                                   title="Countries with FIFA World Cup Wins",
                                   color_continuous_scale="Viridis")),

    html.Div([
        html.Label("Select a country:"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': c, 'value': c} for c in sorted(winner_counts['country'].unique())],
            value='Brazil',
            style={'color': 'black'}
        ),
        html.Div(id='country-output', style={"marginTop": "10px", "fontSize": "18px"}),
    ], style={'width': '45%', 'display': 'inline-block', 'padding': '20px'}),

    html.Div([
        html.Label("Select a year:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': y, 'value': y} for y in sorted(df['year'])],
            value=2022,
            style={'color': 'black'}
        ),
        html.Div(id='year-output', style={"marginTop": "10px", "fontSize": "18px"}),
    ], style={'width': '45%', 'display': 'inline-block', 'padding': '20px'})
])

# Callbacks
@app.callback(
    Output('country-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_output(selected_country):
    count = df[df['winner'] == selected_country].shape[0]
    return f"{selected_country} has won the World Cup {count} time(s)."

@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year_output(selected_year):
    row = df[df['year'] == selected_year].iloc[0]
    return f"In {selected_year}, Winner: {row['winner']}, Runner-Up: {row['runner_up']}."

# Run locally
if __name__ == '__main__':
    app.run_server(debug=True)
