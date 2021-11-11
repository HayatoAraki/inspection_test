import PySimpleGUI as sg
import inspection
import results
import edit
import cv2


width=20
height=1
sg.theme('DarkGray9')

col1 = [
          [sg.Button('Start inspection', size=(width,height))],
          [sg.Button('Check results', size=(width,height))],
          [sg.Button('Learn', size=(width,height))],
    ]

col2 = [
    [sg.Button('Exit', size=(10,1)),
     sg.Button('Settings', size=(10,1)),
     sg.Text('Alpha 0.01 2021.11.05')]
    ]

layout = [[sg.Text('Cabvity Defect Inspection', font=('Arial',22), pad=((8,8),(8,16)))],
          [sg.Column(col1, justification='center')],
          [sg.Column(col2, justification='center')]
          ]

window = sg.Window('Main Window | Cavity Defect Inspection', layout, size = (450,200))

while True: # Event loop
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Start inspection':
        
        iwindow = inspection.make_iwindow()
        
        while True:
            ievent, ivalues = iwindow.read()
            if ievent in (sg.WIN_CLOSED, 'Exit'):
                break
            
        iwindow.close()

    elif event == 'Check results':

        results.main()
        

window.close()
