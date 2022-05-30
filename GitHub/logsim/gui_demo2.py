# Adapted from an example by Dr Gee (CUED)
import wx
from wx import ArtProvider

class Gui(wx.Frame):
    QuitID=999
    OpenID=998
    def __init__(self, title):
        """Initialise widgets and layout."""
        super().__init__(parent=None, title=title, size=(400, 400))
        QuitID=999
        OpenID=998
        locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        # Configure the file menu
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        toolbar=self.CreateToolBar()
        myimage=wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR)
        toolbar.AddTool(wx.ID_ANY,"New file", myimage)
        myimage=wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR)
        toolbar.AddTool(OpenID,"Open file", myimage)
        myimage=wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR)
        toolbar.AddTool(wx.ID_ANY,"Save file", myimage)
        myimage=wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR)
        toolbar.AddTool(QuitID,"Quit", myimage)
        toolbar.Bind(wx.EVT_TOOL, self.Toolbarhandler)
        toolbar.Realize()
        self.ToolBar = toolbar
        # Configure the widgets
        self.text = wx.StaticText(self, wx.ID_ANY, "Some text")
        self.button1 = wx.Button(self, wx.ID_ANY, "Button1")
        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1)
        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(side_sizer, 1, wx.ALL, 5)

        side_sizer.Add(self.text, 1, wx.TOP, 10)
        side_sizer.Add(self.button1, 1, wx.ALL, 5)

        self.SetSizeHints(300, 300)
        self.SetSizer(main_sizer)

    def OnMenu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            print("Quitting")
            self.Close(True)
 
    def OnButton1(self, event):
        """Handle the event when the user clicks button1."""
        print ("Button 1 pressed")
        
    def Toolbarhandler(self, event): 
        if event.GetId()==self.QuitID:
            print("Quitting")
            self.Close(True)
        if event.GetId()==self.OpenID:
            openFileDialog= wx.FileDialog(self, "Open txt file", "", "", wildcard="TXT files (*.txt)|*.txt", style=wx.FD_OPEN+wx.FD_FILE_MUST_EXIST)
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
               print("The user cancelled") 
               return     # the user changed idea...
            print("File chosen=",openFileDialog.GetPath())
            
app = wx.App()
gui = Gui("Demo")
gui.Show(True)
app.MainLoop()
