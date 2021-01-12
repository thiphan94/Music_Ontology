# hello_psg.py
#Transport LIST
from rdflib import Graph, URIRef
from rdflib.tools import csv2rdf

transport_graph = Graph()
transport_graph.parse("Projet_transport_rdf_xlm.owl")

#uber_graph= Graph()
#uber_graph.parse("Uber_Paris.owl")
quarter=['Q1', 'Q2', 'Q3', 'Q4']
year=['2017', '2018', '2019', '2020']
import PySimpleGUI as sg
#sg.theme('Reddit')   # Add a touch of color

col = [[sg.Frame(layout=[[sg.Multiline("Welcome to the prototype of this application that will :\n   - Show all transports available\n   - Search for users journey\n   - Search for information on dbpedia\nThis app uses a personalised ontology representing some of the Transports available in Paris.",key='-TEXT-',size=(500,30))]],
        title='Informations:')]]


layout = [
    [sg.Frame(layout=[[sg.Button("Show all Transport",size=(31,1))],
    [sg.Button("Search Users"),sg.Text('',key='-Search-0'), sg.InputText(size=(19,1))],
    [sg.Button("Search Information"),sg.Text('',key='-Search-1'), sg.InputText(size=(15,1))],
    [sg.Button("Uber statistics for"), sg.Listbox((quarter), size=(20, 4), enable_events=True, key='_LIST_'), sg.Listbox((year), size=(20, 4), enable_events=True, key='_LIST1_')]
    ], title='Interface:'), sg.Column(col)],
]
# Create the window
window = sg.Window("Demo", layout,size=(1080,550),return_keyboard_events=True)

