import PySimpleGUI as sg
import os
import cv2


def make_window(n, data, image_size):


    size1 = (12,1)
    size2 = (8,1)
    e_graph = sg.Graph(image_size,(0,image_size[1]),(image_size[0],0),key='E_GRAPH')
    row1 = [[sg.Text('x1', size=size1),sg.InputText('000', size=size2, key='X1')]]
    row2 = [[sg.Text('y1', size=size1),sg.InputText('000', size=size2, key='Y1')]]
    row3 = [[sg.Text('x2', size=size1),sg.InputText('000', size=size2, key='X2')]]
    row4 = [[sg.Text('y2', size=size1),sg.InputText('000', size=size2, key='Y2')]]
    row5 = [[sg.Text('Possibility (%)', size=size1),sg.InputText('000', size=size2, key='PS')]]
    subcol1 = sg.Frame(f'No. {n}',
                       [
                           [sg.Column(row1, justification='center')],
                           [sg.Column(row2, justification='center')],
                           [sg.Column(row3, justification='center')],
                           [sg.Column(row4, justification='center')],
                           [sg.Column(row5, justification='center')],
                           [sg.Text('Notes:')],
                           [sg.InputText(key='NOTES', size=(23,1))]
                       ]
                       )
    #col1 = [[e_graph, sg.Column(subcol1, justification='center')]]
    col1 = [[e_graph, subcol1]]
    col2 = [
        [sg.Button('Exit', size=(10,1)),
         sg.Button('Settings', size=(10,1)),
         sg.Text('Alpha 0.01 2021.11.05')]
    ]
    layout = [[sg.Text("Edit window", font=('Arial', 18))],
              [sg.Column(col1, justification='center')],
              [sg.Column(col2, justification='center')]]
    
    window = sg.Window('Edit', layout, finalize=True, size=(1400,930))

    return window


def init(row, n, path, data, e_img_bytes, e_window, dsize):

    file_list = list(data.keys())
    filename = os.path.join(path,str(file_list[row]))
    basename = file_list[row]
    defects = data[basename]['defect']
    position = [0,0,0,0]
    size = [0,0]
    possibility = 0
    notes = "Empty"

    graph = e_window['E_GRAPH']
    graph.erase()
    graph.draw_image(data=e_img_bytes, location=(0,0))
    
    for defect in defects:
        if defect['No'] == n:
            position = defect['position']
            [sizex, sizey] = data[basename]['size']
            resized_x1 = dsize[0] * position[0] / sizex - 5
            resized_y1 = dsize[1] * position[1] / sizey - 5
            resized_x2 = dsize[0] * position[2] / sizex + 5
            resized_y2 = dsize[1] * position[3] / sizey + 5
            possibility = defect['possibility']
            notes = defect['notes']
            graph.draw_rectangle((resized_x1,resized_y1), (resized_x2,resized_y2), line_color="#FF0000", line_width=5)
            
    e_window['X1'].update(position[0])            
    e_window['Y1'].update(position[1])            
    e_window['X2'].update(position[2])            
    e_window['Y2'].update(position[3])
    e_window['PS'].update(possibility*100)
    e_window['NOTES'].update(notes)

    return 0
    

def main(row, n, path, data):

    image_size = (1120,840)
    
    window = make_window(n, data, image_size)
    graph = window['E_GRAPH']

    file_list = list(data.keys())
    filename = os.path.join(path, str(file_list[row]))
    img = cv2.imread(filename)
    resized = cv2.resize(img, dsize=image_size)
    img_bytes = cv2.imencode('.png', resized)[1].tobytes()
    init(row, n, path, data, img_bytes, window, image_size)
    #graph.draw_rectangle((0,0),image_size, fill_color="#FFFFFF")

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

    window.close()
    
    return 0
