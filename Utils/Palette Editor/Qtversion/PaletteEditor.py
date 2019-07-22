# -*- coding: utf-8 -*-

#Copyright (c) Rocketchip 2019

# Created by: PyQt5 UI code generator 5.12.1


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def __init__(self):
        self.data = [(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0)]
        self.file_path = None

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow 
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 100)
        MainWindow.setWindowIcon(QtGui.QIcon('imgs/palette.ico'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.Button3 = QtWidgets.QPushButton(self.centralwidget)
        self.Button3.setText("")
        self.Button3.setObjectName("Button3")
        self.gridLayout.addWidget(self.Button3, 0, 2, 1, 1)
        self.Button2 = QtWidgets.QPushButton(self.centralwidget)
        self.Button2.setText("")
        self.Button2.setObjectName("Button2")
        self.gridLayout.addWidget(self.Button2, 0, 1, 1, 1)
        self.Button4 = QtWidgets.QPushButton(self.centralwidget)
        self.Button4.setText("")
        self.Button4.setObjectName("Button4")
        self.gridLayout.addWidget(self.Button4, 0, 4, 1, 1)
        self.Button5 = QtWidgets.QPushButton(self.centralwidget)
        self.Button5.setText("")
        self.Button5.setObjectName("Button5")
        self.gridLayout.addWidget(self.Button5, 2, 0, 1, 1)
        self.Button1 = QtWidgets.QPushButton(self.centralwidget)
        self.Button1.setText("")
        self.Button1.setObjectName("Button1")
        self.gridLayout.addWidget(self.Button1, 0, 0, 1, 1)
        self.Button8 = QtWidgets.QPushButton(self.centralwidget)
        self.Button8.setText("")
        self.Button8.setObjectName("Button8")
        self.gridLayout.addWidget(self.Button8, 2, 4, 1, 1)
        self.Button6 = QtWidgets.QPushButton(self.centralwidget)
        self.Button6.setText("")
        self.Button6.setObjectName("Button6")
        self.gridLayout.addWidget(self.Button6, 2, 1, 1, 1)
        self.Button7 = QtWidgets.QPushButton(self.centralwidget)
        self.Button7.setText("")
        self.Button7.setObjectName("Button7")
        self.gridLayout.addWidget(self.Button7, 2, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        for i in range(1,9):
            exec('self.Button'+str(i)+'.setStyleSheet("QWidget { background-color: rgb(0,0,0)}")')

        self.Button1.clicked.connect(lambda : self.color_picker(self.Button1, 1))
        self.Button2.clicked.connect(lambda : self.color_picker(self.Button2, 2))
        self.Button3.clicked.connect(lambda : self.color_picker(self.Button3, 3))
        self.Button4.clicked.connect(lambda : self.color_picker(self.Button4, 4))
        self.Button5.clicked.connect(lambda : self.color_picker(self.Button5, 5))
        self.Button6.clicked.connect(lambda : self.color_picker(self.Button6, 6))
        self.Button7.clicked.connect(lambda : self.color_picker(self.Button7, 7))
        self.Button8.clicked.connect(lambda : self.color_picker(self.Button8, 8))

        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_as.triggered.connect(self.save_as)
        self.actionAbout.triggered.connect(self.about_dialog)
        self.actionExit.triggered.connect(QtCore.QCoreApplication.instance().quit)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as..."))
        self.actionSave_as.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

    def color_picker(self, button, button_id):
        color = QtWidgets.QColorDialog.getColor()
        print(color.blue())
        rgb = (color.red(),color.green(),color.blue())
        print(rgb)
        self.data[button_id-1] = rgb
        button.setStyleSheet("QWidget { background-color: %s}" % color.name())

    def save(self):
        print(self.data)
        print(self.file_path)
        if self.file_path != None:
            with open(self.file_path[0], "w") as file:
                try:
                    for y in range(0, len(self.data)):
                        for x in range(0, len(self.data[y])):
                            data = str(self.data[y][x])
                            if len(data) == 1:
                                data = "00"+data
                            elif len(data) == 2:
                                data = "0"+data
                            file.write(data)
                    file.write("this data and the programs associated with it are made by Rocket-chip team, DON'T STEAL THEM, and credit us")
                except:
                    print("Error")
        else:
            popup = QtWidgets.QMessageBox()
            popup.setIcon(QtWidgets.QMessageBox.Warning)
            popup.setText("No file choosen")
            # popup.setInformativeText("")
            popup.setWindowTitle("Alert!")
            # popup.setDetailedText("The details are as follows:")

            x = popup.exec_()

    def save_as(self):
        self.file_path = QtWidgets.QFileDialog.getSaveFileName(self.MainWindow, 'Save File')
        self.save()

    def new_file(self, button):
        for i in range(1,9):
            exec('self.Button'+str(i)+'.setStyleSheet("QWidget { background-color: rgb(0,0,0)}")')
        self.file_path = None
        self.data = []
        for y in range(1, 9):
            self.data.append((0, 0, 0))

    def open_file(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self.MainWindow,"Open File")
        print(path)
        with open(path[0], "r") as file:
            data = file.read()
            print(data)
            temp = []
            for y in range(0, 8):
                temp.append((int(data[y*9+0:y*9+0+3]),int(data[y*9+3:y*9+3+3]), int(data[y*9+6:y*9+6+3])))
            print(temp)
            self.data = temp
            #reinitialize colors of colrbuttons
            for i in range(1,9):
                exec('self.Button'+str(i)+'.setStyleSheet("QWidget { background-color: rgb('+str(self.data[i-1][0])+','+str(self.data[i-1][1])+','+str(self.data[i-1][2])+')}")')

    def about_dialog(self):
        dialog = QtWidgets.QMessageBox()
        dialog.setIconPixmap(QtGui.QPixmap("imgs/palette_scaled.ico"))
        dialog.setText("Palette Editor:")
        dialog.setInformativeText("version : 1.0\nlicence : MIT\nCopyright (c) Rocketchip 2019")
        dialog.setWindowTitle("About :")
        dialog.setDetailedText("\nCreated by Geek_Joystick and TwistedLlama\n\nWebsite: https://rocketchip-team.github.io/")

        x = dialog.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
