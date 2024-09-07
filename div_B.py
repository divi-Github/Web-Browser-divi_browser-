from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *



import sys #sys,os: Standard Python libraries for interacting with the system (file paths, os etc).
import os

from PyQt5.QtGui import QIcon 

from PyQt5.QtWidgets import QFileDialog 


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):

      
        super(MainWindow, self).__init__(*args,**kwargs) 
        

        self.browser = QWebEngineView() 
        # Creates the web view (the part that displays web pages).

        self.browser.setUrl(QUrl('https://google.com')) 
        # Sets the initial page to Google.

        self.urlbar = QLineEdit() 
        # Creates an input field for the address bar. PyQt uses signals and slots for communication.

        self.browser.urlChanged.connect(self.update_urlbar) 
        # Emitted when the URL in the browser changes.

        self.browser.loadFinished.connect(self.update_title) 
        # Emitted when a page finishes loading.

        self.status = QStatusBar() 
        # Creates a status bar at the bottom of the window.

        self.setCentralWidget(self.browser) 
        # Makes the web view the main area of the window.

        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation") # Creates a navigation toolbar.

        self.addToolBar(navtb) # Adds the toolbar to the window.



        back_icon = QIcon("back.png")
        next_icon = QIcon("forward.png")
        reload_icon = QIcon("reload.png")
        home_icon = QIcon("home.png")
        download_icon = QIcon("dwnld.png")
        history_icon = QIcon("history.png")

        navtb.addSeparator() # Adds a separator to the navigation toolbar

# BACK Button 

        back_btn = QAction(back_icon,"Back", self) 
        # QAction object represents a user-triggerable command or action ,associated with widgets like menus, buttons etc

        back_btn.triggered.connect(self.browser.back) # Connects the button's click signal to the browser's "back" function.
        navtb.addAction(back_btn) # adds the button to the navigation toolbar.

        navtb.addSeparator() 

# FORWARD Button

        next_btn = QAction(next_icon,"Forward", self)
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        navtb.addSeparator()

# RELOAD Button

        reload_btn = QAction(reload_icon,"Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        navtb.addSeparator()

# HOME Button

        home_btn = QAction(home_icon,"Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

# DOWNLOAD Button

        download_btn = QAction(download_icon,"Download", self)
        download_btn.triggered.connect(self.download_file) 
        navtb.addAction(download_btn)

        navtb.addSeparator()

# HISTORY Button

        history_btn = QAction(history_icon,"History", self)
        history_btn.triggered.connect(self.show_history)
        navtb.addAction(history_btn)


        navtb.addSeparator()

# STOP Button

        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
        stop_btn = QAction("Stop", self)
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Settings")
        set_homepage_action = QAction("Set Homepage", self)
        set_homepage_action.triggered.connect(self.set_homepage)
        settings_menu.addAction(set_homepage_action)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Text (Any text you want to highlight)")
        self.search_bar.returnPressed.connect(self.search)
        navtb.addWidget(self.search_bar)

        self.show()

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "" : #blank
            q.setScheme("http")

        self.browser.setUrl(q)



    # Navigates the browser to a predefined homepage
    def navigate_home(self):
        self.browser.seturl(QUrl("https://goggle.com"))

    # Updates the text in the URL bar to match the provided URL (q) and moves the cursor to the beginning.
    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    # Fetches the title of the currently loaded webpage and updates the window's title bar with it.
    def update_title(self):
        title = self.browser.page().title
        self.setWindowTitle(f"")

    # Initiates a download by presenting a "Save As" dialog for the user to choose a file location 
    # and then connects a signal to start the actual download process.
    def download_file(self):
        options = QFileDialog.Options() 
        filename, _ = QFileDialog.getSaveFileName(self, "Download File", "", "All Files (*.*)", options=options)
        if filename: 
            self.browser.page().profile().downloadRequested.connect(self.handle_download)

    # Handles the download process, accepting the suggested file path and triggering the download if it's ready.
    def handle_download(self, download):
        if download.isFinished():
            return   
        suggested_path = download.suggestedFileName()
        download.setPath(suggested_path)    
        download.accept()

    # Retrieves the browser's history, builds a formatted list of visited pages, and displays it in a message box.
    def show_history(self):
        history = self.browser.history()
        history_list = ""
        for i in range(history.count()):
            item = history.itemAt(i)
            history_list += f"{i + 1}. {item.title()}: {item.url().toString()}\n" 

        QMessageBox.information(self, "History", history_list) 

    # Displays a dialog box where the user can enter a new homepage URL and returns both the entered URL 
    # and a boolean indicating if the user clicked 'OK'.
    def set_homepage(self):
        new_homepage, ok = QInputDialog.getText(self, "Homepage", "Enter new homepage URL:")
        if ok:
            # TODO: You might want to validate if its a valid URL here
            self.homepage = new_homepage


    # Update navigate_home to use the custom homepage
    #  Instructs the browser to navigate to the URL stored in the self.homepage attribute.
    def navigate_home(self):
        self.browser.setUrl(QUrl(self.homepage)) 

    def search(self): 
        search_text = self.search_bar.text() # Retrieves the text entered by the user in the search bar widget.
        self.browser.findText(search_text)  
        #Initiates a search within the currently loaded web page for the specified search_text.

"""Creates the PyQt application object.Set application name and icon."""
app = QApplication(sys.argv) 
# creates a new application object using PyQt and prepares it to handle command-line arguments, if any are provided.


app.setApplicationName("divi_Browser") #Application Name
app.setWindowIcon(QIcon("d.png")) # Application icon

window = MainWindow() #Creates the main browser window.
app.exec_()  #Starts the PyQt event loop (which handles user interactions).  
