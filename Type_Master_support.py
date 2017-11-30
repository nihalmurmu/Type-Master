#! /usr/bin/env python
#
# Support module generated by PAGE version 4.9
# In conjunction with Tcl version 8.6
#    Nov 22, 2017 12:29:41 AM
#    Nov 22, 2017 01:58:09 AM

'''
   * Don't even try to understand this.
   * I wrote it, and I have no idea why it works.
   * But it does. My subconscious is that good.
'''

from PIL import ImageTk
import PIL.Image

import About.about
import About.about_support
import WPM.wpm
import WPM.wpm_support

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1


def set_Tk_var():
    global support_variable
    support_variable = Type_Master_Support_Variable()


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top
    icon = Image("photo", file="resource/icon/icon.png")
    root.tk.call('wm','iconphoto',root._w,icon)
    root.resizable(width=False, height=False)

    # disable the scrolling of TextBox
    w.TextBox.bind("<MouseWheel>", on_mousewheel)
    w.TextBox.bind("<Button-4>", on_mousewheel)
    w.TextBox.bind("<Button-5>", on_mousewheel)

    # bind the key events to root 
    """
    unbind the start key and call the timer, unbind itself and bind and call the 'key' function
    this way the timer only called during first key stroke
    + make sure to check the key so only alphabetic key is pressed
    """
    root.bind("<Key>",start_key)
    

    root.bind("<Return>",return_key)
    root.bind("<BackSpace>",backspace_key)
    root.bind("<space>",space_key)
    
    w.AboutButton.bind("<Button-1>", launch_about_window)
    w.ResetButton.config(command=reset_all)
    w.TimerLabel.config(textvariable=support_variable.TimerLabelVariable)
    w.WPMLabel.config(textvariable=support_variable.WpmLabelVariable)

    update_textBox()

    support_variable.lineEnd = int(w.TextBox.index("%d.0" %support_variable.rowCount + " lineend").split('.')[1])

    # underline tag
    w.TextBox.tag_config("underline", foreground = "red", underline=True)

    # wrong tag
    w.TextBox.tag_config("wrong", foreground = "red")

    # cursor tag
    w.TextBox.tag_config("cursor", background = "#9fd6ff")
    w.TextBox.configure(state=DISABLED)

    support_variable.TimerLabelVariable.set("Timer")
    support_variable.WpmLabelVariable.set("WPM")

    root.wait_visibility()



def reset_all():
    """ Reset all the necessary elements """

    support_variable.charCount = 0
    support_variable.columnCount = -1
    support_variable.rowCount = 1
    support_variable.remaining = -1
    support_variable.correctCharCount = 0
    support_variable.wrongCharCount = 0
    update_textBox()
    root.unbind("<Key")
    root.bind("<Key>",start_key)
    w.WordOption.configure(state=NORMAL)
    w.AboutButton.configure(state=NORMAL)
    support_variable.WpmLabelVariable.set("WPM")
    support_variable.TimerLabelVariable.set("Timer")

def update_textBox(*args):
    """ Update the textBox wrt to choice """

    return_symbol = u"\u23CE" + '\n' # for return symbol

    w.TextBox.configure(state=NORMAL)
    w.TextBox.delete('1.0', END)
    fileData = open("resource/data/"+support_variable.WordOptionChoices[support_variable.WordOptionVar.get()], 'r').read()
    support_variable.textLength = len(fileData)
    fileData = re.sub('\r?\n', return_symbol, fileData)
    w.TextBox.insert(INSERT, fileData)
    w.TextBox.configure(state=DISABLED)
    support_variable.rowCount = 1
    support_variable.columnCount = -1
    update_cursor("cursor",1)



