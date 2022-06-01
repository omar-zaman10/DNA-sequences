import wx

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

        # Configure the widgets
        self.text = wx.StaticText(self, wx.ID_ANY, "Some text",pos = (600,200))


        #buttons as part o widgets
        self.button_run = wx.Button(self, wx.ID_ANY, "Run",pos = (600,350))
        self.button_continue = wx.Button(self, wx.ID_ANY, "Continue",pos = (600,400))
        self.button_Add_Monitor = wx.Button(self, wx.ID_ANY, "Add Monitor",pos = (600,450))
        self.button_Remove_Monitor = wx.Button(self, wx.ID_ANY, "Remove Monitor",pos = (600,500))
        self.button_Quit = wx.Button(self, wx.ID_ANY, "Quit",pos = (600,550))



        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.button_run.Bind(wx.EVT_BUTTON, self.OnButton_run)
        self.button_continue.Bind(wx.EVT_BUTTON, self.OnButton_continue)
        self.button_Add_Monitor.Bind(wx.EVT_BUTTON, self.OnButton_Add_Monitor)
        self.button_Remove_Monitor.Bind(wx.EVT_BUTTON, self.OnButton_Remove_Monitor)
        self.button_Quit.Bind(wx.EVT_BUTTON, self.OnButton_Quit)




        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(side_sizer, 1, wx.ALL, 5)


        self.SetSizeHints(300, 300)
        self.SetSizer(main_sizer)

    def OnMenu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            self.Close(True)


    #Button logic
 
    def OnButton_run(self, event):
        """Handle the event when the user clicks button_run."""
        print ("Button Run pressed")


    def OnButton_continue(self, event):
        """Handle the event when the user clicks button_continue."""
        print ("Button continue pressed")
    def OnButton_Add_Monitor(self, event):
        """Handle the event when the user clicks button_Add_Monitor."""
        print ("Button Add Monitor pressed")
    def OnButton_Remove_Monitor(self, event):
        """Handle the event when the user clicks button_Remove_Monitor."""
        print ("Button Remove Monitor pressed")
    def OnButton_Quit(self, event):
        """Handle the event when the user clicks button_Quit."""
        print ("Button Quit pressed")

app = wx.App()
gui = Gui("Demo")
gui.Show(True)
app.MainLoop()