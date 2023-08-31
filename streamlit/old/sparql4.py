from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

#print('hola')
# Specify the DBPedia endpoint
sparql = SPARQLWrapper("https://mired.uspceu.es/sparql")

# Query for the description of "Capsaicin", filtered by language
sparql.setQuery("""
    prefix mcr: <https://mired.uspceu.es/microrrelatos#>
    select distinct ?Concept where {[] a ?Concept} LIMIT 100
""")

# Convert results to JSON format
sparql.setReturnFormat(JSON)
result = sparql.query().convert()

# The return data contains "bindings" (a list of dictionaries)
for hit in result["results"]["bindings"]:
    # We want the "value" attribute of the "comment" field
    print(hit["Concept"]["value"])

#results_df = pd.io.json.json_normalize(results['results']['bindings'])
#results_df[['item.value', 'itemLabel.value']]
