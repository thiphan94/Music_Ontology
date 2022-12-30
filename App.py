from datetime import datetime
import rdflib
from rdflib import Graph, URIRef
from rdflib.tools import csv2rdf
from SPARQLWrapper import SPARQLWrapper, JSON

music_graph = Graph()
music_graph.parse("Projet_music_rdf_xlm.owl")

import PySimpleGUI as sg


sg.theme('DarkGrey1')   # Add a touch of color

col = [[sg.Frame(layout=[[sg.Multiline("This application will be a search engine to music ontology :\n   - Show all artistes available\n   - Search informations with query.",key='-TEXT-',size=(400,30),font=("Helvetica", 12), text_color='black',)]],
        title='Informations:')]]


layout = [
    [sg.Frame(layout=[[sg.Button("Show all Artistes",size=(31,1))],
    [sg.Text('Genre', size=(15, 1), auto_size_text=False, justification='right'), sg.InputCombo(['Classic', 'Rock', 'Hiphop', 'Rap', 'Pop','Blues','Dixieland','House','Jazz','R&B','Soul','Traditional pop'], enable_events=True, key='combogenre',size=(20, 3))],
    [sg.Text('Instrument', size=(15, 1), auto_size_text=False, justification='right'), sg.InputCombo(['Guitar', 'Piano', 'Drums', 'Violin','Vocals'], enable_events=True, key='comboinstrument',size=(20, 3))],
    [sg.Text('Certification', size=(15, 1), auto_size_text=False, justification='right'), sg.InputCombo(['Diamond', 'Gold', 'Platinum'], enable_events=True, key='combocertification',size=(20, 3))],
    [sg.Button("Search"),sg.Text('',key='-Search-4')],
    [sg.Button("Exit")]
    ], title='Interface:'), sg.Column(col)],
]
# Create the window
window = sg.Window("Music Ontology", layout,size=(1080,550),return_keyboard_events=True)


# Create an event loop
while True:
    event, values = window.read()
    for i,j in values.items():
        print(i,j)

    #Search all Artistes
    if event == "Show all Artistes" :
        # If new type of transport, add one Union with bas:NewTransport
        all_transports = music_graph.query("""
               PREFIX bas: <http://www.semanticweb.org/music_ontologie#>
               PREFIX owl: <http://www.w3.org/2002/07/owl#>
               PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
               PREFIX xml: <http://www.w3.org/XML/1998/namespace>
               PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

               SELECT ?bas
               WHERE {{
                ?bas rdf:type bas:Composer .
               }
               UNION {
                ?bas rdf:type bas:Author .
               }
               UNION {
                ?bas rdf:type bas:Interpreter .
               }}

               """)
        # "Clean" the results to print only transport's name
        liste_t=[]
        for transport in all_transports:
            for s in range(len(transport)):
                s_ = str(transport[s]).split('#')
                if 'http://www.semanticweb.org/music_ontologie' in s_:
                    s_.remove('http://www.semanticweb.org/music_ontologie')
                if not s_:
                    sub = 'music_ontologie'
                else:
                    sub = s_[0]
                #print(sub)  # print the element only
                liste_t.append(sub)
        liste_t="\n".join(liste_t)
        window['-TEXT-'].update(liste_t)


    

    
