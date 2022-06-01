# Adapted from an example by Dr Gee (CUED)
import wx

class Gui(wx.Frame):
    def __init__(self, title):
        """Initialise widgets and layout."""
        super().__init__(parent=None, title=title, size=(400, 100))
      
        # Configure the file menu
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Configure the widgets
        self.text = wx.StaticText(self, wx.ID_ANY, "Some text")
        button_sizer.Add(self.text, 1, wx.TOP+wx.LEFT+wx.RIGHT, 5)
        self.button1 = wx.Button(self, wx.ID_ANY, label="Button 1", name="SomeNameOrOther")

        button_sizer.Add(self.button1, 1, wx.RIGHT, 5)
        self.button2 = wx.Button(self, wx.ID_ANY, "Button2")

        button_sizer.Add(self.button2 , 1, wx.RIGHT, 5)
        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2)
        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(side_sizer, 1, wx.ALL, 5)

        side_sizer.Add(self.text, 1, wx.TOP, 10)
        side_sizer.Add(self.button1, 1, wx.ALL, 5)
        side_sizer.Add(self.button2, 1, wx.ALL, 5)

        self.SetSizeHints(300, 100)
        self.SetSizer(button_sizer)
        controlwin = wx.ScrolledWindow(self, -1, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER|wx.HSCROLL|wx.VSCROLL)
        button_sizer.Add(controlwin,1, wx.EXPAND | wx.ALL, 10)
        button_sizer2 = wx.BoxSizer(wx.VERTICAL)
        controlwin.SetSizer(button_sizer2)
        controlwin.SetScrollRate(10, 10)
        controlwin.SetAutoLayout(True)

        button_sizer2.Add(wx.Button(controlwin, wx.ID_ANY, "Run"), 0, wx.ALL, 10)

    def OnMenu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            print("Quitting")
            self.Close(True)
 
    def OnButton1(self, event):
        """Handle the event when the user clicks button1."""
        print ("Button 1 pressed")
        
    def OnButton2(self, event):
        """Now find button 1 and change its label."""
        print ("Button 2 pressed")
        tmp=wx.FindWindowByName("SomeNameOrOther")
        if tmp!=None:
            tmp.SetLabel("Button 1 updated")
        
            
app = wx.App()
gui = Gui("Demo")
gui.Show(True)
app.MainLoop()