def update_Finger():
    """ update the canvas with the required finger pictures """    

    textChar = w.TextBox.get("%d.%d" %(support_variable.rowCount, support_variable.columnCount), "%d.%d" %(support_variable.rowCount, support_variable.columnCount + 1))

    try:
        w.HandCanvas.delete(support_variable.img)
    except StandardError:
        pass

    if textChar.lower() in support_variable.key_1:
        support_variable.img = w.HandCanvas.create_image(35, 0, anchor=NW, image=support_variable.finger1)
        w.HandCanvas.image = support_variable.img

    elif textChar.lower() in support_variable.key_2:
        support_variable.img = w.HandCanvas.create_image(35, 0, anchor=NW, image=support_variable.finger2)
        w.HandCanvas.image = support_variable.img

    elif textChar.lower() in support_variable.key_3:
        support_variable.img = w.HandCanvas.create_image(35, 0, anchor=NW, image=support_variable.finger3)
        w.HandCanvas.image = support_variable.img

    elif textChar.lower() in support_variable.key_4:
        support_variable.img = w.HandCanvas.create_image(35, 0, anchor=NW, image=support_variable.finger4)
        w.HandCanvas.image = support_variable.img

    elif textChar.lower() in support_variable.key_5:
        support_variable.img = w.HandCanvas.create_image(35, 0, anchor=NW, image=support_variable.finger5)
        w.HandCanvas.image = support_variable.img

    elif textChar.lower() in support_variable.key_6:
        support_variable.img = w.HandCanvas.create_image(35, 0, anchor=NW, image=support_variable.finger6)
        w.HandCanvas.image = support_variable.img

    elif textChar.lower() in support_variable.key_7:
        support_variable.img = w.HandCanvas.create_image(35, 0, anchor=NW, image=support_variable.finger7)
        w.HandCanvas.image = support_variable.img

    elif textChar.lower() in support_variable.key_8:
        support_variable.img = w.HandCanvas.create_image(35, 0, anchor=NW, image=support_variable.finger8)
        w.HandCanvas.image = support_variable.img

    elif textChar.lower() in support_variable.key_9:
        support_variable.img = w.HandCanvas.create_image(35, 0, anchor=NW, image=support_variable.finger9)
        w.HandCanvas.image = support_variable.img


def on_mousewheel(event):
    return 'break'


def backspace_key(event):               #complete
    """handles the backspace key event"""

    if support_variable.columnCount:
        support_variable.charCount = support_variable.charCount - 1
        update_cursor("cursor",-1)

        if 'wrong' in w.TextBox.tag_names("%d.%d" %(support_variable.rowCount, support_variable.columnCount)):
            support_variable.wrongCharCount -= 1

        else:
            support_variable.correctCharCount -= 1

    elif support_variable.rowCount != 1:
        support_variable.charCount = support_variable.charCount - 1
        remove_tag("cursor")
        support_variable.rowCount = support_variable.rowCount - 1
        support_variable.columnCount = int(w.TextBox.index("%d.0" %support_variable.rowCount + " lineend").split('.')[1])
        update_cursor("cursor",-1)

        if 'wrong' in w.TextBox.tag_names("%d.%d" %(support_variable.rowCount, support_variable.columnCount)):
            support_variable.wrongCharCount -= 1

        else:
            support_variable.correctCharCount -= 1
    

    w.TextBox.tag_remove("wrong", "%d.%d" %(support_variable.rowCount, support_variable.columnCount), "%d.%d" %(support_variable.rowCount, support_variable.columnCount+1))

    if ' ' == w.TextBox.get("%d.%d" %(support_variable.rowCount, support_variable.columnCount), "%d.%d" %(support_variable.rowCount, support_variable.columnCount + 1)):
        remove_tag("underline")
        

    w.TextBox.see("%d.%d" %(support_variable.rowCount, support_variable.columnCount - 50))
    if support_variable.columnCount < 50:
        w.TextBox.see("%d.%d" %(support_variable.rowCount - 1,  int(w.TextBox.index("%d.0" %(support_variable.rowCount - 1) + " lineend").split('.')[1]) - 20 ))
                                           

def space_key(event):           
    """handles the spacebar key event"""

    support_variable.charCount = support_variable.charCount + 1

    if event.char == w.TextBox.get("%d.%d" %(support_variable.rowCount, support_variable.columnCount), "%d.%d" %(support_variable.rowCount, support_variable.columnCount + 1)):
        remove_tag("underline")
        support_variable.correctCharCount += 1

    else:
        add_tag("wrong")
        support_variable.wrongCharCount += 1

    scroll_textBox()
    update_cursor("cursor",1)



