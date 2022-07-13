from urllib.request import urlopen
from          PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from   urllib.error import HTTPError, URLError
from            bs4 import BeautifulSoup

import requests
import os
import time
import psutil
import pandas as pd

import WebScraperTable
import WebScraperImage
import WebScraperEmails
#import resources
#import resources2
import sys

class Ui_MainWindow(object):

    color_iterator = 0
    color = [[111, 211, 44, 255],[251, 123, 38, 255],[123, 15, 69, 255],[255, 255, 0, 200]]

    table_wst = []
    table_wst.append([])
    table_wst[0].append("Time of execution [s]")
    table_wst[0].append("CPU use [%]")
    table_wst[0].append("Memory Use [GB]")
    table_wst[0].append("Numbers of el. scrap.")
    wst = 1

    table_wsi = []
    table_wsi.append([])
    table_wsi[0].append("Time of execution [s]")
    table_wsi[0].append("CPU use [%]")
    table_wsi[0].append("Memory Use [GB]")
    table_wsi[0].append("Numbers of el. scrap.")
    wsi = 1

    table_wse = []
    table_wse.append([])
    table_wse[0].append("Time of execution [s]")
    table_wse[0].append("CPU use [%]")
    table_wse[0].append("Memory Use [GB]")
    table_wse[0].append("Numbers of el. scrap.")
    wse = 1


    def back(self):
        self.webView.back()

    def forward(self):
        self.webView.forward()

    def reload(self):
        self.webView.reload()

    def goAdress(self):
        print('address')

    def home(self):
        self.webView.load(QtCore.QUrl("http://www.google.com"))

    def search(self):
        url = self.ln_addressbar.text()
        self.webView.load(QtCore.QUrl(url))

    def WebScraper(self):
        self.webView.setGeometry(QtCore.QRect(0, 50, (self.width-380), (self.height-300)))

    def dimensionPage(self):
        self.webView.setGeometry(QtCore.QRect(0, 50, self.width, self.height))

    def dimensionPage2(self):
        self.webView.setGeometry(QtCore.QRect(0, 50, (self.width-370), (self.height-125)))

    def open_script(self):
        #os.system("xterm -hold -e lala.sh")
        os.system("xterm -e bash -c './ ; exec lala.sh'")

    def change_url(self):
        self.ln_addressbar.setText(self.ln_table_url.text())
        self.webView.load(QtCore.QUrl(self.ln_table_url.text()))

    def pb_tab_save(self):
        start = time.time()
        url = self.ln_table_url.text()
        key_word = self.ln_table_key_word.text()

        if self.cb_table_get_pages.isChecked():
            nr_tables = 0
        else:
            nr_tables = int(self.ln_table_pages.text())

        if self.cb_table_get_rows.isChecked():
            nr_rows = 0
        else:
            nr_rows = int(self.ln_table_nr_rows.text())

        if self.cb_table_get_columns.isChecked():
            cols_list = 0
        else:
            cols_list = list(self.ln_table_col.text().split(","))
            cols_list = map(int, cols_list)

        file = self.ln_table_file.text()
        path = self.ln_table_path.text()
        nonASCII = self.cb_table_non_ascii.isChecked()

        if self.rb_table_csv.isChecked():
            format = 'CSV'
        elif self.rb_table_json.isChecked():
            format = 'JSON'
        else:
            format = "MySQL"

        if url and path:
            WebScraperTable.scrape(url, key_word, nonASCII, nr_tables, nr_rows, cols_list, file, path, format)
            self.image1 = QtGui.QPixmap("images/Saved2.png")
            self.image1 = self.image1.scaledToWidth(341)
        else:
            self.image1 = QtGui.QPixmap("images/Error_saving.png")
            self.image1 = self.image1.scaledToWidth(341)

        self.image_table.setAlignment(QtCore.Qt.AlignCenter)
        self.image_table.setPixmap(self.image1)
        end = time.time()
        time_tb = end - start
        self.table_wst.append([])
        self.table_wst[self.wst].append(time_tb)
        self.table_wst[self.wst].append(psutil.cpu_percent())
        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUse = py.memory_info()[0] / 2. ** 30
        self.table_wst[self.wst].append(memoryUse)
        self.table_wst[self.wst].append(nr_tables)
        self.wst += 1
        s1 = pd.DataFrame(ui.table_wst)
        s1.to_csv("WebScraperTable.csv", index=False)

    def pb_imag_save(self):
        start = time.time()
        search    = self.ln_image_search.text()
        dest_imag = self.ln_image_dest.text()
        nr_imag   = self.ln_image_nr.text()
        if self.rb_image_none.isChecked():
            tbs = ''
        elif self.rb_image_trans.isChecked():
            tbs = 'ic:trans'
        elif self.rb_image_white.isChecked():
            tbs = 'isc:white'
        elif self.rb_image_black.isChecked():
            tbs = 'isc:black'
        elif self.rb_image_gray.isChecked():
            tbs = 'isc:gray'
        elif self.rb_image_red.isChecked():
            tbs = 'isc:red'
        elif self.rb_image_orange.isChecked():
            tbs = 'isc:orange'
        elif self.rb_image_yellow.isChecked():
            tbs = 'isc:yellow'
        elif self.rb_image_green.isChecked():
            tbs = 'isc:green'
        elif self.rb_image_alice.isChecked():
            tbs = 'isc:blue'
        elif self.rb_image_purple.isChecked():
            tbs = 'isc:purple'
        elif self.rb_image_pink.isChecked():
            tbs = 'isc:pink'

        if search and dest_imag and nr_imag:
            WebScraperImage.scrape_imag.search_and_download(search_term=search,
                                                            tbs=tbs,
                                                            driver_path=WebScraperImage.scrape_imag.CHROMEDRIVER_PATH,
                                                            target_path=dest_imag,
                                                            number_images=int(nr_imag))
            self.image1 = QtGui.QPixmap("images/Saved2.png")
            self.image1 = self.image1.scaledToWidth(341)
        else:
            self.image1 = QtGui.QPixmap("images/Error_saving.png")
            self.image1 = self.image1.scaledToWidth(341)

        self.image_imag.setAlignment(QtCore.Qt.AlignCenter)
        self.image_imag.setPixmap(self.image1)
        end = time.time()
        time_tb = end - start
        self.table_wsi.append([])
        self.table_wsi[self.wsi].append(time_tb)
        self.table_wsi[self.wsi].append(psutil.cpu_percent())
        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUse = py.memory_info()[0] / 2. ** 30
        self.table_wsi[self.wsi].append(memoryUse)
        self.table_wsi[self.wsi].append(nr_imag)
        self.wsi = self.wsi + 1
        print(self.wsi)
        s2 = pd.DataFrame(self.table_wsi)
        s2.to_csv("WebScraperImage.csv", index=False)

    def email_save(self):
        start = time.time()
        file_name = self.ln_email_file.text()
        path = self.ln_email_path.text()
        url = self.ln_email_url.text()

        if self.cb_email_pages.isChecked():
            pages_nr = 0
        else:
            pages_nr = int(self.ln_email_page_nr.text())

        if self.rb_email_csv.isChecked():
            format = "CSV"
        elif self.rb_email_json.isChecked():
            format = "JSON"
        else:
            format = "MySQL"

        if url and path:
            WebScraperEmails.scrape_email.scrape(WebScraperEmails.scrape_email,
                                                 url=url,
                                                 nr_pages=pages_nr,
                                                 file_name=file_name,
                                                 path_file=path,
                                                 format=format)

            self.image1 = QtGui.QPixmap("images/Saved2.png")
            self.image1 = self.image1.scaledToWidth(341)
        else:
            self.image1 = QtGui.QPixmap("images/Error_saving.png")
            self.image1 = self.image1.scaledToWidth(341)

        self.image_emails.setAlignment(QtCore.Qt.AlignCenter)
        self.image_emails.setPixmap(self.image1)
        end = time.time()
        time_tb = end - start
        self.table_wse.append([])
        self.table_wse[self.wse].append(time_tb)
        self.table_wse[self.wse].append(psutil.cpu_percent())
        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUse = py.memory_info()[0] / 2. ** 30
        self.table_wse[self.wse].append(memoryUse)
        self.table_wse[self.wse].append(pages_nr)
        self.wse += 1
        s3 = pd.DataFrame(ui.table_wse)
        s3.to_csv("WebScraperImage.csv", index=False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.l_table_url.setText(_translate("MainWindow", "URL:"))
        #self.ln_table_url.setPlaceholderText(_translate("MainWindow", "self.webView.sender().url().url().toString"))
        self.l_table_key_word.setText(_translate("MainWindow", "Key Word"))
        self.l_table_nr_columns.setText(_translate("MainWindow", "Get Columns"))
        #self.ln_table_col.setPlaceholderText(_translate("MainWindow", "Number of each columns, Ex: 1,2,3,5,8"))
        self.l_table_nr_rows.setText(_translate("MainWindow", "Number of rows:"))
        self.cb_table_get_columns.setText(_translate("MainWindow", "Get All Columns"))
        self.cb_table_get_rows.setText(_translate("MainWindow", "Get All Rows"))
        self.cb_table_non_ascii.setText(_translate("MainWindow", "DEL non-ASCII"))
        self.l_table_save.setText(_translate("MainWindow", "Save as:"))
        self.rb_table_json.setText(_translate("MainWindow", "JSON"))
        self.rb_table_mysql.setText(_translate("MainWindow", "MySQL"))
        self.rb_table_csv.setText(_translate("MainWindow", "CSV"))
        self.l_table_file.setText(_translate("MainWindow", "File Name:"))
        self.pb_table_save.setText(_translate("MainWindow", "Save"))
        self.l_table_pages.setText(_translate("MainWindow", "Tables:"))
        #self.ln_table_pages.setPlaceholderText(_translate("MainWindow", "Number of each page to scrape"))
        self.cb_table_get_pages.setText(_translate("MainWindow", "Get All Tables"))
        self.l_table_path.setText(_translate("MainWindow", "Path:"))
        self.tab.setTabText(self.tab.indexOf(self.Table), _translate("MainWindow", "Table"))
        ################
        self.l_email_url.setText(_translate("MainWindow", "URL:"))
        self.l_email_page_nr.setText(_translate("MainWindow", "Number of pages:"))
        self.pb_email_save.setText(_translate("MainWindow", "Save"))
        self.rb_email_mysql.setText(_translate("MainWindow", "MySQL"))
        self.l_email_path.setText(_translate("MainWindow", "Path:"))
        #self.ln_email_url.setPlaceholderText(_translate("MainWindow", "current URL"))
        self.rb_email_json.setText(_translate("MainWindow", "JSON"))
        self.l_email_file.setText(_translate("MainWindow", "File Name:"))
        self.l_email_save.setText(_translate("MainWindow", "Save as:"))
        self.rb_email_csv.setText(_translate("MainWindow", "CSV"))
        ###########
        self.l_image_search.setText(_translate("MainWindow", "Search images with:"))
        #self.ln_image_search.setText(_translate("MainWindow", "URL:"))
        self.l_image_nr.setText(_translate("MainWindow", "Number of images:"))
        self.l_image_dest.setText(_translate("MainWindow", "Destination PATH:"))
        self.pb_image_save.setText(_translate("MainWindow", "Save"))
        ####################
        self.tab.setTabText(self.tab.indexOf(self.Emails), _translate("MainWindow", "E-mails"))
        self.tab.setTabText(self.tab.indexOf(self.Image), _translate("MainWindow", "Image"))

    def changePage(self):
        start = time.time()
        url1 = QtCore.QUrl(self.ln_addressbar.sender().url().url())
        self.color_iterator = 0
        if url1.isValid():
            self.ln_addressbar.setText(self.webView.sender().url().url())
            self.ln_table_url.setText(self.webView.sender().url().url())
            self.ln_table_file.setText(str(os.path.split(self.webView.sender().url().url())[1]))
            self.ln_email_url.setText(self.webView.sender().url().url())
            self.ln_email_file.setText(str(os.path.split(self.webView.sender().url().url())[1]))
            self.image_table.clear()
            self.sourceView.clear()
            response = requests.get(str(self.ln_addressbar.sender().url().url()))
            soup = BeautifulSoup(response.text, 'html.parser')
            self.sourceView.insertPlainText(soup.prettify())
            self.sourceView.setReadOnly(True)
            #self.color_search_word('text')
            print(url1.isValid())
        else:
            try:
                html = urlopen(url)
            except URLError as e:
                self.ln_addressbar.setText("Error 404")
                self.webView.load(QtCore.QUrl("file:///home/palade/Documents/proiecte/Sisteme de Operare/WebScraper/errors/ServernotFound.png"))
            except HTTPError as e:
                self.ln_addressbar.setText("Server not Found")
                self.webView.load(QtCore.QUrl("file:///home/palade/Documents/proiecte/Sisteme de Operare/WebScraper/errors/Error404.png"))
        end = time.time()
        print(end - start)

    def table_ws(self):
        self.pb_table = QtWidgets.QPushButton(self.centralwidget)
        self.pb_table.setGeometry(QtCore.QRect((self.width - 260), 300, 85, 27))
        self.pb_table.setObjectName("pb_table")
        font2 = QtGui.QFont()
        font2.setFamily("URW Palladio L")
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(True)
        font2.setWeight(75)
        self.pb_table.setFont(font2)
        self.pb_table.setText("Lala")

    def color_search_word(self):
        start = time.time()
        #############
        cursor = self.sourceView.textCursor()
        pattern = self.ln_sourceView_search_word.text()
        # Setup the desired format for matches
        format = QtGui.QTextCharFormat()
        if self.color_iterator == len(self.color):
            self.color_iterator = 0
            print(self.color_iterator)
        format.setBackground(QtGui.QBrush(QtGui.QColor(self.color[self.color_iterator][0], self.color[self.color_iterator][1], self.color[self.color_iterator][2], self.color[self.color_iterator][3])))
        # Setup the regex engine
        regex = QtCore.QRegExp(pattern)
        # Process the displayed document
        pos = 0
        index = regex.indexIn(self.sourceView.toPlainText(), pos)
        while (index != -1):
            # Select the matched text and apply the desired format
            cursor.setPosition(index)
            cursor.movePosition(QtGui.QTextCursor.EndOfWord, 1)
            cursor.mergeCharFormat(format)
            # Move to the next match
            pos = index + regex.matchedLength()
            index = regex.indexIn(self.sourceView.toPlainText(), pos)
        self.color_iterator += 1
        end = time.time()
        print(end - start)

    def color_clear(self):
        self.sourceView.clear()
        response = requests.get(str(self.ln_addressbar.text()))
        soup = BeautifulSoup(response.text, 'html.parser')
        self.sourceView.insertPlainText(soup.prettify())
        self.sourceView.setReadOnly(True)
        self.color_iterator = 0

    def setupUi(self, MainWindow):
        start = time.time()
        sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        self.width = sizeObject.width()
        self.height = sizeObject.height()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1362, 748)
        MainWindow.showMaximized()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        ########## Reload ##########
        self.tb_reload = QtWidgets.QToolButton(self.centralwidget)
        self.tb_reload.setGeometry(QtCore.QRect(50, 10, 31, 31))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/reload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_reload.setIcon(icon)
        self.tb_reload.setObjectName("tb_reload")
        ########## -> Event  ###########
        self.tb_reload.clicked.connect(self.reload)
        ################################

        ########## Home ##########
        self.tb_home = QtWidgets.QToolButton(self.centralwidget)
        self.tb_home.setGeometry(QtCore.QRect(90, 10, 31, 31))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_home.setIcon(icon1)
        self.tb_home.setObjectName("tb_home")
        ########## -> Event  ###########
        self.tb_home.clicked.connect(self.home)
        ################################

        ########## Forward ##########
        self.tb_forward = QtWidgets.QToolButton(self.centralwidget)
        self.tb_forward.setGeometry(QtCore.QRect(130, 10, 31, 31))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/forword.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_forward.setIcon(icon2)
        self.tb_forward.setObjectName("tb_forward")
        ########## -> Event  ###########
        self.tb_forward.clicked.connect(self.forward)
        ################################

        ########## Search ##########
        self.tb_search = QtWidgets.QToolButton(self.centralwidget)
        self.tb_search.setGeometry(QtCore.QRect((self.width-120), 10, 31, 31))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_search.setIcon(icon3)
        self.tb_search.setObjectName("tb_search")
        ########## -> Event  ###########
        self.tb_search.clicked.connect(self.search)
        ################################

        ########## WebScraper ##########
        self.tb_WebScraper = QtWidgets.QToolButton(self.centralwidget)
        self.tb_WebScraper.setGeometry(QtCore.QRect((self.width-80), 10, 31, 31))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/soup.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_WebScraper.setIcon(icon3)
        self.tb_WebScraper.setObjectName("tb_search")
        ########## -> Event  ###########
        self.tb_WebScraper.clicked.connect(self.WebScraper)
        ########## Label Web Scraper ##########
        self.l_webscraper = QtWidgets.QLabel(self.centralwidget)
        self.l_webscraper.setGeometry(QtCore.QRect((self.width-250), 50, 300, 41))
        font = QtGui.QFont()
        font.setFamily("URW Palladio L")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.l_webscraper.setFont(font)
        self.l_webscraper.setObjectName("l_webscraper")
        self.l_webscraper.setText("Web Scraper")
        ########## Close Web Scraper ##########
        self.tb_close_ws = QtWidgets.QToolButton(self.centralwidget)
        self.tb_close_ws.setGeometry(QtCore.QRect((self.width-24), 65, 15, 15))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_close_ws.setIcon(icon3)
        self.tb_close_ws.setObjectName("tb_close_ws")
        ########## -> Event  ###########
        self.tb_close_ws.clicked.connect(self.dimensionPage)
        ########## Scrape Table ##########
        #self.pb_table = QtWidgets.QPushButton(self.centralwidget)
        #self.pb_table.setGeometry(QtCore.QRect((self.width-260), 95, 85, 27))
        #self.pb_table.setObjectName("pb_table")
        #font2 = QtGui.QFont()
        #font2.setFamily("URW Palladio L")
        #font2.setPointSize(10)
        #font2.setBold(False)
        #font2.setItalic(True)
        #font2.setWeight(75)
        #self.pb_table.setFont(font2)
        #self.pb_table.setText("Table")
        ########## -> Event  ###########
        #self.pb_table.clicked.connect(self.table_ws)
        ################################

        ########## WebCrawling ##########
        self.tb_search = QtWidgets.QToolButton(self.centralwidget)
        self.tb_search.setGeometry(QtCore.QRect((self.width-40), 10, 31, 31))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/spider.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_search.setIcon(icon3)
        self.tb_search.setObjectName("tb_search")
        ########################################
        ########## -> Event  ###########
        self.tb_search.clicked.connect(self.search)
        ################################

        ####--------------------------------------------#####
        ####################### TAB #########################
        ####--------------------------------------------#####
        self.tab = QtWidgets.QTabWidget(self.centralwidget)
        self.tab.setGeometry(QtCore.QRect((self.width-370), 95, 371, 620))
        #####################################################

        ################ Palette ############################
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        ############################################################################

        self.tab.setPalette(palette)
        self.tab.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tab.setObjectName("tab")

        ########## AddressBar ##########
        self.ln_addressbar = QtWidgets.QLineEdit(self.centralwidget)
        self.ln_addressbar.setGeometry(QtCore.QRect(170, 10, (self.width-300), 31))
        self.ln_addressbar.setObjectName("ln_addressbar")
        ########## -> Event  ###########
        # self.ln_addressbar.clicked.connect(self.goAddress)
        ################################

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ############### TAB -> Table ##################
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        self.Table = QtWidgets.QWidget()
        self.Table.setAcceptDrops(False)
        self.Table.setAutoFillBackground(True)
        self.Table.setObjectName("Table")

        ############## URL #####################
        # Label
        self.l_table_url = QtWidgets.QLabel(self.Table)
        self.l_table_url.setGeometry(QtCore.QRect(10, 40, 54, 17))
        self.l_table_url.setObjectName("l_table_url")
        # Line Edit
        self.ln_table_url = QtWidgets.QLineEdit(self.Table)
        self.ln_table_url.setGeometry(QtCore.QRect(40, 30, 311, 31))
        self.ln_table_url.setObjectName("ln_table_url")
        ############# -> Event ##############
        self.ln_table_url.returnPressed.connect(self.change_url)
        #####################################

        ############# Table Name ###############
        # Label
        self.l_table_key_word = QtWidgets.QLabel(self.Table)
        self.l_table_key_word.setGeometry(QtCore.QRect(10, 90, 71, 17))
        self.l_table_key_word.setObjectName("l_table_key_word")
        # Line Edit
        self.ln_table_key_word = QtWidgets.QLineEdit(self.Table)
        self.ln_table_key_word.setGeometry(QtCore.QRect(90, 80, 261, 31))
        self.ln_table_key_word.setObjectName("ln_table_key_word")

        ############## Columns ##################
        # Label
        self.l_table_nr_columns = QtWidgets.QLabel(self.Table)
        self.l_table_nr_columns.setGeometry(QtCore.QRect(10, 140, 81, 17))
        self.l_table_nr_columns.setObjectName("l_table_nr_columns")
        # Line Edit
        self.ln_table_col = QtWidgets.QLineEdit(self.Table)
        self.ln_table_col.setGeometry(QtCore.QRect(90, 130, 131, 31))
        self.ln_table_col.setText("")
        self.ln_table_col.setObjectName("ln_table_col")
        self.l_table_nr_rows = QtWidgets.QLabel(self.Table)
        # Check Box
        self.cb_table_get_columns = QtWidgets.QCheckBox(self.Table)
        self.cb_table_get_columns.setGeometry(QtCore.QRect(230, 140, 121, 22))
        self.cb_table_get_columns.setChecked(True)
        self.cb_table_get_columns.setObjectName("cb_table_get_columns")

        ################ Rows #########################
        # Label
        self.l_table_nr_rows.setGeometry(QtCore.QRect(10, 190, 101, 17))
        self.l_table_nr_rows.setObjectName("l_table_nr_rows")
        # Line Edit
        self.ln_table_rows = QtWidgets.QLineEdit(self.Table)
        self.ln_table_rows.setGeometry(QtCore.QRect(110, 180, 111, 31))
        self.ln_table_rows.setText("")
        self.ln_table_rows.setPlaceholderText("")
        self.ln_table_rows.setObjectName("ln_table_rows")
        # Check Box
        self.cb_table_get_rows = QtWidgets.QCheckBox(self.Table)
        self.cb_table_get_rows.setGeometry(QtCore.QRect(230, 190, 121, 22))
        self.cb_table_get_rows.setChecked(True)
        self.cb_table_get_rows.setObjectName("cb_table_get_rows")

        ########## Non-ASCII characters #############
        # Check Box
        self.cb_table_non_ascii = QtWidgets.QCheckBox(self.Table)
        self.cb_table_non_ascii.setGeometry(QtCore.QRect(70, 410, 101, 22))
        self.cb_table_non_ascii.setChecked(True)
        self.cb_table_non_ascii.setObjectName("cb_table_non_ascii")

        ################# Save ######################
        self.l_table_save = QtWidgets.QLabel(self.Table)
        self.l_table_save.setGeometry(QtCore.QRect(10, 360, 101, 17))
        self.l_table_save.setObjectName("l_table_save")
        # Radio - JSON
        self.rb_table_json = QtWidgets.QRadioButton(self.Table)
        self.rb_table_json.setGeometry(QtCore.QRect(150, 370, 101, 22))
        self.rb_table_json.setObjectName("rb_table_json")
        # Radio - MySql
        self.rb_table_mysql = QtWidgets.QRadioButton(self.Table)
        self.rb_table_mysql.setGeometry(QtCore.QRect(240, 370, 101, 22))
        self.rb_table_mysql.setObjectName("rb_table_mysql")
        # Radio - CSV
        self.rb_table_csv = QtWidgets.QRadioButton(self.Table)
        self.rb_table_csv.setGeometry(QtCore.QRect(70, 370, 101, 22))
        self.rb_table_csv.setChecked(True)
        self.rb_table_csv.setObjectName("rb_table_csv")
        # Push Button
        self.pb_table_save = QtWidgets.QPushButton(self.Table)
        self.pb_table_save.setGeometry(QtCore.QRect(270, 410, 85, 27))
        self.pb_table_save.setObjectName("pb_table_save")
        ################ -> Event #####################
        self.pb_table_save.clicked.connect(self.pb_tab_save)
        ###############################################

        ################## File ########################
        # Label
        self.l_table_file = QtWidgets.QLabel(self.Table)
        self.l_table_file.setGeometry(QtCore.QRect(10, 290, 101, 17))
        self.l_table_file.setObjectName("l_table_file")
        # Line Edit
        self.ln_table_file = QtWidgets.QLineEdit(self.Table)
        self.ln_table_file.setGeometry(QtCore.QRect(80, 280, 271, 31))
        self.ln_table_file.setObjectName("ln_table_file")

        #################### Image ########################
        self.image_table = QtWidgets.QLabel(self.Table)
        self.image_table.setGeometry(QtCore.QRect(10, 450, 341, 120))

        ################### Table nr #########################
        # Label
        self.l_table_pages = QtWidgets.QLabel(self.Table)
        self.l_table_pages.setGeometry(QtCore.QRect(10, 240, 41, 17))
        self.l_table_pages.setObjectName("l_table_pages")
        # Line Edit
        self.ln_table_pages = QtWidgets.QLineEdit(self.Table)
        self.ln_table_pages.setGeometry(QtCore.QRect(80, 230, 141, 31))
        self.ln_table_pages.setText("")
        self.ln_table_pages.setObjectName("ln_table_pages")
        # Check Box
        self.cb_table_get_pages = QtWidgets.QCheckBox(self.Table)
        self.cb_table_get_pages.setGeometry(QtCore.QRect(230, 240, 121, 22))
        self.cb_table_get_pages.setChecked(True)
        self.cb_table_get_pages.setObjectName("cb_table_get_pages")

        ################### Path ############################
        # Label
        self.l_table_path = QtWidgets.QLabel(self.Table)
        self.l_table_path.setGeometry(QtCore.QRect(10, 330, 101, 17))
        self.l_table_path.setObjectName("l_table_path")
        # Line Edit
        self.ln_table_path = QtWidgets.QLineEdit(self.Table)
        self.ln_table_path.setGeometry(QtCore.QRect(80, 320, 271, 31))
        self.ln_table_path.setObjectName("ln_table_path")

        ########################################################
        ########################################################

        ####################### TAB -> Emails #########################
        self.tab.addTab(self.Table, "")
        self.Emails = QtWidgets.QWidget()
        self.Emails.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.Emails.setObjectName("Emails")
        #
        ########################## URL ###############################
        # Label
        self.l_email_url = QtWidgets.QLabel(self.Emails)
        self.l_email_url.setGeometry(QtCore.QRect(10, 55, 54, 17))
        self.l_email_url.setObjectName("l_email_url")
        # Line Edit
        self.ln_email_url = QtWidgets.QLineEdit(self.Emails)
        self.ln_email_url.setGeometry(QtCore.QRect(40, 50, 311, 31))
        self.ln_email_url.setObjectName("ln_email_url")

        ######################### Path ###############################
        # Label
        self.l_email_path = QtWidgets.QLabel(self.Emails)
        self.l_email_path.setGeometry(QtCore.QRect(10, 235, 101, 17))
        self.l_email_path.setObjectName("l_email_path")
        # Line Edit
        self.ln_email_path = QtWidgets.QLineEdit(self.Emails)
        self.ln_email_path.setGeometry(QtCore.QRect(80, 230, 271, 31))
        self.ln_email_path.setObjectName("ln_email_path")

        ######################### Number of pages ############################
        # Label
        self.l_email_page_nr = QtWidgets.QLabel(self.Emails)
        self.l_email_page_nr.setGeometry(QtCore.QRect(10, 105, 130, 17))
        self.l_email_page_nr.setObjectName("l_email_page_nr")
        # Line Edit
        self.ln_email_page_nr = QtWidgets.QLineEdit(self.Emails)
        self.ln_email_page_nr.setGeometry(QtCore.QRect(130, 100, 221, 31))
        self.ln_email_page_nr.setObjectName("ln_email_page_nr")
        # Check Box
        self.cb_email_pages = QtWidgets.QCheckBox(self.Emails)
        self.cb_email_pages.setGeometry(QtCore.QRect(260, 140, 121, 22))
        self.cb_email_pages.setChecked(True)
        self.cb_email_pages.setObjectName("cb_email_pages")
        self.cb_email_pages.setText("Get All Pages")

        ########################## Save ###############################
        # Label
        self.l_email_save = QtWidgets.QLabel(self.Emails)
        self.l_email_save.setGeometry(QtCore.QRect(10, 350, 101, 17))
        self.l_email_save.setObjectName("l_email_save")
        # Push Button
        self.pb_email_save = QtWidgets.QPushButton(self.Emails)
        self.pb_email_save.setGeometry(QtCore.QRect(270, 400, 85, 27))
        self.pb_email_save.setObjectName("pb_email_save")
        self.pb_email_save.clicked.connect(self.email_save)
        # Radio -> MySql
        self.rb_email_mysql = QtWidgets.QRadioButton(self.Emails)
        self.rb_email_mysql.setGeometry(QtCore.QRect(240, 360, 101, 22))
        self.rb_email_mysql.setObjectName("rb_email_mysql")
        # Radio -> JSON
        self.rb_email_json = QtWidgets.QRadioButton(self.Emails)
        self.rb_email_json.setGeometry(QtCore.QRect(150, 360, 101, 22))
        self.rb_email_json.setObjectName("rb_email_json")
        # Radio -> CSV
        self.rb_email_csv = QtWidgets.QRadioButton(self.Emails)
        self.rb_email_csv.setGeometry(QtCore.QRect(70, 360, 101, 22))
        self.rb_email_csv.setObjectName("rb_email_csv")

        ########################## Image ##############################
        self.image_emails = QtWidgets.QGraphicsView(self.Emails)
        self.image_emails.setGeometry(QtCore.QRect(10, 440, 341, 91))
        self.image_emails.setObjectName("image_emails")

        ######################### File ###############################
        # Label
        self.l_email_file = QtWidgets.QLabel(self.Emails)
        self.l_email_file.setGeometry(QtCore.QRect(10, 185, 271, 17))
        self.l_email_file.setObjectName("l_email_file")
        # Line Edit
        self.ln_email_file = QtWidgets.QLineEdit(self.Emails)
        self.ln_email_file.setGeometry(QtCore.QRect(80, 180, 271, 31))
        self.ln_email_file.setObjectName("ln_email_file")
        ################################################################
        ################################################################

        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        ####################### TAB -> Image #########################
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        self.tab.addTab(self.Table, "")
        self.Image = QtWidgets.QWidget()
        self.Image.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.Image.setObjectName("Image")

        ########################## Search  ###############################
        # Label
        self.l_image_search = QtWidgets.QLabel(self.Image)
        self.l_image_search.setGeometry(QtCore.QRect(10, 55, 135, 17))
        self.l_image_search.setObjectName("l_image_search")
        # Line Edit
        self.ln_image_search = QtWidgets.QLineEdit(self.Image)
        self.ln_image_search.setGeometry(QtCore.QRect(135, 50, 220, 31))
        self.ln_image_search.setObjectName("ln_image_search")

        ################# Image ####################
        self.image_imag = QtWidgets.QLabel(self.Image)
        self.image_imag.setGeometry(QtCore.QRect(10, 450, 341, 120))

        ################# Number of images  ####################
        # Label
        self.l_image_nr = QtWidgets.QLabel(self.Image)
        self.l_image_nr.setGeometry(QtCore.QRect(10, 105, 135, 17))
        self.l_image_nr.setObjectName("l_image_nr")
        # Line Edit
        self.ln_image_nr = QtWidgets.QLineEdit(self.Image)
        self.ln_image_nr.setGeometry(QtCore.QRect(135, 100, 220, 31))
        self.ln_image_nr.setObjectName("ln_image_nr")

        ################# Destination PATH  ####################
        # Label
        self.l_image_dest = QtWidgets.QLabel(self.Image)
        self.l_image_dest.setGeometry(QtCore.QRect(10, 155, 135, 17))
        self.l_image_dest.setObjectName("l_image_dest")
        # Line Edit
        self.ln_image_dest = QtWidgets.QLineEdit(self.Image)
        self.ln_image_dest.setGeometry(QtCore.QRect(135, 150, 220, 31))
        self.ln_image_dest.setObjectName("ln_image_dest")

        ########################## Save ###############################
        # Push Button
        self.pb_image_save = QtWidgets.QPushButton(self.Image)
        self.pb_image_save.setGeometry(QtCore.QRect(270, 400, 85, 27))
        self.pb_image_save.setObjectName("pb_image_save")
        self.pb_image_save.clicked.connect(self.pb_imag_save)
        # Set color
        self.l_image_set_color = QtWidgets.QLabel(self.Image)
        self.l_image_set_color.setGeometry(QtCore.QRect(10, 220, 135, 17))
        self.l_image_set_color.setObjectName("l_image_set_color")
        self.l_image_set_color.setText("Color: ")
        x = 10
        y = 17
        # Radio -> Search RED images
        self.rb_image_red = QtWidgets.QRadioButton(self.Image)
        self.rb_image_red.setGeometry(QtCore.QRect(x, 250, 101, 22))
        self.rb_image_red.setObjectName("rb_image_red")
        x = x + y
        # Label -> Search RED images
        self.l_image_red = QtWidgets.QLabel(self.Image)
        self.l_image_red.setGeometry(QtCore.QRect(x, 250, 22, 22))
        self.l_image_red.setObjectName("l_image_red")
        self.l_image_red.setStyleSheet("QLabel { background-color : red}")
        x = x + 2*y
        # Radio -> Search ORANGE images
        self.rb_image_orange = QtWidgets.QRadioButton(self.Image)
        self.rb_image_orange.setGeometry(QtCore.QRect(x, 250, 101, 22))
        self.rb_image_orange.setObjectName("rb_image_orange")
        x = x + y
        # Label -> Search ORANGE images
        self.l_image_orange= QtWidgets.QLabel(self.Image)
        self.l_image_orange.setGeometry(QtCore.QRect(x, 250, 22, 22))
        self.l_image_orange.setObjectName("l_image_orange")
        self.l_image_orange.setStyleSheet("QLabel { background-color : orange}")
        x = x + 2 * y
        # Radio -> Search YELLOW images
        self.rb_image_yellow = QtWidgets.QRadioButton(self.Image)
        self.rb_image_yellow.setGeometry(QtCore.QRect(x, 250, 101, 22))
        self.rb_image_yellow.setObjectName("rb_image_yellow")
        x = x + y
        # Label -> Search YELLOW images
        self.l_image_yellow= QtWidgets.QLabel(self.Image)
        self.l_image_yellow.setGeometry(QtCore.QRect(x, 250, 22, 22))
        self.l_image_yellow.setObjectName("l_image_yellow")
        self.l_image_yellow.setStyleSheet("QLabel { background-color : yellow}")
        x = x + 2 * y
        # Radio -> Search GREEN images
        self.rb_image_green = QtWidgets.QRadioButton(self.Image)
        self.rb_image_green.setGeometry(QtCore.QRect(x, 250, 101, 22))
        self.rb_image_green.setObjectName("rb_image_green")
        x = x + y
        # Label -> Search GREEN images
        self.l_image_green = QtWidgets.QLabel(self.Image)
        self.l_image_green.setGeometry(QtCore.QRect(x, 250, 22, 22))
        self.l_image_green.setObjectName("l_image_green")
        self.l_image_green.setStyleSheet("QLabel { background-color : green}")
        x = x + 2 * y
        # Radio -> Search ALICE images
        self.rb_image_alice = QtWidgets.QRadioButton(self.Image)
        self.rb_image_alice.setGeometry(QtCore.QRect(x, 250, 101, 22))
        self.rb_image_alice.setObjectName("rb_image_alice")
        x = x + y
        # Label -> Search ALICE images
        self.l_image_alice = QtWidgets.QLabel(self.Image)
        self.l_image_alice.setGeometry(QtCore.QRect(x, 250, 22, 22))
        self.l_image_alice.setObjectName("l_image_alice")
        self.l_image_alice.setStyleSheet("QLabel { background-color : blue}")
        x = x + 2 * y
        # Radio -> Search PURPLE images
        self.rb_image_purple = QtWidgets.QRadioButton(self.Image)
        self.rb_image_purple.setGeometry(QtCore.QRect(x, 250, 101, 22))
        self.rb_image_purple.setObjectName("rb_image_purple")
        x = x + y
        # Label -> Search PURPLE images
        self.l_image_purple= QtWidgets.QLabel(self.Image)
        self.l_image_purple.setGeometry(QtCore.QRect(x, 250, 22, 22))
        self.l_image_purple.setObjectName("l_image_purple")
        self.l_image_purple.setStyleSheet("QLabel { background-color : purple}")
        x = x + 2 * y
        # Radio -> Search PINK images
        self.rb_image_pink = QtWidgets.QRadioButton(self.Image)
        self.rb_image_pink.setGeometry(QtCore.QRect(x, 250, 101, 22))
        self.rb_image_pink.setObjectName("rb_image_pink")
        x = x + y
        # Label -> Search PINK images
        self.l_image_pink = QtWidgets.QLabel(self.Image)
        self.l_image_pink.setGeometry(QtCore.QRect(x, 250, 22, 22))
        self.l_image_pink.setObjectName("l_image_pink")
        self.l_image_pink.setStyleSheet("QLabel { background-color : pink}")

        # Radio -> Search BLACK images
        self.rb_image_black = QtWidgets.QRadioButton(self.Image)
        self.rb_image_black.setGeometry(QtCore.QRect(10, 290, 101, 22))
        self.rb_image_black.setObjectName("rb_image_black")
        # Label -> Search BLACK images
        self.l_image_black = QtWidgets.QLabel(self.Image)
        self.l_image_black.setGeometry(QtCore.QRect(27, 290, 22, 22))
        self.l_image_black.setObjectName("l_image_black")
        self.l_image_black.setStyleSheet("QLabel { background-color : black}")
        # Radio -> Search GRAY images
        self.rb_image_gray = QtWidgets.QRadioButton(self.Image)
        self.rb_image_gray.setGeometry(QtCore.QRect(61, 290, 101, 22))
        self.rb_image_gray.setObjectName("rb_image_white")
        # Label -> Search GRAY images
        self.l_image_gray = QtWidgets.QLabel(self.Image)
        self.l_image_gray.setGeometry(QtCore.QRect(78, 290, 22, 22))
        self.l_image_gray.setObjectName("l_image_gray")
        self.l_image_gray.setStyleSheet("QLabel { background-color : gray}")
        # Radio -> Search WHITE images
        self.rb_image_white = QtWidgets.QRadioButton(self.Image)
        self.rb_image_white.setGeometry(QtCore.QRect(111, 290, 101, 22))
        self.rb_image_white.setObjectName("rb_image_white")
        # Label -> Search WHITE images
        self.l_image_whiteb = QtWidgets.QLabel(self.Image)
        self.l_image_whiteb.setGeometry(QtCore.QRect(128, 290, 22, 22))
        self.l_image_whiteb.setObjectName("l_image_whiteb")
        self.l_image_whiteb.setStyleSheet("QLabel { background-color : black}")
        self.l_image_white = QtWidgets.QLabel(self.Image)
        self.l_image_white.setGeometry(QtCore.QRect(129, 291, 20, 20))
        self.l_image_white.setObjectName("l_image_white")
        self.l_image_white.setStyleSheet("QLabel { background-color : white}")
        # Radio -> Search Transparent images
        self.rb_image_trans = QtWidgets.QRadioButton(self.Image)
        self.rb_image_trans.setGeometry(QtCore.QRect(10, 325, 101, 22))
        self.rb_image_trans.setObjectName("rb_image_trans")
        self.rb_image_trans.setText("Transparent")
        # Radio -> Search Transparent images
        self.rb_image_none = QtWidgets.QRadioButton(self.Image)
        self.rb_image_none.setGeometry(QtCore.QRect(110, 325, 101, 22))
        self.rb_image_none.setObjectName("rb_image_none")
        self.rb_image_none.setText("NONE")
        self.rb_image_none.setChecked(True)


        ################################################################
        ################################################################

        self.tab.addTab(self.Image, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.tab.addTab(self.Image, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.tab.addTab(self.Emails, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ########## Source View ##########
        self.sourceView = QtWidgets.QTextEdit(self.centralwidget)
        self.sourceView.setGeometry(10, (self.height-240), (self.width-379), (self.height-603))
        self.sourceView.setObjectName("sourceView")
        # Label
        self.l_sourceView_search_word = QtWidgets.QLabel(self.sourceView)
        self.l_sourceView_search_word.setGeometry(QtCore.QRect(650, 2, 50, 17))
        self.l_sourceView_search_word.setObjectName("l_sourceView_search_word")
        self.l_sourceView_search_word.setText("Search: ")
        self.l_sourceView_search_word.setAutoFillBackground(True)

        # Line Edit
        self.ln_sourceView_search_word = QtWidgets.QLineEdit(self.sourceView)
        self.ln_sourceView_search_word.setGeometry(QtCore.QRect(700, 0, (self.width-1020), 20))
        self.ln_sourceView_search_word.setObjectName("ln_sourceView_search_word")
        self.ln_sourceView_search_word.returnPressed.connect(self.color_search_word)

        # Search Button
        self.tb_sourceView_search_word = QtWidgets.QToolButton(self.sourceView)
        self.tb_sourceView_search_word.setGeometry(QtCore.QRect((self.width-453), 0, 20, 20))
        icon31 = QtGui.QIcon()
        icon31.addPixmap(QtGui.QPixmap("icons/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_sourceView_search_word.setIcon(icon31)
        self.tb_sourceView_search_word.setObjectName("tb_sourceView_search_word")
        ########## -> Event  ###########
        self.tb_sourceView_search_word.clicked.connect(self.color_search_word)

        # Delete Search Word
        self.tb_sourceView_del_word = QtWidgets.QToolButton(self.sourceView)
        self.tb_sourceView_del_word.setGeometry(QtCore.QRect((self.width - 433), 0, 20, 20))
        icon31 = QtGui.QIcon()
        icon31.addPixmap(QtGui.QPixmap("icons/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_sourceView_del_word.setIcon(icon31)
        self.tb_sourceView_del_word.setObjectName("tb_sourceView_del_word")
        ########## -> Event  ###########
        self.tb_sourceView_del_word.clicked.connect(self.color_clear)

        # Close Source View
        self.tb_sourceView_close_word = QtWidgets.QToolButton(self.sourceView)
        self.tb_sourceView_close_word.setGeometry(QtCore.QRect((self.width - 413), 0, 20, 20))
        icon31 = QtGui.QIcon()
        icon31.addPixmap(QtGui.QPixmap("icons/forword.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_sourceView_close_word.setIcon(icon31)
        self.tb_sourceView_close_word.setObjectName("tb_sourceView_close_word")
        ########## -> Event  ###########
        self.tb_sourceView_close_word.clicked.connect(self.dimensionPage2)

        ########## Web View ##########
        self.webView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.dimensionPage()
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.webView.load(QtCore.QUrl("http://www.google.com"))
        ########## _> Event ##########
        self.webView.loadFinished.connect(self.changePage)
        ################################

        ########## Back ##########
        self.tb_back = QtWidgets.QToolButton(self.centralwidget)
        self.tb_back.setGeometry(QtCore.QRect(10, 10, 31, 31))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_back.setIcon(icon4)
        self.tb_back.setObjectName("tb_back")
        ########## -> Event  ###########
        self.tb_back.clicked.connect(self.back)
        ################################

        ########## Menu Bar ##########
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        ########## Stop Bash Script #########
        #self.pb_stop_bs = QtWidgets.QPushButton(self.centralwidget)
        #self.pb_stop_bs.setGeometry(QtCore.QRect((self.width-100), (self.height - 100), 99, 20))
        #self.pb_stop_bs.setStyleSheet("background-color: red")
        #self.pb_stop_bs.setText("STOP Alarm")
        #self.pb_stop_bs.clicked.connect(self.open_script)

        ########## Pause Process #########
        #self.pb_pause_bs = QtWidgets.QPushButton(self.centralwidget)
        #self.pb_pause_bs.setGeometry(QtCore.QRect((self.width - 200), (self.height - 100), 98, 20))
        #self.pb_pause_bs.setStyleSheet("background-color: yellow")
        #self.pb_pause_bs.setText("PAUSE")
        #self.pb_pause_bs.clicked.connect(self.open_script)

        ########## Resume Process #########
        #self.pb_resume_bs = QtWidgets.QPushButton(self.centralwidget)
        #self.pb_resume_bs.setGeometry(QtCore.QRect((self.width - 300), (self.height - 100), 98, 20))
        #self.pb_resume_bs.setStyleSheet("background-color: green")
        #self.pb_resume_bs.setText("RESUME")
        #self.pb_resume_bs.clicked.connect(self.open_script)

        end = time.time()
        print(end - start)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

