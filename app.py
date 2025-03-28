{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Imports"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import plotly.express as px\n",
    "import dash\n",
    "from dash import dcc, html, Input, Output"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Dataset"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "data = [\n",
    "    {\"year\": 1930, \"winner\": \"Uruguay\", \"runner_up\": \"Argentina\"},\n",
    "    {\"year\": 1934, \"winner\": \"Italy\", \"runner_up\": \"Czechoslovakia\"},\n",
    "    {\"year\": 1938, \"winner\": \"Italy\", \"runner_up\": \"Hungary\"},\n",
    "    {\"year\": 1950, \"winner\": \"Uruguay\", \"runner_up\": \"Brazil\"},\n",
    "    {\"year\": 1954, \"winner\": \"Germany\", \"runner_up\": \"Hungary\"},\n",
    "    {\"year\": 1958, \"winner\": \"Brazil\", \"runner_up\": \"Sweden\"},\n",
    "    {\"year\": 1962, \"winner\": \"Brazil\", \"runner_up\": \"Czechoslovakia\"},\n",
    "    {\"year\": 1966, \"winner\": \"England\", \"runner_up\": \"Germany\"},\n",
    "    {\"year\": 1970, \"winner\": \"Brazil\", \"runner_up\": \"Italy\"},\n",
    "    {\"year\": 1974, \"winner\": \"Germany\", \"runner_up\": \"Netherlands\"},\n",
    "    {\"year\": 1978, \"winner\": \"Argentina\", \"runner_up\": \"Netherlands\"},\n",
    "    {\"year\": 1982, \"winner\": \"Italy\", \"runner_up\": \"Germany\"},\n",
    "    {\"year\": 1986, \"winner\": \"Argentina\", \"runner_up\": \"Germany\"},\n",
    "    {\"year\": 1990, \"winner\": \"Germany\", \"runner_up\": \"Argentina\"},\n",
    "    {\"year\": 1994, \"winner\": \"Brazil\", \"runner_up\": \"Italy\"},\n",
    "    {\"year\": 1998, \"winner\": \"France\", \"runner_up\": \"Brazil\"},\n",
    "    {\"year\": 2002, \"winner\": \"Brazil\", \"runner_up\": \"Germany\"},\n",
    "    {\"year\": 2006, \"winner\": \"Italy\", \"runner_up\": \"France\"},\n",
    "    {\"year\": 2010, \"winner\": \"Spain\", \"runner_up\": \"Netherlands\"},\n",
    "    {\"year\": 2014, \"winner\": \"Germany\", \"runner_up\": \"Argentina\"},\n",
    "    {\"year\": 2018, \"winner\": \"France\", \"runner_up\": \"Croatia\"},\n",
    "    {\"year\": 2022, \"winner\": \"Argentina\", \"runner_up\": \"France\"}\n",
    "]\n",
    "\n",
    "df = pd.DataFrame(data)\n",
    "\n",
    "# Consider West Germany and Germany the same\n",
    "df.replace({'winner': {'West Germany': 'Germany'}, 'runner_up': {'West Germany': 'Germany'}}, inplace=True)\n",
    "\n",
    "# Winners count\n",
    "winner_counts = df['winner'].value_counts().reset_index()\n",
    "winner_counts.columns = ['country', 'wins']\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Step 2: Initialize Dash App\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [],
   "source": [
    "app = dash.Dash(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [],
   "source": [
    "server = app.server  # For deployment on Render\n",
    "app.layout = html.Div(style={'backgroundColor': '#111111', 'color': 'white', 'padding': '20px'}, children=[\n",
    "    html.H1(\"FIFA World Cup Winners & Runner-Ups\", style={\"textAlign\": \"center\"}),\n",
    "\n",
    "    # Choropleth Map\n",
    "    dcc.Graph(id='choropleth',\n",
    "              figure=px.choropleth(winner_counts,\n",
    "                                   locations=\"country\",\n",
    "                                   locationmode='country names',\n",
    "                                   color=\"wins\",\n",
    "                                   title=\"Countries with FIFA World Cup Wins\",\n",
    "                                   color_continuous_scale=\"Viridis\")),\n",
    "\n",
    "    html.Div([\n",
    "        html.Label(\"Select a country:\"),\n",
    "        dcc.Dropdown(\n",
    "            id='country-dropdown',\n",
    "            options=[{'label': c, 'value': c} for c in sorted(winner_counts['country'].unique())],\n",
    "            value='Brazil',\n",
    "            style={'color': 'black'}  # Keep dropdown text black for visibility\n",
    "        ),\n",
    "        html.Div(id='country-output', style={\"marginTop\": \"10px\", \"fontSize\": \"18px\"}),\n",
    "    ], style={'width': '45%', 'display': 'inline-block', 'padding': '20px'}),\n",
    "\n",
    "    html.Div([\n",
    "        html.Label(\"Select a year:\"),\n",
    "        dcc.Dropdown(\n",
    "            id='year-dropdown',\n",
    "            options=[{'label': y, 'value': y} for y in sorted(df['year'])],\n",
    "            value=2022,\n",
    "            style={'color': 'black'}  # Keep dropdown text black for visibility\n",
    "        ),\n",
    "        html.Div(id='year-output', style={\"marginTop\": \"10px\", \"fontSize\": \"18px\"}),\n",
    "    ], style={'width': '45%', 'display': 'inline-block', 'padding': '20px'})\n",
    "])\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Callbacks"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.callback(\n",
    "    Output('country-output', 'children'),\n",
    "    Input('country-dropdown', 'value')\n",
    ")\n",
    "def update_country_output(selected_country):\n",
    "    count = df[df['winner'] == selected_country].shape[0]\n",
    "    return f\"{selected_country} has won the World Cup {count} time(s).\"\n",
    "\n",
    "@app.callback(\n",
    "    Output('year-output', 'children'),\n",
    "    Input('year-dropdown', 'value')\n",
    ")\n",
    "def update_year_output(selected_year):\n",
    "    row = df[df['year'] == selected_year].iloc[0]\n",
    "    return f\"In {selected_year}, Winner: {row['winner']}, Runner-Up: {row['runner_up']}.\"\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "        <iframe\n",
       "            width=\"100%\"\n",
       "            height=\"650\"\n",
       "            src=\"http://127.0.0.1:8050/\"\n",
       "            frameborder=\"0\"\n",
       "            allowfullscreen\n",
       "            \n",
       "        ></iframe>\n",
       "        "
      ],
      "text/plain": [
       "<IPython.lib.display.IFrame at 0x13dfa8b50>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