def return_key(event):                  # TODO: make it as a feature for the next build
    """handles the return key event"""

    
    support_variable.charCount = support_variable.charCount + 1
    r_var = u"\u23CE"

    # correct
    if w.TextBox.get("%d.%d" %(support_variable.rowCount,support_variable.columnCount),"%d.%d" %(support_variable.rowCount,support_variable.columnCount + 1)) == r_var: 
        remove_tag("cursor")

        # updating rowCount, charCount and columnCount

        support_variable.rowCount = support_variable.rowCount + 1
        support_variable.columnCount = -1

        support_variable.correctCharCount += 1

        # updating the lineEnd
        support_variable.lineEnd = int(w.TextBox.index("%d.0" %support_variable.rowCount + " lineend").split('.')[1])


        # scrolled one unit
        w.TextBox.yview_scroll(1,UNITS)
    # wrong
    else:
        support_variable.wrongCharCount += 1
        add_tag("wrong")
        scroll_textBox()

    update_cursor("cursor",1)


def scroll_textBox():
    w.TextBox.see("%d.%d" %(support_variable.rowCount, support_variable.columnCount + 60))
    if support_variable.lineEnd - support_variable.columnCount < 50:
        w.TextBox.see("%d.%d" %(support_variable.rowCount + 1, 10))


def update_cursor(tagid,direction):     # complete
    """update the cursor"""

    remove_tag(tagid)
    support_variable.columnCount += direction
    add_tag(tagid)
    update_Finger()


def add_tag(tagid):                   # complete
    """add the tag tagid"""

    w.TextBox.tag_add(tagid, "%d.%d" %(support_variable.rowCount,support_variable.columnCount), "%d.%d" %(support_variable.rowCount,support_variable.columnCount+1))
    

def remove_tag(tagid):                  #complete
    """remove the tag tagid"""

    w.TextBox.tag_remove(tagid, "%d.%d" %(support_variable.rowCount, support_variable.columnCount), "%d.%d" %(support_variable.rowCount, support_variable.columnCount+1))

def start_key(event):

    KeyRules = [
        event.char != '',           # ctrl,capslock,shift
        event.keycode != 119,       # delete
        event.keycode != 23,        # tab
        event.keycode != 9,         # escape
        event.keycode != 64         # alt
    ]

    

    if all(KeyRules):
        root.unbind("<Key>")
        root.bind("<Key>",key)

       
        w.WordOption.configure(state=DISABLED)
        w.AboutButton.configure(state=DISABLED)

        support_variable.Time = int(support_variable.TimeValue.get())
        timer(int(support_variable.TimeValue.get()))
        
        key(event)

    

