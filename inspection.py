import PySimpleGUI as sg

def make_iwindow(x=None, y=None):

    MyList = ["fig1", "fig2", "fig3", "fig4", "fig5"]
    
    size_text = (15,1)
    size_input = (50,1)
    size_button = (10,1)

    subcol1 = [[sg.Text('Image directory:', size=size_text),
                sg.InputText(key='t1', size=size_input),
                sg.FolderBrowse(key='input', target='t1', size=size_button)]]
    subcol2 = [[sg.Text('Model file:', size=size_text),
                sg.InputText(key='t2', size=size_input),
                sg.FileBrowse(key='model', target='t2', size=size_button)]]
    subcol3 = [[sg.Text('Output directory:', size=size_text),
                sg.InputText(key='t3', size=size_input),
                sg.FolderBrowse(key='output', target='t3', size=size_button)]]
    col1 = [[sg.Column(subcol1)], [sg.Column(subcol2)], [sg.Column(subcol3)]]
    col2 = [[sg.Button('Start inspection', size=(20,1))]]
    subcol4 = [[sg.ProgressBar(len(MyList), orientation='h', size=(40,20), key='-prog-'),
                sg.Text('00%', size=(10,1))]]
    subcol5 = [[sg.Button('Check results', size=(20,1), disabled=True)]]
    col3 = [[sg.Column(subcol4)], [sg.Column(subcol5, justification='center')]]
    col4 = [[sg.Button('Exit', size=(10,1)),
             sg.Button('Settings', size=(10,1)),
             sg.Text('Alpha 0.01 2021.11.05')]]
    i_layout = [[sg.Text('Inspection window', font=('Arial',18))],
                [sg.Column(col1, justification='center')],
                [sg.Column(col2, justification='center')],
                [sg.Column(col3, justification='center', pad=(10,30))],
                [sg.Column(col4, justification='center')]]
                
    return sg.Window("Start Inspection | Cavity Defect Inspection", i_layout, finalize=True, size=(600,360), location=(x, y))
