from guizero import App, TextBox, Text, PushButton, CheckBox
def text_box(app, disp:str, position:list, default):
    '''
    Takes in app as guizero application object, and then return the following to the caller of this function:
        label: a guizero Text object
        box : a guizero TextBox object
    '''
    if len(position) == 2:
        posbox = [position[0]+1, position[1]]
    else:
        print('Incorrect number of arguments to text_box.')
        return
    label =    Text(app, grid = position, text = disp,  align = 'left')
    box   = TextBox(app, grid=posbox,     text=str(default), align='left')
    box.text_size = 12
    return label, box