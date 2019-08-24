import tkinter as tk 
    #root.overrideredirect(1) # code to hide the title bar and outline

root = tk.Tk()
root.geometry("300x545+600+50") # widthxheight+xpos+ypos
root.wm_attributes("-transparentcolor","black") # code to make the color transparent
back_image = tk.PhotoImage(file='images/calculator.png')
tk.Label(root, image=back_image).place(x=0, y=0, width=300, height=545)

# common args
kwargs = {'master':root,'relief':'flat','bd':0,'highlightthickness':0}

# calc display
display_text = tk.StringVar()
display_text.set('0.0000')
tk.Label(**kwargs, textvariable=display_text, font=('Digital-7', 12, 'bold'), width=15, fg="red", 
    bg='#2D2C2D', anchor='e').place(x=80, y=103)

def Button(name, xpos, ypos, event):
    # helper function for creating buttons
    img = tk.PhotoImage(file='images/' + name + '.png')
    btn = tk.Button(**kwargs, image=img, command=lambda: event_click(event))
    btn.image = img # copy for garbage collection
    return btn.place(x=xpos, y=ypos)

# calculator buttons
Button('ce', 43, 221, 'ce'), Button('div', 99, 221, '/'), Button('times', 153, 221, '*')
Button('7', 42, 277, '7'),  Button('8', 98, 276, '8'), Button('9', 153, 276, '9'), Button('c', 210, 276, 'c')
Button('4', 43, 331, '4'),  Button('5', 97, 331, '5'), Button('6', 153, 331, '6'), Button('minus', 209, 331, '-')
Button('1', 43, 387, '1'),  Button('2', 98, 388, '2'), Button('3', 155, 388, '3'), Button('plus', 209, 388, '+')
Button('0', 44, 443, '0'),  Button('dot', 125, 443, '.'), Button('equal', 181, 443, '=')

''' calculator functions '''
# global variables
# design pattern :: 1,234.57 --> [front] . [back]
front = [] 
back = []
decimal = False
x_val = 0.0
y_val = 0.0
result = 0.0
operator = ''

def event_click(event):
    global operator, decimal, result
    if event in ['ce','e']:
        clear_click()
        update_display(0.0)
        operator = ''
        result = 0.0
    if event in ['0','1','2','3','4','5','6','7','8','9']:
        number_click(event)
    if event in ['*','/','+','-']:
        operator_click(event)
    if event == '.':
        decimal = True 
    if event == '=':
        calculate_click()

# helper functions
def update_display(display_value):
    global display_text
    ''' update the calc display with number click events, update with results, and update with error messages '''
    try: # to display float number
        display_text.set('{:,.4f}'.format(display_value))
    except: # to display error message
        display_text.set(display_value)

def format_number():
    ''' create a consolidated string of numbers from front and back number lists '''
    return ''.join(front) + '.' + ''.join(back)

# click events
def number_click(event):
    ''' add digit to front or back list when clicked '''
    global front, back
    if decimal:
        back.append(event)
    else:
        front.append(event)

    display_value = float(format_number())
    update_display(display_value)

def clear_click():
    ''' clear contents of front and back list, reset display, and reset decimal flag '''
    global front, back, decimal
    front.clear()
    back.clear()
    decimal = False

def operator_click(event):
    ''' set the operator based on the event button, this may also trigger a calculation in the event
        that the result is used in a subsequent operation '''
    global operator, x_val
    operator = event
    try: # if no x_val exists, use prior result
        x_val = float(format_number())
    except:
        x_val = result
    clear_click()

def calculate_click():
    ''' attempt to perform operation on x and y variables if exist '''
    global x_val, y_val, result

    # check for x value
    if not x_val:
        return 
    try: # check for y value
        y_val = float(format_number())
    except:
        y_val = 0.0
    try: # check for division by zero
        result = float(eval(str(x_val) + operator + str(y_val)))
        update_display(result)
    except ZeroDivisionError:
        error = "ERROR! DIV/0"
        x_val = 0.0
        clear_click()
        update_display(error)

    clear_click()

root.mainloop()