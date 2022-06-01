from unittest import TextTestResult
import wx
import wx.glcanvas as wxcanvas
from OpenGL import GL, GLUT
import numpy as np
import wx.lib.scrolledpanel as scrolled



class MyGLCanvas(wxcanvas.GLCanvas):

    def __init__(self, parent,id,pos,size):
        """Initialise canvas properties and useful variables."""
        super().__init__(parent, -1,pos=pos,size=size,
                         attribList=[wxcanvas.WX_GL_RGBA,
                                     wxcanvas.WX_GL_DOUBLEBUFFER,
                                     wxcanvas.WX_GL_DEPTH_SIZE, 16, 0])
        GLUT.glutInit()
        self.init = False
        self.context = wxcanvas.GLContext(self)

        # Initialise variables for panning
        self.pan_x = 0
        self.pan_y = 0

        # Initialise variables for zooming
        self.zoom = 1

        # Bind events to the canvas
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)


    def init_gl(self):
        """Configure and initialise the OpenGL context."""
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        GL.glDrawBuffer(GL.GL_BACK)
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glViewport(0, 0, size.width, size.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, size.width, 0, size.height, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslated(self.pan_x, self.pan_y, 0.0)
        GL.glScaled(self.zoom, self.zoom, self.zoom)

    def render(self, text):
        """Handle all drawing operations."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # Draw specified text at position (10, 10)
        self.render_text(text, 10, 10)

        # Draw a sample signal trace

        
        GL.glColor3f(0.0, 0.0, 1.0)  # signal trace is blue   Colour

        
        #Trace drawing


        #Test trace data
        """
        data  = [(i//5) % 2  for i in range(20)]

        GL.glBegin(GL.GL_LINE_STRIP)
        for i,val in enumerate(data):
            y = 100 + val*25
            x = (i * 20) + 10
            x_next = (i * 20) + 30
           
            GL.glVertex2f(x, y)
            GL.glVertex2f(x_next, y)
        GL.glEnd()



        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range(20):
            x = (i * 20) + 10
            x_next = (i * 20) + 30
            if i % 2 == 0:
                y = 150
            else:
                y = 175
            GL.glVertex2f(x, y)
            GL.glVertex2f(x_next, y)
        GL.glEnd()"""

        # We have been drawing to the back buffer, flush the graphics pipeline
        # and swap the back buffer to the front
        GL.glFlush()
        self.SwapBuffers()

    def clear_canvas(self):
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True
        GL.glClearColor(255,255,255,0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glFlush()
        self.SwapBuffers()


    def draw_trace(self):
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        GL.glColor3f(0.0, 0.0, 1.0)  # signal trace is blue   Colour

        
        #Trace drawing


        #Test trace data

        data  = [(i//5) % 2  for i in range(20)]

        GL.glBegin(GL.GL_LINE_STRIP)
        for i,val in enumerate(data):
            y = 100 + val*25
            x = (i * 20) + 10
            x_next = (i * 20) + 30
           
            GL.glVertex2f(x, y)
            GL.glVertex2f(x_next, y)
        GL.glEnd()



        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range(20):
            x = (i * 20) + 10
            x_next = (i * 20) + 30
            if i % 2 == 0:
                y = 150
            else:
                y = 175
            GL.glVertex2f(x, y)
            GL.glVertex2f(x_next, y)
        GL.glEnd()

        # We have been drawing to the back buffer, flush the graphics pipeline
        # and swap the back buffer to the front
        GL.glFlush()
        self.SwapBuffers()

    def on_paint(self, event):
        """Handle the paint event."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        size = self.GetClientSize()
        text = "".join(["Canvas redrawn on paint event, size is ",
                        str(size.width), ", ", str(size.height)])
        self.render(text)

    def on_size(self, event):
        """Handle the canvas resize event."""
        # Forces reconfiguration of the viewport, modelview and projection
        # matrices on the next paint event
        self.init = False

    def render_text(self, text, x_pos, y_pos):
        """Handle text drawing operations."""
        GL.glColor3f(0.0, 0.0, 0.0)  # text is black
        GL.glRasterPos2f(x_pos, y_pos)
        font = GLUT.GLUT_BITMAP_HELVETICA_12

        for character in text:
            if character == '\n':
                y_pos = y_pos - 20
                GL.glRasterPos2f(x_pos, y_pos)
            else:
                GLUT.glutBitmapCharacter(font, ord(character))





class Gui(wx.Frame):
    def __init__(self, title):
        """Initialise widgets and layout."""
        super().__init__(parent=None, title=title, size=(800, 600))

        # Configure the file menu
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        self.scrollable = wx.ScrolledCanvas(self, wx.ID_ANY )
        self.scrollable.SetSizeHints(200, 200)
        self.scrollable.ShowScrollbars(wx.SHOW_SB_ALWAYS,wx.SHOW_SB_DEFAULT)
        self.scrollable.SetScrollbars(20, 20, 0, 0)
        


        #Switch Panel

        self.panel = wx.ScrolledWindow(self,wx.ID_ANY,pos=(25,50),size = (300,175))
        self.panel.SetBackgroundColour('White')

        switch_x = 10
        switch_y = 10
        n = 12 #number of switches

        self.text = wx.StaticText(self.panel, wx.ID_ANY, "Switches",pos = (switch_x,switch_y))
        self.text = wx.StaticText(self.panel, wx.ID_ANY, "Current State",pos = (switch_x+70,switch_y))
        self.text = wx.StaticText(self.panel, wx.ID_ANY, "Change State",pos = (switch_x+170,switch_y))


        self.panel.ShowScrollbars(wx.SHOW_SB_ALWAYS,wx.SHOW_SB_DEFAULT)
        self.panel.SetScrollbars(20, 10, 0, 4.5*n)

        self.list_of_change_buttons = []
        #self.change_button = wx.Button(self.panel, wx.ID_ANY, "Change",pos = (switch_x+170,50+ 40))

        list_of_switch_names = [f'S{i+1}' for i in range(n)] #Switch name generation


        #self.list_of_panels = [wx.Panel(self.panel,wx.ID_ANY,pos=(switch_x+70,50+40*i),size=(80,20)) for i in range(n)]

        #self.colour_panel = wx.Panel(self.panel,wx.ID_ANY,pos=(switch_x+70,50),size=(80,20))
        #self.colour_panel.SetBackgroundColour('Red')

        list_of_switch_values = [0 for i in range(n)]
        self.list_of_switch_text_values = []

        for i in range(n):
            self.list_of_change_buttons.append(wx.Button(self.panel, wx.ID_ANY, "Change",pos = (switch_x+170,50+ 40*i)))
            self.text = wx.StaticText(self.panel, wx.ID_ANY, list_of_switch_names[i],pos = (switch_x+20,50+40*i))

            #self.list_of_panels[i].SetBackgroundColour('Red')

            self.list_of_switch_text_values.append(wx.StaticText(self.panel, wx.ID_ANY,str(list_of_switch_values[i]),pos = (switch_x+105,50+40*i)))



        #self.panel.Bind(wx.EVT_PAINT, self.OnPaint)





        # Configure the widgets

        #buttons as part o widgets
        button1_x = 550
        button1_y = 300

        self.button_run = wx.Button(self, wx.ID_ANY, "Run",pos = (button1_x,button1_y))
        self.button_continue = wx.Button(self, wx.ID_ANY, "Continue",pos = (button1_x,button1_y +50))
        self.button_Add_Monitor = wx.Button(self, wx.ID_ANY, "Add Monitor",pos = (button1_x,button1_y+100))
        self.button_Remove_Monitor = wx.Button(self, wx.ID_ANY, "Remove Monitor",pos = (button1_x,button1_y+150))
        self.button_Quit = wx.Button(self, wx.ID_ANY, "Quit",pos = (button1_x,button1_y+200))

        

        #Controls/menus for buttons

        component_list = ['G1','G3','CLK','S1']
        Remove_list = ['A1','G2','D1']

        self.run_spin_control = wx.SpinCtrl(self, wx.ID_ANY, value = '10', min=0, max=20,pos = (button1_x+120,button1_y))
        self.continue_spin_control = wx.SpinCtrl(self, wx.ID_ANY, value = '10', min=0, max=20,pos = (button1_x+120,button1_y+50))
        self.Add_Monitor_choices = wx.Choice(self, wx.ID_ANY,choices = component_list,pos = (button1_x+120,button1_y+100))
        self.Remove_Monitor_choices = wx.Choice(self, wx.ID_ANY,choices = Remove_list,pos = (button1_x+120,button1_y+150))


        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        self.button_run.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.button_continue.Bind(wx.EVT_BUTTON, self.OnButton_continue)
        self.button_Add_Monitor.Bind(wx.EVT_BUTTON, self.OnButton_Add_Monitor)
        self.button_Remove_Monitor.Bind(wx.EVT_BUTTON, self.OnButton_Remove_Monitor)
        self.button_Quit.Bind(wx.EVT_BUTTON, self.OnButton_Quit)

        #self.change_button.Bind(wx.EVT_BUTTON, self.OnButton_Change)

        for i in range(n):
            self.list_of_change_buttons[i].Bind(wx.EVT_BUTTON, self.getOnButton_Change(i))





        #Bind Controls/menus

        #self.run_spin_control.Bind(wx)


        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer = wx.BoxSizer(wx.VERTICAL)
        new_sizer = wx.BoxSizer(wx.HORIZONTAL)

        

        self.canvas = MyGLCanvas(self.scrollable, wx.ID_ANY, (25,250),  wx.Size(500,300))



        self.canvas.SetSizeHints(500, 500)
        main_sizer.Add(self.scrollable, 1,  wx.EXPAND+wx.TOP, 5)

        #new_sizer.Add(self.panel,1,  wx.EXPAND+wx.TOP, 5)
        

        

        self.SetSizeHints(200, 200)
        self.SetSizer(main_sizer)
        #self.SetSizer(new_sizer)

    def OnPaint(self,event=None):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 4))
        dc.DrawLine(100, 100, 100, 200)
       
    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            self.Close(True)

 
    def on_run_button(self, event):
        """Handle the event when the user clicks the run button."""

        val = self.run_spin_control.GetValue()
        text = f"Run button pressed with {val} cycles"
        self.canvas.render(text)
        self.canvas.draw_trace()
        print(text)

    def OnButton_continue(self, event):
        """Handle the event when the user clicks button_continue."""

        val = self.continue_spin_control.GetValue()

        print (f"Button continue pressed with {val} cycles")


    def OnButton_Add_Monitor(self, event):
        """Handle the event when the user clicks button_Add_Monitor."""

        index = self.Add_Monitor_choices.GetCurrentSelection() #- gets selectin index
        sel = self.Add_Monitor_choices.GetString(index)

        print ("Button Add Monitor pressed",sel)


    def OnButton_Remove_Monitor(self, event):
        """Handle the event when the user clicks button_Remove_Monitor."""

        index = self.Remove_Monitor_choices.GetCurrentSelection() #- gets selectin index
        sel = self.Remove_Monitor_choices.GetString(index)

        print ("Button Remove Monitor pressed",sel)


    def OnButton_Quit(self, event):
        """Handle the event when the user clicks button_Quit."""
        self.canvas.clear_canvas()
        print ("Button Quit pressed")

    def getOnButton_Change(self,i):

        def OnButton_Change(event):
            """Handle the event when the user clicks."""
            #self.colour_panel.SetBackgroundColour('Green')
            #self.list_of_panels[0].SetBackgroundColour('Green')
            val = int(self.list_of_switch_text_values[i].GetLabel())
            self.list_of_switch_text_values[i].SetLabel(f'{(val +1)%2}')
            print (f"Button Change S{i+1} pressed")

        return OnButton_Change

app = wx.App()
gui = Gui("Demo")
gui.Show(True)
app.MainLoop()