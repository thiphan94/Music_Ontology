# hello_psg.py
#Transport LIST
import rdflib
from rdflib import Graph, URIRef
from rdflib.tools import csv2rdf
from SPARQLWrapper import SPARQLWrapper, JSON

music_graph = Graph()
music_graph.parse("Projet_music_rdf_xlm.owl")

#uber_graph= Graph()
#uber_graph.parse("Uber_Paris.owl")
quarter=['Q1', 'Q2', 'Q3', 'Q4']
year=['2017', '2018', '2019', '2020']
import PySimpleGUI as sg


sg.theme('DarkGrey1')   # Add a touch of color

col = [[sg.Frame(layout=[[sg.Multiline("This application will be a search engine to music ontology :\n   - Show all artistes available\n   - Search informations with query.",key='-TEXT-',size=(500,30),font=("Helvetica", 12), text_color='black',)]],
        title='Informations:')]]


layout = [
    [sg.Frame(layout=[[sg.Button("Show all Artistes",size=(31,1))],
    [sg.Text('Gnere', size=(15, 1), auto_size_text=False, justification='right'), sg.InputCombo(['Classic', 'Rock', 'Hiphop', 'Rap', 'Pop'], enable_events=True, key='combogenre',size=(20, 3))],
    [sg.Text('Instrument', size=(15, 1), auto_size_text=False, justification='right'), sg.InputCombo(['Guitar', 'Piano', 'Drums', 'Violin','Vocals'], enable_events=True, key='comboinstrument',size=(20, 3))],
    [sg.Text('Album Certification', size=(15, 1), auto_size_text=False, justification='right'), sg.InputCombo(['Diamond', 'Gold', 'Platinum'], enable_events=True, key='combocertification',size=(20, 3))],
    [sg.Button("Search"),sg.Text('',key='-Search-4')]
    ], title='Interface:'), sg.Column(col)],
]
# Create the window
window = sg.Window("Music Ontology", layout,size=(1080,550),return_keyboard_events=True)


sparql = SPARQLWrapper("http://dbpedia.org/sparql")

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


    #Search Artiste by instrument
    if event == "Instrument":
        event, values = window.read()
        instrument = values['comboinstrument']
        print(instrument)
        to_print=[]
        # print(values.get(0))
        # instrument=values.get(0)
        # print(len(instrument))
        # if len(instrument) == 0:
        #     instrument = 'Marie'
        # # Cleaning
        instrument_ = instrument.replace(" ", "_")
        instrument_list = []
        instrument_list[:0] = instrument_
        if instrument_list[0] == '_':
            del instrument_list[0]
        if instrument_list[-1] == '_':
            del instrument_list[-1]
        instrument_ = ''.join(instrument_list)
        # query for type of instrument and return Artiste who play this instrument
        search = music_graph.query("""
               PREFIX bas: <http://www.semanticweb.org/music_ontologie#>
               PREFIX owl: <http://www.w3.org/2002/07/owl#>
               PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
               PREFIX xml: <http://www.w3.org/XML/1998/namespace>
               PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

               SELECT ?bas
               WHERE {{
               ?bas bas:primaryinstrument bas:"""+instrument_+""" .
               }}""")

        print(len(search))  # TODO Do not remove, otherwise, it will not show all the results
        if len(search)==0:
            to_print.append("Not found!")

        # Print results
        strx="Artiste use " + str(instrument_) +": "
        to_print.append(strx)
        to_print.append("&")
        for tra in search:
            for s in range(len(tra)):
                s_ = str(tra[s]).split('#')
                if 'http://www.semanticweb.org/music_ontologie' in s_:
                    s_.remove('http://www.semanticweb.org/music_ontologie')
                if not s_:
                    sub = 'music_ontologie'
                else:
                    sub = s_[0]
                print(sub)  # print the element only
                to_print.append(sub)
                to_print.append("&")
        #     counter += 1
        for idx,itm in enumerate(to_print):
            if itm =="&":
                to_print[idx]="\n"

        to_print = " ".join(to_print)
        window['-TEXT-'].update(to_print)


    
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
                    ?bas bas:primaryinstrument bas:"""+input[1]+""" .
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
                        ?bas bas:primaryinstrument bas:"""+input[1]+""" .
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
                    ?bas bas:primaryinstrument bas:"""+input[1]+""" 
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
                    ?bas bas:primaryinstrument bas:"""+input[1]+""" .
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
        file = open("result.txt", "w")
        file.write("Query: search by " + str(input) + "\n" +"Result(s) "+ str(list_result) + "\n")
        file.close()
        file1 = open('result.txt', 'r')
        print(file1.read())
        file1.close()

        for idx,itm in enumerate(to_print):
            if itm =="&":
                to_print[idx]="\n"

        to_print = " ".join(to_print)
        window['-TEXT-'].update(to_print)
        
        #Search Artiste by genre
    if event == "Genre":
        event, values = window.read()
        to_print=[]
        print(values.get(0))
        genre=values.get(0)
        if len(genre) == 0:
            genre = 'Marie'
        # Cleaning
        genre_ = genre.replace(" ", "_")
        genre_list = []
        genre_list[:0] = genre_
        if genre_list[0] == '_':
            del genre_list[0]
        if genre_list[-1] == '_':
            del genre_list[-1]
        genre_ = ''.join(genre_list)
        # query for user's name and return transports, depart, arrivee
        search = music_graph.query("""
               PREFIX bas: <http://www.semanticweb.org/music_ontologie#>
               PREFIX owl: <http://www.w3.org/2002/07/owl#>
               PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
               PREFIX xml: <http://www.w3.org/XML/1998/namespace>
               PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

               SELECT ?bas
               WHERE {{
               ?bas bas:hasGenre bas:"""+genre_+""" .
               }}""")

        print(len(search))  # TODO Do not remove, otherwise, it will not show all the results
        if len(search)==0:
            to_print.append("User not found")

        # "Clean" the results to print only transport's name
        counter = 0
        for tra in search:
            if counter == 0:
                print("Artiste : ", end='')
                to_print.append("Artiste : ")
            elif counter == 1:
                print("Instrument : \n    -", end='')
                to_print.append("Instrument : \n    -")
            else:
                print('    -', end='')
                to_print.append('    -')
            for s in range(len(tra)):
                s_ = str(tra[s]).split('#')
                if 'http://www.semanticweb.org/music_ontologie' in s_:
                    s_.remove('http://www.semanticweb.org/music_ontologie')
                if not s_:
                    sub = 'music_ontologie'
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

    

    if event == sg.WIN_CLOSED:
        break
window.close()