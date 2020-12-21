#Python and RDF
from rdflib import Graph, URIRef


print('\nSEARCH : ')
#Initialize a graph
search_info_graph = Graph()
#Parse in an RDF file graph dbpedia
#Ask for input, and clean the input to search for it
#query=str(input('Enter your search :'))
query=''#TODO DELTE
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
search_info_graph.parse(search)
if len(search_info_graph.serialize(format='n3').decode('utf-8'))==0 or len(search_info_graph.serialize(format='n3').decode('utf-8'))==1:
    print('Page not found')
#TODO Maybe search more info and add a way to print the predicate, ie openingDate : 1793 for Louvre query
results = search_info_graph.query("""
       PREFIX dbo: <http://dbpedia.org/ontology/> 
       PREFIX s: <""" + search +"""> 
       PREFIX dbp: <http://dbpedia.org/property/>
       SELECT ?abstract ?established ?openingDate
       WHERE {
          ?s dbo:abstract ?abstract .
          OPTIONAL {?s dbp:established ?established .}
          OPTIONAL {?s dbo:openingDate ?openingDate .}
          FILTER (lang(?abstract) = 'en')
       }""")
if len(results)==0:
    print("Nothing valuable has been found")
for element in results:
    for i in range(len(element)):
        if element[i] ==None:
            continue
        if i == 0:
            print('ABSTRACT : ', end='')
        if i ==1 or i==2:
            print("Opening/Established in : ", end='')
        print(element[i])#print the element only


print('\nTRANSPORTS : ')
#Transport LIST
transport_graph = Graph()
transport_graph.parse("Paris_transport_rdf_xlm.owl")

#If new type of transport, add one Union with bas:NewTransport
all_transports = transport_graph.query(""" 
       PREFIX bas: <http://www.semanticweb.org/Paris_transport_ontologie#> 
       PREFIX owl: <http://www.w3.org/2002/07/owl#> 
       PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
       PREFIX xml: <http://www.w3.org/XML/1998/namespace> 
       PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
       PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

       SELECT ?bas
       WHERE {{
        ?bas rdf:type bas:Bus . 
       }
       UNION {
        ?bas rdf:type bas:Metro . 
       }
       UNION {
        ?bas rdf:type bas:RER . 
       }
       UNION {
        ?bas rdf:type bas:Uber . 
       }
       UNION {
        ?bas rdf:type bas:Taxi_VTC . 
       }
       UNION {
        ?bas rdf:type bas:Lime . 
       }}

       """)

#"Clean" the results to print only transport's name
for transport in all_transports:
    for s in range(len(transport)):
        s_ = str(transport[s]).split('#')
        if 'http://www.semanticweb.org/Paris_transport_ontologie' in s_:
            s_.remove('http://www.semanticweb.org/Paris_transport_ontologie')
        if not s_:
            sub = 'Paris_transport_ontologie'
        else:
            sub = s_[0]
        print(sub)#print the element only


print('\nUSER : ')
#ask user name
#user_name=str(input('User name : '))
user_name=''#TODO Delete
if len(user_name)==0:
    user_name='Marie'
#Cleaning
user_name_=user_name.replace(" ", "_")
user_name_list=[]
user_name_list[:0]=user_name_
if user_name_list[0]=='_':
    del user_name_list[0]
if user_name_list[-1]=='_':
    del user_name_list[-1]
user_name_= ''.join(user_name_list)
#query for user's name and return transports, depart, arrivee
trajet = transport_graph.query(""" 
       PREFIX bas: <http://www.semanticweb.org/Paris_transport_ontologie#> 
       PREFIX owl: <http://www.w3.org/2002/07/owl#> 
       PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
       PREFIX xml: <http://www.w3.org/XML/1998/namespace> 
       PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
       PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

       SELECT ?bas
       WHERE {{
       ?bas bas:estDepartDe bas:Marie .
       }
       UNION {
        ?bas bas:estUtilisePar bas:Marie .  
       }
       UNION {
       ?bas bas:estArriveDe bas:Marie .
       }
       }""")

print(len(trajet))#TODO Do not remove, otherwise, it will not show all the results ? BUG
#"Clean" the results to print only transport's name
counter=0
for tra in trajet:
    if counter == 0:
        print("Departure : ", end='')
    elif counter == 1:
        print("Transports : \n    -", end='')
    elif 1 == len(trajet) - counter:
        print("Arriving : ", end='')
    else:
        print('    -', end='')
    for s in range(len(tra)):
        s_ = str(tra[s]).split('#')
        if 'http://www.semanticweb.org/Paris_transport_ontologie' in s_:
            s_.remove('http://www.semanticweb.org/Paris_transport_ontologie')
        if not s_:
            sub = 'Paris_transport_ontologie'
        else:
            sub = s_[0]
        print(sub)#print the element only
    counter+=1