#Search Artiste by combo
    if event == "Search":
        event, values = window.read()
        
        print("test",values)
        input = [values['combogenre'],values['comboinstrument'],values['combocertification']]
        print("test2",input)
        to_print=[]
        if input[0]=='':
            if input[1]=='':
                search = music_graph.query("""
                    PREFIX bas: <http://www.semanticweb.org/music_ontologie#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX xml: <http://www.w3.org/XML/1998/namespace>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                    SELECT DISTINCT ?album
                    WHERE {
                    ?bas bas:hasAlbum ?album .
                    ?album bas:hasCertification bas:"""+input[2]+"""
                    }""")
            elif input[2]=='':
                search = music_graph.query("""
                    PREFIX bas: <http://www.semanticweb.org/music_ontologie#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX xml: <http://www.w3.org/XML/1998/namespace>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                    SELECT DISTINCT ?bas
                    WHERE {
                    ?bas bas:hasInstrument bas:"""+input[1]+""" .
                    }""")

            else:
                search = music_graph.query("""
                        PREFIX bas: <http://www.semanticweb.org/music_ontologie#>
                        PREFIX owl: <http://www.w3.org/2002/07/owl#>
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX xml: <http://www.w3.org/XML/1998/namespace>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                        SELECT DISTINCT ?bas ?album
                        WHERE {
                        ?bas bas:hasInstrument bas:"""+input[1]+""" .
                        ?bas bas:hasAlbum ?album .
                        ?album bas:hasCertification bas:"""+input[2]+"""
                        }""")

        elif input[1]=='':
            if input[2]=='':
                search = music_graph.query("""
                    PREFIX bas: <http://www.semanticweb.org/music_ontologie#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX xml: <http://www.w3.org/XML/1998/namespace>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                    SELECT DISTINCT ?bas 
                    WHERE {
                    ?bas bas:hasGenre bas:"""+input[0]+""" .
                    }""")

            else:
                search = music_graph.query("""
                    PREFIX bas: <http://www.semanticweb.org/music_ontologie#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX xml: <http://www.w3.org/XML/1998/namespace>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                    SELECT DISTINCT ?bas ?album
                    WHERE {
                    ?bas bas:hasGenre bas:"""+input[0]+""" .
                    ?bas bas:hasAlbum ?album .
                    ?album bas:hasCertification bas:"""+input[2]+"""
                    }""")                
        
        elif input[2]=='':
            search = music_graph.query("""
                    PREFIX bas: <http://www.semanticweb.org/music_ontologie#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX xml: <http://www.w3.org/XML/1998/namespace>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                    SELECT DISTINCT ?bas 
                    WHERE {
                    ?bas bas:hasGenre bas:"""+input[0]+""" .
                    ?bas bas:hasInstrument bas:"""+input[1]+""" 
                    }""")
    
        else:
            search = music_graph.query("""
                    PREFIX bas: <http://www.semanticweb.org/music_ontologie#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX xml: <http://www.w3.org/XML/1998/namespace>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                    SELECT DISTINCT ?bas ?album
                    WHERE {
                    ?bas bas:hasGenre bas:"""+input[0]+""" .
                    ?bas bas:hasInstrument bas:"""+input[1]+""" .
                    ?bas bas:hasAlbum ?album .
                    ?album bas:hasCertification bas:"""+input[2]+"""
                    }""")
        print(len(search))  # TODO Do not remove, otherwise, it will not show all the results
        
        if len(search)==0:
            to_print.append("Not found!")
        list_result =[]
        # Print results
        for tra in search:
            counter=0

            for s in range(len(tra)):
                
                s_ = str(tra[s]).split('#')
                if 'http://www.semanticweb.org/music_ontologie' in s_:
                    s_.remove('http://www.semanticweb.org/music_ontologie')
                if not s_:
                    sub = 'music_ontologie'
                else:
                    sub = s_[0]
                print(sub)  # print the element only
                list_result.append(sub)
                #print only artiste and album
                if input[0]=='':
                    if input[1] == '':   
                        to_print.append("Album:")
                        to_print.append(" ")
                        to_print.append(sub)
                        to_print.append("&")
                    elif input[2] == '':
                        to_print.append("Artiste:")
                        to_print.append(" ")
                        to_print.append(sub)
                        to_print.append("&")
                    else:
                        if counter == 0:
                            to_print.append("Artiste:")
                            to_print.append(" ")
                            to_print.append(sub)
                            to_print.append(", ")
                        elif counter == 1:
                            to_print.append("Album:")
                            to_print.append(" ")
                            to_print.append(sub)
                            to_print.append("&")
                elif input[1]=='':
                    if input[2] == '':
                        to_print.append("Artiste:")
                        to_print.append(" ")
                        to_print.append(sub)
                        to_print.append("&")
                    else:
                        if counter == 0:
                            to_print.append("Artiste:")
                            to_print.append(" ")
                            to_print.append(sub)
                            to_print.append(", ")
                        elif counter == 1:
                            to_print.append("Album:")
                            to_print.append(" ")
                            to_print.append(sub)
                            to_print.append("&")
                elif input[2]=='':
                    to_print.append("Artiste:")
                    to_print.append(" ")
                    to_print.append(sub)
                    to_print.append("&")
                else:
                    if counter == 0:
                        to_print.append("Artiste:")
                        to_print.append(" ")
                        to_print.append(sub)
                        to_print.append(", ")
                    elif counter == 1:
                        to_print.append("Album:")
                        to_print.append(" ")
                        to_print.append(sub)
                        to_print.append("&")
                
                counter += 1
        #Write results to file
        # datetime object containing current date and time
        now = datetime.now()
        with open("result.txt", "a") as text_file:
            text_file.write(str(now) + ", " + "Query: keywords " + str(input) + "\n" +"Result(s) "+ str(list_result) + "\n" + "\n")
            text_file.close()

        for idx,itm in enumerate(to_print):
            if itm =="&":
                to_print[idx]="\n"

        to_print = " ".join(to_print)
        window['-TEXT-'].update(to_print)
        
    
    # If user closed window with X or if user clicked "Exit" button then exit
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
window.close()