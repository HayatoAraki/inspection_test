import PySimpleGUI as sg
import io
import os
import cv2
import glob
import json
import numpy as np
import edit


def make_rwindow(x=None, y=None):

    size_text = (15,1)
    size_input = (50,1)
    size_button = (10,1)

    filename = "./results.jpg"
    debug_text = "/Users/casa_arakih/Nextcloud/Araki/2021/inspection/test1111/img"

    col1 = [[sg.Text('Results direcory:', size=size_text),
             sg.InputText(debug_text, key='t1', size=size_input),
             sg.FolderBrowse(key='results', target='t1', size=size_button),
             sg.Button('Load', size=size_button)]]
    frame1 = sg.Frame('Files',
                      [
                          [sg.Table([[]],
                                    ['File Name', 'Defect'],
                                    col_widths=[30,5],
                                    auto_size_columns=False,
                                    select_mode=None,
                                    enable_events = True,
                                    num_rows=20,
                                    key='FILES',
                                    justification='left'
                                    )
                           ]
                      ]
                      )
    frame2 = sg.Frame('Defects',
                      [
                          [sg.Table([[]],
                                    ['No.', 'Possibility', 'Notes'],
                                    col_widths=[5,10,20],
                                    auto_size_columns=False,
                                    select_mode=None,
                                    num_rows=20,
                                    key='TABLE'
                                    )
                           ],
                          [sg.Button('+', size=(1,1)),
                           sg.Button('Edit', size=size_button)]
                      ]
                      )
    col2 = [[sg.Graph((800,600),(0,600),(800,0), key='GRAPH'),
             sg.Column([[frame1],[frame2]], justification='center')]]
    col3 = [[sg.Button('Exit', size=(10,1)),
             sg.Button('Settings', size=(10,1)),
             sg.Text('Alpha 0.01 2021.11.05')]]
    i_layout = [[sg.Text('Results window', font=('Arial', 18))],
                [sg.Column(col1, justification='left')],
                [sg.Column(col2, justification='center')],
                [sg.Column(col3, justification='center')]]



    return sg.Window("Check results | Cavity Defect Inspection", i_layout, finalize=True, size=(1200,750), location=(x,y))


def load_mark(path, filename, graph, data):

    #jsonfile = open(path + '/defects.json', 'r')
    #data = json.load(jsonfile)
    basename = os.path.basename(filename)
    defects = data[basename]['defect']
    defect_list = []
    
    for defect in defects:
        x1,y1,x2,y2 = defect['position']
        [sizex, sizey] = data[basename]['size']
        resized_x1 = 800 * x1 / sizex - 5
        resized_y1 = 600 * y1 / sizey - 5
        resized_x2 = 800 * x2 / sizex + 5
        resized_y2 = 600 * y2 / sizey + 5
        graph.draw_rectangle((resized_x1,resized_y1), (resized_x2,resized_y2), line_color="#FF0000", line_width=4)
        text_x = (resized_x1 + resized_x2)/2
        text_y = resized_y1-10
        graph.draw_text("No. " + str(defect['No']), (text_x,text_y), color="#FFFFFF")
        defect_list.append([defect['No'], str(defect['possibility']*100)+"%", defect['notes']])

    return defect_list


def file_table(defect_data, g_files):

    files = []
    for data in defect_data.values():
        files.append([data['filename'], len(data['defect'])])

    g_files.update(values=files)

    return 0
    
    
def select_image(row, path, g_graph, g_table, defect_data):

    file_list = list(defect_data.keys())
    filename = os.path.join(path,str(file_list[row]))

    img = cv2.imread(filename)
    resized = cv2.resize(img, dsize=(800,600))
    img_bytes = cv2.imencode('.png', resized)[1].tobytes()

    g_graph.erase()
    g_graph.draw_image(data=img_bytes, location=(0,0))
    defect_list = load_mark(path, filename, g_graph, defect_data)
    g_table.update(values=defect_list)
    
    return filename


def load_json(path):
    
    jsonfile = open(path + '/defects.json', 'r')
    data = json.load(jsonfile)

    return data


def main():
    
    rwindow = make_rwindow()
    filename = "results.jpg"
    graph = rwindow['GRAPH']
    files = rwindow['FILES']
    table = rwindow['TABLE']
    graph.draw_rectangle((0,0),(800,600), fill_color="#FFFFFF")
    rwindow.finalize()
    n = 0

    color_t1 = sg.theme_button_color(color = None)[0]
    color_t2 = sg.theme_button_color(color = None)[1]
    color_b1 = sg.theme_text_color(color = None)
    color_b2 = sg.theme_background_color(color = None)

    imgpath = None
    defect_data = None
    row_number = None

    #debug
    #rectangle = graph.draw_rectangle((300,200),(500,400), line_color="#FFFF00", line_width=4)
    
    while True:
        revent, rvalues = rwindow.read()
        
        if revent in (sg.WIN_CLOSED, 'Exit'):
            break
        elif revent == 'Load':
            imgpath = rvalues['t1']
            defect_data = load_json(imgpath)
            file_table(defect_data, files)
            
        elif revent == 'FILES':
            if rvalues['FILES'] != []:
                row_number = rvalues['FILES'][0]
                select_image(row_number, imgpath, graph, table, defect_data)
        
            
        elif revent == '+':
            print('"+" pressed')
            #pass

        elif revent == '-':
            pass
        
        elif revent == 'Edit':
            if rvalues['TABLE'] != []:
                defect_number = rvalues['TABLE'][0] + 1
                edit.main(row_number, defect_number, imgpath, defect_data)
                #pass


    
    rwindow.close()
