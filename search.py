from bs4 import BeautifulSoup
import httplib, re
from collections import defaultdict
import webbrowser
from PyQt4 import QtGui
from PyQt4.QtCore import QString, QTimer
import main_window
import settings_diag
import os, glob, pickle

class MainApp(QtGui.QMainWindow, main_window.Ui_MainWindow):
    """ MainApp Class thats generated from the untitled.ui and converted to python """
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.actionQuit.triggered.connect(QtGui.qApp.quit)
        self.settings = Settings()
        self.settings.load_settings()
        self.pushSearch.clicked.connect(self.do_a_search)
        self.actionSettings.triggered.connect(self.show_settings_diag)
        self.results = defaultdict(list)
        self.listWidgetResults.itemClicked.connect(self.item_clicked)
        one_off_timer = QTimer()
        one_off_timer.singleShot(1, self.do_a_search)

    def main(self):
        self.show()
    
    def show_settings_diag(self):
        """ Clicked on the settings menu item """
        settings_dialogue = SettingsDialogue(self.settings, parent=self)
        return_value = settings_dialogue.exec_()
        if return_value == 1:
            self.settings.load_settings()

    def do_a_search(self):
        self.results = defaultdict(list)
        self.listWidgetResults.clear()
        for e in self.settings.search_terms:
            #print "searching for:  "+ e
            process_first_page(self.results, e)
        for e in self.settings.search_terms:
            for w in self.results[e]:
                item = KijijiListItem(w)
                self.listWidgetResults.addItem(item)

    def item_clicked(self):
        """ kijijijiijii list item clicked"""
        for item in self.listWidgetResults.selectedItems():
            webbrowser.open(item.link)

class KijijiListItem(QtGui.QListWidgetItem):
    """ Container class for a kijiji item """
    def __init__(self, item, *args, **kwargs):
        super(KijijiListItem, self).__init__(*args, **kwargs)
        self.link = get_link(item)
        body = get_body(item)
        self.setText(body)
        self.setToolTip(self.link)

class SettingsDialogue(QtGui.QDialog, settings_diag.Ui_Dialog):
    """ this should pop up a settings window """
    def __init__(self, settings, parent=None):
        super(SettingsDialogue, self).__init__(parent)
        self.setupUi(self)
        self.settings = settings
        self.settings.load_settings()
        self.lineEditCity.setText(str(self.settings.city))
        self.pushAddButton.clicked.connect(self._add_clicked)
        for u in self.settings.search_terms:
            self.listWidgetSearchTerms.addItem(QtGui.QListWidgetItem(u))
        self.listWidgetSearchTerms.itemClicked.connect(self._item_clicked)
        self.lineEditSearchTerms.setFocus()

    def _item_clicked(self):
        """ clicked on an item in the list widget """
        item = self.listWidgetSearchTerms.takeItem(self.listWidgetSearchTerms.currentRow())
        item = None

    def _add_clicked(self):
        """ clicked on the add button """
        text = self.lineEditSearchTerms.text()
        self.listWidgetSearchTerms.addItem(QtGui.QListWidgetItem(text))
        text = str(text)
        self.settings.search_terms.append(text)
        self.lineEditSearchTerms.clear()

    def accept(self, *args, **kwargs):
        """ Runs when the OK button is pressed and exits the dialogue """
        text = str(self.lineEditCity.text())
        self.settings.city = text.lower()
        self.settings.search_terms = []
        items = self.return_items()
        for i in items:
            item_text = str(i.text()).strip().lower()
            if item_text == '':
                pass
            else:
                self.settings.search_terms.append(str(i.text()))
        self.settings.save_settings()
        return QtGui.QDialog.accept(self, *args, **kwargs)

    def return_items(self):
        """ Fetch all the items in the list widget """
        for i in xrange(self.listWidgetSearchTerms.count()):
            yield self.listWidgetSearchTerms.item(i)

""" Settings class """


class Settings():
    """ Going to use the settings class to pickle everything and write it to disk """
    def __init__(self):
        self.city = "halifax"
        self.search_terms = []

    def save_settings(self):
        save_file = file("settings.dat", "wb")
        pickle.dump(self, save_file, 2)
        save_file.close()

    def load_settings(self):
        if check_for_save_file():
            load_file = file('settings.dat', "rb")
            settings = pickle.load(load_file)
            self.city = settings.city
            self.search_terms = settings.search_terms
            load_file.close()
            return True
        return False

def check_for_save_file():
    """ check for the existence of a save """
    path = "./"
    for cur_file in glob.glob(os.path.join(path, "*.dat")):
        return True
    return False


def get_link(string):
    start_link = string.find('href=')
    if start_link == -1:
        return None
    start_quote = string.find('"', start_link)
    end_quote = string.find('"', start_quote + 1)
    url = string[start_quote + 1 : end_quote]
    return url

def get_body(string):
    pattern = '</a>\n'
    start_link = string.find(pattern)
    body = string[start_link + len(pattern) : -1]
    return body

def remove_control_chars(s):
    return (''.join([x for x in s if ord(x) < 128]))

def is_want(product):
    return (re.search(r'Wanted', product))    

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def get_result(soup, num):
    match = "resultRow"+str(num)
    if (soup.find(id=match)):       
        mylist = soup.find(id=match).findAll("td")
        mylink =  soup.find(id=match).a
        desc = mylist[2]
        desc = remove_html_tags(str(desc))    
        return (str(mylink) + desc)
    else:
        return

def process_first_page(results, search):
    pagenum = 1;
    if pagenum == 1:
        pagestr = "isSearchFormZtrue"
    else:
        pagestr = "PageZ"+pagenum

    city = "halifax.kijiji.ca"
    httpconn = httplib.HTTPConnection(city)
    if (type(search) is list or type(search) is tuple):
        searchstr1 = "-".join(search)
        searchstr2 = "Q20".join(search)
    else:
        searchstr1 = search
        searchstr2 = search

    querystr = "/f-"+searchstr1+"-Classifieds-W0QQKeywordZ"+searchstr2+"QQ"+pagestr
    httpconn.request("GET", querystr)

    r1 = httpconn.getresponse()
    #print r1.status, r1.reason
    data1 = r1.read()
    soup = BeautifulSoup(data1)
    
    items = 20
    for i in reversed(range(items)):        
        product = get_result(soup, i)        
        if (product and not is_want(product)):
            results[search].append( product)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    MA = MainApp()
    MA.main()
    app.setStyle(QString("plastique"))
    app.exec_()