# Create an event loop
while True:
    event, values = window.read()
    for i,j in values.items():
        print(i,j)
    if event == "Search Information":
        event, values = window.read()
        to_print=[]
        print(values.get(1))
        # Initialize a graph
        search_info_graph = Graph()
        # Parse in an RDF file graph dbpedia
        # Ask for input, and clean the input to search for it
        query=values.get(1)
        if len(query) == 0:
            query = 'Eiffel Tower'
        # Cleaning
        query_ = query.replace(" ", "_")
        query_list = []
        query_list[:0] = query_
        if query_list[0] == '_':
            del query_list[0]
        if query_list[-1] == '_':
            del query_list[-1]
        query_ = ''.join(query_list)

        # Search
        base = "http://dbpedia.org/resource/"
        search = base + query_
        print("Searching for ", query, " at ", search)
        to_print.append("Searching for "+ query+ " at "+search)
        search_info_graph.parse(search)
        if len(search_info_graph.serialize(format='n3').decode('utf-8')) == 0 or len(
                search_info_graph.serialize(format='n3').decode('utf-8')) == 1:
            print('Page not found')
            to_print.append('Page not found')
        # TODO Maybe search more info and add a way to print the predicate, ie openingDate : 1793 for Louvre query
        results = search_info_graph.query("""
               PREFIX dbo: <http://dbpedia.org/ontology/> 
               PREFIX s: <""" + search + """> 
               PREFIX dbp: <http://dbpedia.org/property/>
               SELECT ?abstract ?established ?openingDate
               WHERE {
                  ?s dbo:abstract ?abstract .
                  OPTIONAL {?s dbp:established ?established .}
                  OPTIONAL {?s dbo:openingDate ?openingDate .}
                  FILTER (lang(?abstract) = 'en')
               }""")
        if len(results) == 0 and len(to_print)==1:
            print("Nothing valuable has been found")
            to_print.append("Nothing valuable has been found")
        for element in results:
            for i in range(len(element)):
                if element[i] == None:
                    continue
                elif i == 0:
                    print('ABSTRACT : ',element[i])
                    to_print.append('ABSTRACT : '+element[i])
                elif i == 1 or i == 2:
                    print("Opening/Established in : ",element[i])
                    to_print.append("Opening/Established in : "+element[i])
                else:
                    print(element[i])  # print the element only
                    to_print.append(element[i])
        to_print = "\n".join(to_print)
        window['-TEXT-'].update(to_print)


    if event == "Show all Transport" :
        # If new type of transport, add one Union with bas:NewTransport
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
        # "Clean" the results to print only transport's name
        liste_t=[]
        for transport in all_transports:
            for s in range(len(transport)):
                s_ = str(transport[s]).split('#')
                if 'http://www.semanticweb.org/Paris_transport_ontologie' in s_:
                    s_.remove('http://www.semanticweb.org/Paris_transport_ontologie')
                if not s_:
                    sub = 'Paris_transport_ontologie'
                else:
                    sub = s_[0]
                #print(sub)  # print the element only
                liste_t.append(sub)
        liste_t="\n".join(liste_t)
        window['-TEXT-'].update(liste_t)


    if event == "Search Users":
        event, values = window.read()
        to_print=[]
        print(values.get(0))
        user_name=values.get(0)
        if len(user_name) == 0:
            user_name = 'Marie'
        # Cleaning
        user_name_ = user_name.replace(" ", "_")
        user_name_list = []
        user_name_list[:0] = user_name_
        if user_name_list[0] == '_':
            del user_name_list[0]
        if user_name_list[-1] == '_':
            del user_name_list[-1]
        user_name_ = ''.join(user_name_list)
        # query for user's name and return transports, depart, arrivee
        trajet = transport_graph.query(""" 
               PREFIX bas: <http://www.semanticweb.org/Paris_transport_ontologie#> 
               PREFIX owl: <http://www.w3.org/2002/07/owl#> 
               PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
               PREFIX xml: <http://www.w3.org/XML/1998/namespace> 
               PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

               SELECT ?bas
               WHERE {{
               ?bas bas:estDepartDe bas:"""+user_name_+""" .
               }
               UNION {
                ?bas bas:estUtilisePar bas:"""+user_name_+""" .  
               }
               UNION {
               ?bas bas:estArriveDe bas:"""+user_name_+""" .
               }
               }""")

        print(len(trajet))  # TODO Do not remove, otherwise, it will not show all the results
        if len(trajet)==0:
            to_print.append("User not found")

        # "Clean" the results to print only transport's name
        counter = 0
        for tra in trajet:
            if counter == 0:
                print("Departure : ", end='')
                to_print.append("Departure : ")
            elif counter == 1:
                print("Transports : \n    -", end='')
                to_print.append("Transports : \n    -")
            elif 1 == len(trajet) - counter:
                print("Arriving : ", end='')
                to_print.append("Arriving : ")
            else:
                print('    -', end='')
                to_print.append('    -')
            for s in range(len(tra)):
                s_ = str(tra[s]).split('#')
                if 'http://www.semanticweb.org/Paris_transport_ontologie' in s_:
                    s_.remove('http://www.semanticweb.org/Paris_transport_ontologie')
                if not s_:
                    sub = 'Paris_transport_ontologie'
                else:
                    sub = s_[0]
                print(sub)  # print the element only
                to_print.append(sub)
                to_print.append("&")
            counter += 1
        for idx,itm in enumerate(to_print):
            if itm =="&":
                to_print[idx]="\n"

        to_print = " ".join(to_print)
        window['-TEXT-'].update(to_print)

    if event =="Uber statistics for":
        quart=values.get('_LIST_')
        quart=str(quart[0])
        ye = values.get('_LIST1_')
        ye = str(ye[0])
        date_print=quart+' '+ye
        #convert to int
        ye_transf={'2017':"'17",'2018':"'18",'2019':"'19",'2020':"'20"}
        for i,j in ye_transf.items():
            if i==ye:
                ye=j
        search_uber=quart+ye
        dict_data_uber={"Q3'20":78,"Q2'20":55,"Q1'20":103,
                        "Q4'19":111,"Q3'19":103,"Q2'19":99,"Q1'19":93,
                        "Q4'18": 91, "Q3'18": 82, "Q2'18": 76, "Q1'18": 70,
                        "Q4'17": 68, "Q3'17": 62, "Q2'17": 57, "Q1'17": 49}
        #Source : https://www.statista.com/statistics/833743/us-users-ride-sharing-services/
        to_print_uber=[]
        to_print_uber.append('Uber had')
        for key, value in dict_data_uber.items():
            if key == search_uber:
                to_print_uber.append(str(value)+'M Users')
        to_print_uber.append('in '+date_print)
        if search_uber == "Q4'20":
            to_print_uber=['No Data']
        to_print_uber = " ".join(to_print_uber)
        window['-TEXT-'].update(to_print_uber)

    if event == sg.WIN_CLOSED:
        break
window.close()