def timer(remaining = None):

    if remaining is not None:
        support_variable.remaining = remaining
        

    if support_variable.remaining == -1:
        support_variable.remaining = 0

    elif support_variable.remaining == 0:
        support_variable.TimerLabelVariable.set("time's up")
        launch_wpm_window()
        w.ResetButton.invoke()

    else:
        mins, secs = divmod(support_variable.remaining, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        support_variable.TimerLabelVariable.set(str(timeformat))
        support_variable.remaining = support_variable.remaining - 1

        support_variable.WPM = int((((support_variable.correctCharCount - support_variable.wrongCharCount)/5)
                * support_variable.Time)
                / ((support_variable.Time - support_variable.remaining)
                * (support_variable.Time /60)))

        if support_variable.WPM <= 0:
            support_variable.WpmLabelVariable.set("0 WPM")

        else:
            support_variable.WpmLabelVariable.set(str(support_variable.WPM) + " WPM")
        
        root.after(1000, timer)


def key(event):                
    """ accepts a printable key , checks for the conditions and do the necessary operation"""

    KeyRules = [
        event.char != '',           # ctrl,capslock,shift
        event.keycode != 119,       # delete
        event.keycode != 23,        # tab
        event.keycode != 9,         # escape
        event.keycode != 64         # alt
    ]

    if all(KeyRules):

        support_variable.charCount = support_variable.charCount + 1

        w.TextBox.see("%d.%d" %(support_variable.rowCount, support_variable.columnCount + 60))
        if support_variable.lineEnd - support_variable.columnCount < 50:
            w.TextBox.see("%d.%d" %(support_variable.rowCount + 1, 10))

        if event.char == w.TextBox.get("%d.%d" %(support_variable.rowCount, support_variable.columnCount),"%d.%d" %(support_variable.rowCount, support_variable.columnCount + 1) ):
            remove_tag("wrong")
            remove_tag("underline")
            support_variable.correctCharCount += 1

        else:
            support_variable.wrongCharCount += 1

            # whitespace can be tagged wrong but it's not visible
            # this 'if' statement will check for whitespace and add a underline tag
            if w.TextBox.get("%d.%d" %(support_variable.rowCount, support_variable.columnCount),"%d.%d" %(support_variable.rowCount, support_variable.columnCount + 1)) == u' ':    # u' ' is space in unicode
                add_tag("underline")

            add_tag("wrong")
        
        # if key is pressed, but required was return
        # TODO: same block repeated in function return, optimize it
        if w.TextBox.get("%d.%d" %(support_variable.rowCount, support_variable.columnCount),"%d.%d" %(support_variable.rowCount, support_variable.columnCount + 1)) == u"\u23CE":
            remove_tag("cursor")
            support_variable.rowCount = support_variable.rowCount + 1
            support_variable.columnCount = -1
            support_variable.lineEnd = int(w.TextBox.index("%d.0" %support_variable.rowCount + " lineend").split('.')[1])
            w.TextBox.yview_scroll(1,UNITS)

           
        update_cursor("cursor",1)

        if support_variable.charCount == support_variable.textLength:
            print("ends")
            w.ResetButton.invoke()
            launch_wpm_window()


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


def launch_about_window(event):
    """ it will create and launch credit window """

    About.about.create_About(root, root)


def launch_wpm_window():
    """ it will launch wpm window """

    WPM.wpm.create_Result(root, root, support_variable.WPM)


class Type_Master_Support_Variable:
    def __init__(self):
        self.TimeValue = StringVar()
        self.TimerLabelVariable = StringVar()
        self.WpmLabelVariable = StringVar()
        self.WordOptionVar = StringVar()
        self.WordOptionChoices = {'Oakhurst curse': '1.dat' , 'The Dog': '2.dat', 'The Whistle': '3.dat', \
                            'Reginald Worries': '4.dat', 'Wicked Prince': '5.dat'}
        self.WordOptionVar.set(list(self.WordOptionChoices.keys())[1])
        self.rowCount = 1
        self.columnCount = -1
        self.charCount = 0              #incase its end of the text, this will call the wpm window
        self.lineEnd = 0
        self.textLength = 0

        self.correctCharCount = 0
        self.wrongCharCount = 0

        self.Time = 0

        self.key_1 = {'1','q','a','z'}
        self.key_2 = {'2','w','s','x'}
        self.key_3 = {'3','e','d','c'}
        self.key_4 = {'4','r','f','v','5','t','g','b'}
        self.key_5 = {' '}
        self.key_6 = {'6','y','h','n','7','u','j','m'}
        self.key_7 = {'8','i','k',','}
        self.key_8 = {'9','o','l','.'}
        self.key_9 = {'0','p',':',';','/',"'",'"','?','<','>',u"\u23CE"}

        self.finger1 = ImageTk.PhotoImage(PIL.Image.open("resource/fingers/f1.png"))
        self.finger2 = ImageTk.PhotoImage(PIL.Image.open("resource/fingers/f2.png"))
        self.finger3 = ImageTk.PhotoImage(PIL.Image.open("resource/fingers/f3.png"))
        self.finger4 = ImageTk.PhotoImage(PIL.Image.open("resource/fingers/f4.png"))
        self.finger5 = ImageTk.PhotoImage(PIL.Image.open("resource/fingers/f5.png"))
        self.finger6 = ImageTk.PhotoImage(PIL.Image.open("resource/fingers/f6.png"))
        self.finger7 = ImageTk.PhotoImage(PIL.Image.open("resource/fingers/f7.png"))
        self.finger8 = ImageTk.PhotoImage(PIL.Image.open("resource/fingers/f8.png"))
        self.finger9 = ImageTk.PhotoImage(PIL.Image.open("resource/fingers/f9.png"))

        self.img = None
        
        self.remaining = 0

        self.WPM = 0


if __name__ == '__main__':
    import Type_Master
    Type_Master.vp_start_gui()