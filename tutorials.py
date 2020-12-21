#1 - Python and RDF
from rdflib import Graph
#Initialize a graph
g = Graph()

#Parse in an RDF file graph dbpedia
#Ask for input, and clean the input to search for it
query=str(input('Enter your search :'))
if len(query)==0:
    query='Eiffel Tower'
#Cleaning
query_=query.replace(" ", "_")
query_list=[]
query_list[:0]=query_
if query_list[0]=='_':
    del query_list[0]
if query_list[-1]=='_':
    del query_list[-1]
query_= ''.join(query_list)

#Search
base = "http://dbpedia.org/resource/"
search=base+query_
print("Searching for ",query," at ",search)
g.parse(search)
results = g.query("""
       PREFIX dbo: <http://dbpedia.org/ontology/> 
       PREFIX s: <http://dbpedia.org/resource/"""+query_+"""> 
       SELECT ?abstract
       WHERE {
          ?s dbo:abstract ?abstract .
          FILTER (lang(?abstract) = 'en')
       }""")
for element in results:
    print(element[0])#print the element only
#Loop through each tripe in the graph (subj, pred, obj) and print abstract of the query
for index, (sub, pred, obj) in enumerate(g):
    #print(pred,obj)
    if pred[-8:-1] == 'abstrac':
        if obj.language == 'en':
            print(sub,pred,obj)

#Print the size of the graph
print(f"{query} has {len(g)} facts")

#Print out the entire graph in RDF Turtle format
#print(g.serialize(format='ttl').decode('u8'))

#Manual graph
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD

g = Graph()
mason = URIRef("http://example.org/mason")
g.add((mason, RDF.type, FOAF.Person))
g.add((mason, FOAF.nick, Literal("mason", lang="en")))
g.add((mason, FOAF.name, Literal ("Mason Carter")))
g.add((mason, FOAF.mbox, URIRef("mailto:mason@example.org")))

shyla = URIRef("http://example.org/shyla")
g.add((shyla, RDF.type, FOAF.Person))
g.add((shyla, FOAF.nick, Literal("shyla", lang="fr")))
g.add((shyla, FOAF.name, Literal ("Shyla Sharter")))
g.add((shyla, FOAF.mbox, URIRef("mailto:shyla@example.org")))

print("\nALL")
for s, p, o in g:
    print(s, p, o)

print('\nNICK')
g.bind("foaf", FOAF)

test_q = "select ?Person where {Person nick nick. ?Person nick lang=en .}"
x = g.query("""SELECT DISTINCT ?name
       WHERE {
          ?Person foaf:name ?name .
       }""")
print(list(x))
#For each foaf:Person in the graph print out heir nickname value
for person in g.subjects(RDF.type, FOAF.Person):
    for nick in g.objects(person, FOAF.nick):
        print(nick)

#Bind the foaf namespace to a prefix for more readable output
g.bind("foaf", FOAF)

print('\nALL bis')
#print all data in the n3 format
print(g.serialize(format='n3').decode('utf-8'))

#Navigating RDF graph

g = Graph()
g.parse('http://dbpedia.org/resource/Berlin')
for s,p,o in g:
    print(s,p,o)
    break

print(len(g))

#Check if triple exist
if(URIRef('http://dbpedia.org/resource/Berlin'),None,None) in g:
    print(f'Triple exist!')
else:
    print(f'Triple does not exist!')

import rdflib

g = rdflib.Graph()
has_border_with = rdflib.URIRef('http://www.example.org/has_border_with')
located_in = rdflib.URIRef('http://www.example.org/located_in')

germany = rdflib.URIRef('http://www.example.org/country1')
france = rdflib.URIRef('http://www.example.org/country2')
china = rdflib.URIRef('http://www.example.org/country3')
mongolia = rdflib.URIRef('http://www.example.org/country4')

europa = rdflib.URIRef('http://www.example.org/part1')
asia = rdflib.URIRef('http://www.example.org/part2')

g.add((germany,has_border_with,france))
g.add((china,has_border_with,mongolia))
g.add((germany,located_in,europa))
g.add((france,located_in,europa))
g.add((china,located_in,asia))
g.add((mongolia,located_in,asia))

q = "select ?country where { ?country <http://www.example.org/located_in> <http://www.example.org/part1> }"
x = g.query(q)
print(list(x))
# write graph to file, re-read it and query the newly created graph
g.serialize("graph.rdf")
g1 = rdflib.Graph()
g1.parse("graph.rdf", format="xml")
x1 = g1.query(q)
print(list(x1))

#TODO Delete below it was just a test -> It was for main.py
transport_graph = Graph()
transport_graph.parse("Paris_transport_rdf_xlm.owl")

for s,p,o in transport_graph:
    s_=str(s).split('#')
    p_ = str(p).split('#')
    o_ = str(o).split('#')
    if 'http://www.semanticweb.org/Paris_transport_ontologie' in s_:
        s_.remove('http://www.semanticweb.org/Paris_transport_ontologie')
    if not s_:
        sub='Paris_transport_ontologie'
    else :
        sub=s_[0]
    if 'http://www.semanticweb.org/Paris_transport_ontologie' in p_:
        p_.remove('http://www.semanticweb.org/Paris_transport_ontologie')
    if not p_:
        pred='Paris_transport_ontologie'
    else :
        pred=p_[0]
    if 'http://www.semanticweb.org/Paris_transport_ontologie' in o_:
        o_.remove('http://www.semanticweb.org/Paris_transport_ontologie')
    if not o_:
        obj='Paris_transport_ontologie'
    else :
        obj=o_[0]
    print(sub, pred, obj)