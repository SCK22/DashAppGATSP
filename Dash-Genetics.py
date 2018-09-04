import dash
from dash.dependencies import Input, Output,State
import dash_core_components as dcc 
import dash_html_components as html
import GeneticAlgoLibrary
import base64
image_filename = 'img//final.jpg' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

import pandas as pd
data = pd.read_csv("data/cities_and_distances.csv")
data.reset_index(inplace=True)
data1 = data.iloc[:,2:]
data1.index = data1.columns.values
dist_mat = data1

app = dash.Dash()
app.layout = html.Div(children = [
	# an element to take the input
	html.H1('Travelling Salesman problem using Genetic Algorithm'),
	html.H3('Best solution so far'),
	html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode())),
	html.P('Number of cities'),
	html.Div(dcc.Input(id='number_of_cities', value = 11,
		type = 'int')),
	html.P('Initial Population size'),
	html.Div(dcc.Input(id='initial_pop_size', value = 1000,
		type = 'int')),
	html.P('Elite Population size'),
	html.Div(dcc.Input(id='nelite', value = 500,
		type = 'int')),
	html.P('Percentage of population to mutate'),
	html.Div(dcc.Input(id='percentage_to_mutate', value = 10,
		type = 'int')),
	html.P('Percentage of population to crossover'),
	html.Div(dcc.Input(id='percentage_to_crossover', value = 80,
		type = 'int')),
	html.P('Overall runs'),
	html.Div(dcc.Input(id='noverall', value = 500,
		type = 'int')),
	# an element to handle the output
	html.Button('Run the genetic algorithm', id='my-button'),
	html.Div(id='output')
	])

# decorator/ wrapper
@app.callback(
	Output(component_id='output', 
		component_property='children'),
	[Input(component_id='my-button', component_property='n_clicks'),
	Input(component_id='noverall', component_property='value'),
	Input(component_id='number_of_cities', component_property='value'),
	Input(component_id='initial_pop_size', component_property='value'),
	Input(component_id='nelite', component_property='value'),
	Input(component_id='percentage_to_mutate', component_property='value'),
	Input(component_id='percentage_to_crossover', component_property='value')])
 
# @app.callback(
# 	Output(component_id='output', 
# 		component_property='children'),
# 	[Input(component_id='my-button', component_property='n_clicks'),)
 
def valuesProvided(n_clicks, noverall, number_of_cities, initial_pop_size, nelite, percentage_to_mutate, percentage_to_crossover):
	s = """Number of cities : {}
		Initial popultaion size :{}
		Number of elite solutions : {}
		Percentage to mutate : {}
		Percentage to crossover : {}
		Overall runs : {}""".format(number_of_cities, initial_pop_size, nelite,percentage_to_mutate, percentage_to_crossover, noverall)
	# if n_clicks is not None and n_clicks > 1:
	# 		return ("Please wait while the first run completes, or refresh the page.")
	if n_clicks is not None:
		ga_obj = GeneticAlgoLibrary.OverallGaRun(noverall=int(noverall),
                                     number_of_cities=int(number_of_cities),
                                     initial_pop_size=int(initial_pop_size),
                                     nelite=int(nelite),
                                     percentage_to_crossover=int(percentage_to_crossover),
                                     percentage_to_mutate=int(percentage_to_mutate),
                                     dist_mat=data1)
		sol = ga_obj.runOverallGa()
		return html.H3("Running the genetic algorithm with the configuration {} resulted in a solution : {}".format(s, sol))
	if n_clicks is None:
		return s


def update_value(n_clicks):
	# try:
		import sys
		import os
		sys.path.append(os.getcwd())
		# return "Power of the provided value is {}".format(str(float(input_data)**2))
		
		printStartingStatement(n_clicks)
	# except:
		# return "Value provided is not a real number"

if __name__ == '__main__':
	app.run_server(debug=True)