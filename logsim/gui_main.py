from cv2 import _InputArray_STD_ARRAY
import wx
import wx.glcanvas as wxcanvas
from OpenGL import GL, GLUT
import numpy as np
import wx.lib.scrolledpanel as scrolled
from devices import Devices
from monitors import Monitors
from network import Network
from names import Names
from scanner import Scanner
from parse import Parser


class MyGLCanvas(wxcanvas.GLCanvas):
    """Handle all drawing operations.

    This class contains functions for drawing onto the canvas. It
    also contains handlers for events relating to the canvas.

    Parameters
    ----------
    parent: parent window.
    devices: instance of the devices.Devices() class.
    monitors: instance of the monitors.Monitors() class.

    Public methods
    --------------
    init_gl(self): Configures the OpenGL context.

    render(self, text): Handles all drawing operations.

    on_paint(self, event): Handles the paint event.

    on_size(self, event): Handles the canvas resize event.

    on_mouse(self, event): Handles mouse events.

    render_text(self, text, x_pos, y_pos): Handles text drawing
                                           operations.

    clear_canvas(self): Clear the canvas of all current traces of the monitored gates and rendered text.

    draw_trace(self): Draw all the traces for the monitored signals.
    """

    def __init__(self, parent, id, pos, size,devices,monitors,network):
        """Initialise canvas properties and useful variables."""
        super().__init__(
            parent,
            -1,
            pos=pos,
            size=size,
            attribList=[
                wxcanvas.WX_GL_RGBA,
                wxcanvas.WX_GL_DOUBLEBUFFER,
                wxcanvas.WX_GL_DEPTH_SIZE,
                16,
                0,
            ],
        )
        GLUT.glutInit()
        self.init = False
        self.context = wxcanvas.GLContext(self)

        # Initialise variables for panning
        self.pan_x = 0
        self.pan_y = 0
        self.data = []  # Signal Data
        self.data_2 = []
        self.added_monitor_list = []
        self.added_monitor_id_tuple_list = []  #has ids (device_id,output_id)
        self.names = devices.names
        self.monitors = monitors
        self.devices = devices
        self.network = network

        # Initialise variables for zooming
        self.zoom = 1

        # Bind events to the canvas
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)

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

    def on_mouse(self, event):
        """Handle mouse events."""
        text = ""
        # Calculate object coordinates of the mouse position
        size = self.GetClientSize()
        ox = (event.GetX() - self.pan_x) / self.zoom
        oy = (size.height - event.GetY() - self.pan_y) / self.zoom
        old_zoom = self.zoom
        if event.ButtonDown():
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            text = "".join(
                [
                    "Mouse button pressed at: ",
                    str(event.GetX()),
                    ", ",
                    str(event.GetY()),
                ]
            )
        if event.ButtonUp():
            text = "".join(
                [
                    "Mouse button released at: ",
                    str(event.GetX()),
                    ", ",
                    str(event.GetY()),
                ]
            )
        if event.Leaving():
            text = "".join(
                ["Mouse left canvas at: ", 
                str(event.GetX()), 
                ", ",
                str(event.GetY())]
            )
        if event.Dragging():
            self.pan_x += event.GetX() - self.last_mouse_x
            self.pan_y -= event.GetY() - self.last_mouse_y
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            self.init = False
            text = "".join(
                [
                    "Mouse dragged to: ",
                    str(event.GetX()),
                    ", ",
                    str(event.GetY()),
                    ". Pan is now: ",
                    str(self.pan_x),
                    ", ",
                    str(self.pan_y),
                ]
            )
        if event.GetWheelRotation() < 0:
            self.zoom *= 1.0 + (event.GetWheelRotation() / (20 * event.GetWheelDelta()))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(
                ["Negative mouse wheel rotation. Zoom is now: ", str(self.zoom)]
            )
        if event.GetWheelRotation() > 0:
            self.zoom /= 1.0 - (event.GetWheelRotation() / (20 * event.GetWheelDelta()))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(
                ["Positive mouse wheel rotation. Zoom is now: ", str(self.zoom)]
            )
        if text:
            self.render(text)
            # self.draw_trace()

        else:
            self.Refresh()  # triggers the paint event

    def render(self, text):
        """Handle all drawing operations."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)


        if self.data:

            for j, signal in enumerate(self.data):

                GL.glColor3f(0.0, 0.0, 1.0)

                GL.glBegin(GL.GL_LINE_STRIP)
                for i, val in enumerate(signal):
                    y = 250 + val * 25 - 50 * j
                    x = (i ) + 50
                    x_next = x+1

                    GL.glVertex2f(x, y)
                    GL.glVertex2f(x_next, y)
                GL.glEnd()

            for tick in range(0,len(signal)//26+1,5):
                x =26*tick +50
                y = 290
                self.render_text(str(tick), x, 290)

            for tick in range(0,len(signal)//13+1):
                GL.glBegin(GL.GL_LINE_STRIP)
                x =13*tick +50
                y = 290
                y_next = 280
                GL.glVertex2f(x, y)
                GL.glVertex2f(x, y_next)
                GL.glEnd()


            GL.glColor3f(0.0, 0.0, 0.0)
            GL.glBegin(GL.GL_LINE_STRIP)
            y = 285
            x = 50
            x_next = (len(signal)* 26) + 26
            GL.glVertex2f(x, y)
            GL.glVertex2f(x_next//21.9+1, y)
            GL.glEnd()


        # We have been drawing to the back buffer, flush the graphics pipeline
        # and swap the back buffer to the front

        if self.added_monitor_list:
            for i, signal in enumerate(self.added_monitor_list):
                self.render_text(signal, 10, 250 - 50 * i)

        GL.glFlush()
        self.SwapBuffers()

    def clear_canvas(self):
        """Clear the canvas of all current traces of the monitored gates and rendered text."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True
        GL.glClearColor(255, 255, 255, 0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
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
        text = "".join(
            [
                "Canvas redrawn on paint event, size is ",
                str(size.width),
                ", ",
                str(size.height),
            ]
        )
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
            if character == "\n":
                y_pos = y_pos - 20
                GL.glRasterPos2f(x_pos, y_pos)
            else:
                GLUT.glutBitmapCharacter(font, ord(character))


class Gui(wx.Frame):
    """Configure the main window and all the widgets.

    This class provides a graphical user interface for the Logic Simulator and
    enables the user to change the circuit properties and run simulations.

    Parameters
    ----------
    title: title of the window.

    Public methods
    --------------
    on_menu(self, event): Event handler for the file menu.

    on_spin(self, event): Event handler for when the user changes the spin
                           control value.

    on_run_button(self, event): Event handler for when the user clicks the run
                                button.

    OnButton_continue(self, event): Event handler for when the user clicks continue 
    
    OnButton_Add_Monitor(self, event): Event handler for when the user clicks button Add_Monitor.

    OnButton_Remove_Monitor(self, event):Event handler for when the user clicks button Remove_Monitor.

    OnButton_Quit(self, event):Event handler for when the user clicks button_Quit.

    getOnButton_Change(self, i): Generate an event handlet for a change button depending on the i'th element of the switch.
    """

    def __init__(self, title,names, devices, network, monitors):
        """Initialise widgets and layout."""
        super().__init__(parent=None, title=title, size=(850, 700))

        # Configure the file menu
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        self.scrollable = wx.ScrolledCanvas(self, wx.ID_ANY)
        self.scrollable.SetSizeHints(200, 200)
        self.scrollable.ShowScrollbars(wx.SHOW_SB_ALWAYS, wx.SHOW_SB_DEFAULT)
        self.scrollable.SetScrollbars(20, 20, 0, 0)
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors 
        self.cycles_completed = 0
        #Clear Monitors

        self.monitors.reset_monitors()
        self.monitored = self.monitors.get_signal_names()[0]

        for m in self.monitored:
            m_id = self.devices.get_signal_ids(m)[0]
            ports = self.devices.get_signal_ids(m)[1:]
            for port in ports:
               self.monitors.remove_monitor(m_id,port)

        #Initialise input and output id and name lists
                
        self.component_list = [] #All components for Add device
        self.connection_list = [] #Input connection names
        
        self.input_ids = [] #(device_id,input_id)
        self.output_connections = [] #Outpur connection names
        self.output_ids = [] #(device_id,output_id)
        for d in self.devices.devices_list:
            self.component_list.append(self.devices.names.get_name_string(d.device_id))

            if d.device_kind != self.devices.SWITCH:
                inputs = d.inputs
                outputs = d.outputs


                for output_id in outputs.keys():
                    self.output_ids.append((d.device_id,output_id))
                    output_name = self.devices.names.get_name_string(d.device_id)
                    if output_id is None:
                        pass
                    else:
                        output_name = f"{output_name}:{self.devices.names.get_name_string(output_id)}"
                    self.output_connections.append(output_name)

                for input_id,(connected_output_device_id, connected_output_port_id) in inputs.items():
                    self.input_ids.append((d.device_id,input_id))
                    self.connection_list.append(f'{self.devices.names.get_name_string(d.device_id)}:{self.devices.names.get_name_string(input_id)}')
    

        # Switch Panel

        self.panel = wx.ScrolledWindow(self, wx.ID_ANY, pos=(25, 50), size=(300, 175))
        #self.panel.SetBackgroundColour("White")

        switch_x = 10
        switch_y = 10
        self.switches = self.devices.find_devices(self.devices.SWITCH) #Switch ids
        n = len(self.switches) 

        self.text_switch = wx.StaticText(
            self.panel, wx.ID_ANY, "Switches", pos=(switch_x-5, switch_y)
        )
        self.text_switch_state = wx.StaticText(
            self.panel, wx.ID_ANY, "Current State", pos=(switch_x + 75, switch_y)
        )
        self.text_switch_change = wx.StaticText(
            self.panel, wx.ID_ANY, "Change State", pos=(switch_x + 170, switch_y)
        )

        self.panel.ShowScrollbars(wx.SHOW_SB_ALWAYS, wx.SHOW_SB_DEFAULT)
        self.panel.SetScrollbars(20, 10, 0, 4.5 * n)

        self.list_of_change_buttons = []
        
        list_of_switch_names = [self.devices.names.get_name_string(switch) for switch in self.switches]  # Switch name generation
        list_of_switch_values = [self.devices.get_device(switch).switch_state for switch in self.switches]
        self.list_of_switch_text_values = []

        self.output_connections.extend(list_of_switch_names)
        self.output_ids.extend((switch,None) for switch in self.switches)
        print(self.output_connections)
        print(self.output_ids)
        print(self.connection_list)
        print(self.input_ids)



        for i in range(n):
            self.list_of_change_buttons.append(
                wx.Button(
                    self.panel, wx.ID_ANY, "Change", pos=(switch_x + 170, 50 + 40 * i)
                )
            )
            self.text = wx.StaticText(
                self.panel,
                wx.ID_ANY,
                list_of_switch_names[i],
                pos=(switch_x + 20, 50 + 40 * i),
            )

            # self.list_of_panels[i].SetBackgroundColour('Red')

            self.list_of_switch_text_values.append(
                wx.StaticText(
                    self.panel,
                    wx.ID_ANY,
                    str(list_of_switch_values[i]),
                    pos=(switch_x + 105, 50 + 40 * i),
                )
            )

         # Connections Panel

        self.panel_connections = wx.Panel(self, wx.ID_ANY, pos=(425, 50), size=(400, 175))
        #self.panel_connections.SetBackgroundColour('White)

        self.text_connections = wx.StaticText(
                self.panel_connections,
                wx.ID_ANY,
                'Connections',
                pos=(125,15),
            )

        self.Gate_choices = wx.Choice(
            self.panel_connections,
            wx.ID_ANY,
            choices=self.connection_list,
            pos=(175, 50),
        )

        '''self.Input_choices1 = wx.Choice(
            self.panel_connections,
            wx.ID_ANY,
            choices=['input1','input2'],
            pos=(275, 50),
        )'''

        self.text_input_pins = wx.StaticText(
                self.panel_connections,
                wx.ID_ANY,
                'Connect Input Pins',
                pos=(0, 50),
            )

        self.text_output_pins = wx.StaticText(
                self.panel_connections,
                wx.ID_ANY,
                'To Output pin',
                pos=(0, 100),
            )

        self.Output_choices = wx.Choice(
            self.panel_connections,
            wx.ID_ANY,
            choices=self.output_connections,
            pos=(175, 100),
        )

        self.connections_button = wx.Button(
            self.panel_connections, wx.ID_ANY, "Make Connection", pos=(275,100)
        )

        # Configure the widgets

        # buttons as part o widgets
        button1_x = 25
        button1_y = 25

        self.panel2 = wx.Panel(self.scrollable, wx.ID_ANY, pos=(550, 250), size=(300, 400))
        #self.panel2.SetBackgroundColour("White")


        self.button_run = wx.Button(self.panel2, wx.ID_ANY, "Run", pos=(button1_x, button1_y))
        self.button_continue = wx.Button(
            self.panel2, wx.ID_ANY, "Continue", pos=(button1_x, button1_y + 50)
        )
        self.button_Add_Monitor = wx.Button(
            self.panel2, wx.ID_ANY, "Add Monitor", pos=(button1_x, button1_y + 100)
        )
        self.button_Remove_Monitor = wx.Button(
            self.panel2, wx.ID_ANY, "Remove Monitor", pos=(button1_x, button1_y + 150)
        )
        self.button_Quit = wx.Button(
            self.panel2, wx.ID_ANY, "Clear", pos=(button1_x, button1_y + 200)
        )

        self.button_language = wx.Button(
            self.panel2, wx.ID_ANY, "Change Language", pos=(button1_x, button1_y + 250)
        )

        # Controls/menus for buttons
        

        #self.component_list = ["G1", "G3", "CLK", "A1", "G2", "D1"]
        self.add_list = self.component_list.copy()
        self.Remove_list = []
        self.language_list = ['English','Arabic']

        self.run_spin_control = wx.SpinCtrl(
            self.panel2, wx.ID_ANY, value="10", min=0, max=20, pos=(button1_x + 130, button1_y)
        )
        self.continue_spin_control = wx.SpinCtrl(
            self.panel2,
            wx.ID_ANY,
            value="10",
            min=0,
            max=20,
            pos=(button1_x + 130, button1_y + 50),
        )
        self.Add_Monitor_choices = wx.Choice(
            self.panel2,
            wx.ID_ANY,
            choices=self.add_list,
            pos=(button1_x + 130, button1_y + 100),
        )
        self.Remove_Monitor_choices = wx.Choice(
            self.panel2,
            wx.ID_ANY,
            choices=self.Remove_list,
            pos=(button1_x + 130, button1_y + 150),
        )

        self.Language_choices = wx.Choice(
            self.panel2,
            wx.ID_ANY,
            choices=self.language_list,
            pos=(button1_x + 130, button1_y + 250),
        )

        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        self.button_run.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.button_continue.Bind(wx.EVT_BUTTON, self.OnButton_continue)
        self.button_Add_Monitor.Bind(wx.EVT_BUTTON, self.OnButton_Add_Monitor)
        self.button_Remove_Monitor.Bind(wx.EVT_BUTTON, self.OnButton_Remove_Monitor)
        self.button_Quit.Bind(wx.EVT_BUTTON, self.OnButton_Quit)
        self.button_language.Bind(wx.EVT_BUTTON, self.OnButton_Language)
        self.connections_button.Bind(wx.EVT_BUTTON, self.OnButton_Make_Connection)


        for i in range(n):
            self.list_of_change_buttons[i].Bind(
                wx.EVT_BUTTON, self.getOnButton_Change(i)
            )

        # Bind Controls/menus

        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer = wx.BoxSizer(wx.VERTICAL)
        new_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.canvas = MyGLCanvas(
            self.scrollable, wx.ID_ANY, (25, 250), wx.Size(500, 300,),devices,monitors,network
        )
        self.canvas.SetSizeHints(500, 500)
        main_sizer.Add(self.scrollable, 1, wx.EXPAND + wx.TOP, 5)
        self.SetSizeHints(200, 200)
        self.SetSizer(main_sizer)

    def OnPaint(self, event=None):
        """Draw vertical line for the Switch Panel."""
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
        self.monitors.reset_monitors()
        self.cycles_completed = 0
        self.canvas.data = []
        val = self.run_spin_control.GetValue()
        text = f"Run button pressed with {val} cycles"
        # self.canvas.render(text)
        self.cycles_completed = val

        for _ in range(val*26):
            if self.network.execute_network():
                self.monitors.record_signals()
            else:
                print("Error! Network oscillating.")

        for device_id, output_id in self.monitors.monitors_dictionary:
            signal_list = self.monitors.monitors_dictionary[(device_id, output_id)]
            self.canvas.data.append(signal_list)
        self.canvas.render(text)
        print(text)

    def OnButton_continue(self, event):
        """Handle the event when the user clicks button_continue."""
        cycles = self.continue_spin_control.GetValue()
        text = f"Continue button pressed with {cycles} cycles"

        # self.canvas.data = [(i//5) % 2  for i in range(self.number_of_cycles)]
        '''self.canvas.data = [
            [(i // (j + 1)) % 2 for i in range(self.number_of_cycles*2)]
            for j in range(len(self.canvas.added_monitor_list))
        ]'''

        if cycles is not None:  # if the number of cycles provided is valid
            if self.cycles_completed == 0:
                print("Error! Nothing to continue. Run first.")
                
            for _ in range(cycles*26):
                if self.network.execute_network():
                    self.monitors.record_signals()
                
                else:
                    print("Error! Network oscillating.")
            self.cycles_completed += cycles


            print(self.monitors.monitors_dictionary.keys())
            print(len(self.canvas.data))

            signal_lengths = []

            '''for device_id, output_id in self.monitors.monitors_dictionary:
                signal_list = self.monitors.monitors_dictionary[(device_id, output_id)]
                signal_lengths.append(len(signal_list))
                #self.data.append(signal_list)

            if len(self.canvas.data) != len(self.monitors.get_signal_names()[0]):

                for device_id, output_id in self.monitors.monitors_dictionary:
                    signal_list = self.monitors.monitors_dictionary[(device_id, output_id)]
                    
                    if len(signal_list) < max(signal_lengths):
                        signal_list = [0 if signal==4  else signal for signal in signal_list]
                        zeros = [0 for i in range(max(signal_lengths) -len(signal_list))]
                        zeros.extend(signal_list) 
                        signal_list = zeros
                        self.canvas.data.append(signal_list)'''
                    


        self.canvas.render(text)

        print(f"Button continue pressed with {cycles} cycles")

    def OnButton_Add_Monitor(self, event):
        """Handle the event when the user clicks button Add_Monitor."""
        index = self.Add_Monitor_choices.GetCurrentSelection()
        signal = self.Add_Monitor_choices.GetString(index)
        text = f"Button Add Monitor {signal} pressed"
        
        
        [device, port] = self.devices.get_signal_ids(signal)
        monitor_error = self.monitors.make_monitor(device, port,self.cycles_completed)
        if monitor_error == self.monitors.NO_ERROR:
            print("Successfully made monitor.")
        else:
            print("Error! Could not make monitor.")

        self.add_list.remove(signal)
        self.Remove_list.append(signal)
        self.Add_Monitor_choices.SetItems(self.add_list)
        self.Remove_Monitor_choices.SetItems(self.Remove_list)

        self.canvas.added_monitor_list.append(signal)
        self.canvas.added_monitor_id_tuple_list.append((device, port))
        self.canvas.render(text)

    def OnButton_Remove_Monitor(self, event):
        """Handle the event when the user clicks button Remove_Monitor."""
        index = (
            self.Remove_Monitor_choices.GetCurrentSelection()
        )  # - gets selectin index
        signal = self.Remove_Monitor_choices.GetString(index)
        text = f"Button Remove Monitor {signal} pressed"

        i = self.canvas.added_monitor_list.index(signal)

        [device, port] = self.devices.get_signal_ids(signal)
        if self.monitors.remove_monitor(device, port):
            print("Successfully zapped monitor")
        else:
            print("Error! Could not zap monitor.")

        self.add_list.append(signal)
        self.Remove_list.remove(signal)
        self.Add_Monitor_choices.SetItems(self.add_list)
        self.Remove_Monitor_choices.SetItems(self.Remove_list)
        try:
            del self.canvas.data[i]
        except:
            print('couldnt delete')
        self.canvas.added_monitor_list.remove(signal)
        self.canvas.added_monitor_id_tuple_list.remove(self.canvas.added_monitor_id_tuple_list[i])
        self.canvas.render(text)

        print(text)

    def OnButton_Quit(self, event):
        """Handle the event when the user clicks button_Quit."""
        self.canvas.clear_canvas()
        self.canvas.data = []
        self.canvas.added_monitor_list = []
        self.add_list = self.component_list.copy()
        self.Remove_list = []
        self.Add_Monitor_choices.SetItems(self.add_list)
        self.Remove_Monitor_choices.SetItems(self.Remove_list)

        self.monitors.reset_monitors()
        self.monitored = self.monitors.get_signal_names()[0]

        for m in self.monitored:
            m_id = self.devices.get_signal_ids(m)[0]
            ports = self.devices.get_signal_ids(m)[1:]
            for port in ports:
               self.monitors.remove_monitor(m_id,port)

        print("Button Quit pressed")

    def OnButton_Language(self, event):
        """Handle the event when the user clicks button_Language."""
        index = self.Language_choices.GetCurrentSelection()
        language = self.Language_choices.GetString(index)

        if language == 'Arabic':
            self.button_run.SetLabel('ركض')
            self.button_continue.SetLabel('استمر')
            self.button_Add_Monitor.SetLabel('أضف شاشة')
            self.button_Remove_Monitor.SetLabel('قم بإزالة الشاشة')
            self.button_Quit.SetLabel('صافي')
            self.text_switch.SetLabel('مفتاح كهربائي')
            self.text_switch_state.SetLabel('الوضع الحالي')
            self.text_switch_change.SetLabel('تغيير الوضع')
            self.text_connections.SetLabel('روابط')
            self.text_input_pins.SetLabel('قم بتوصيل دبوس الإدخال')
            self.text_output_pins.SetLabel('لإخراج دبوس')
            self.connections_button.SetLabel('صنع روابط')
            
            for i in self.list_of_change_buttons:
                i.SetLabel('للتغيير')

        elif language == 'English':
            self.button_run.SetLabel('Run')
            self.button_continue.SetLabel('Continue')
            self.button_Add_Monitor.SetLabel('Add Monitor')
            self.button_Remove_Monitor.SetLabel('Remove Monitor')
            self.button_Quit.SetLabel('Clear')
            self.text_switch.SetLabel('Switches')
            self.text_switch_state.SetLabel('Current State')
            self.text_switch_change.SetLabel('Change State')
            self.text_connections.SetLabel('Connections')
            self.text_input_pins.SetLabel('Connect Input Pins')
            self.text_output_pins.SetLabel('To Output Pin')
            self.connections_button.SetLabel('Make Connection')

            for i in self.list_of_change_buttons:
                i.SetLabel('Change')

        print("Button Language pressed")

    def getOnButton_Change(self, i):
        """Generate a handle for a change button depending on the i'th element of the switch."""
        def OnButton_Change(event):
            """Handle the event when the user clicks change_button."""
            # self.colour_panel.SetBackgroundColour('Green')
            # self.list_of_panels[0].SetBackgroundColour('Green')
            val = int(self.list_of_switch_text_values[i].GetLabel())
            self.devices.set_switch(self.switches[i],(val +1)%2)
            self.list_of_switch_text_values[i].SetLabel(f"{(val +1)%2}")
            print(f"Button Change S{i+1} pressed")

        return OnButton_Change

    def OnButton_Make_Connection(self, event):
        """Handle the event when the user presses connections_button."""
        input_index =  self.Gate_choices.GetCurrentSelection()
        output_index = self.Output_choices.GetCurrentSelection()
        input_device_id,input_id = self.input_ids[input_index]
        output_device_id,output_id = self.output_ids[output_index]
        G = self.devices.get_device(input_device_id)
        print(G.inputs)
        G.inputs[input_id] = None
    
        self.network.make_connection(input_device_id, input_id, output_device_id,output_id)

        inputs = G.inputs

        print(inputs)


        print("Button Make Connection pressed")
