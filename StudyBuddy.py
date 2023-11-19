import sys
import os
import subprocess

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import configparser

#Variables
enabled_0 = False
enabled_1 = False
value_0 = 0
value_1 = 0
fileOpen = None
editMode = False
prev_score = 0
ovrall_score = 0

file_content = configparser.ConfigParser()
file_content["CONFIG"] = {}
file_content["IDENTIFICATION_Q"] = {}
file_content["IDENTIFICATION_A"] = {}

config = configparser.ConfigParser()
config['DEFAULT'] = {
    'multiplier' : 0.5,
    'zoom' : '1',
    'configured' : '0'
    }

try:
    with open('config.txt','r'):
        config.read('config.txt')
        multiplier = float(config.get('DEFAULT','multiplier'))
        zoom = float(config.get('DEFAULT','zoom'))
except FileNotFoundError:
    with open('config.txt', 'w') as configfile:
        config.write(configfile)
        multiplier = float(config.get('DEFAULT','multiplier'))
        zoom = float(config.get('DEFAULT','zoom'))

#Image button
class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

class object():
    pass

class Main_Menu(QWidget):
    def __init__(self, parent = None):
        super(Main_Menu, self).__init__(parent)
        self.pixmap_pencil = QPixmap('contents/pencil.png')
        
        self.title_txt = QLabel(self)
        self.title_txt.setText("Study Buddy")
        self.title_txt.setStyleSheet("font: " + str(int(100*multiplier)) + "pt Humble Cafe")
        self.title_txt.move(93,25)
        
        self.choose_temp_btn = PicButton(QPixmap('contents/Choose_Temp.png'),self)
        self.choose_temp_btn.move(125,165)
        
        self.make_temp_btn = PicButton(QPixmap('contents/Make_Temp.png'),self)
        self.make_temp_btn.move(125,315)
        
        self.about_btn = PicButton(QPixmap('contents/About.png'),self)
        self.about_btn.move(375,465)

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        
        painter.setBrush(self.color)
        painter.drawPixmap(self.rect(), self.pixmap_pencil)
        
        painter.drawRect(63,20,397,102)

class Choose_Temp(QWidget):
    def __init__(self, parent = None):
        super(Choose_Temp, self).__init__(parent)
        global fileOpen
        self.file = False

        self.title_txt = QLabel(self)
        self.title_txt.setText("Study Buddy")
        self.title_txt.setStyleSheet("font: " + str(int(100*multiplier)) + "pt Humble Cafe")
        self.title_txt.move(145,25)

        self.temp_txt = QLabel(self)
        self.temp_txt.setText("Template to use: ")
        self.temp_txt.setStyleSheet("font: "+ str(int(24*multiplier)) + "pt Montserrat")
        self.temp_txt.move(50,200)

        self.back_btn = PicButton(QPixmap("contents/Back.png"), self)
        self.back_btn.move(25,410)

        self.start_btn = PicButton(QPixmap("contents/Start.png"), self)
        self.start_btn.move(490,410)
        self.start_btn.hide()

        self.combox = QComboBox(self)
        self.combox.addItem("Choose File...")
        self.combox.setGeometry(275,190,300,50)

        if fileOpen:
            self.combox.addItem(fileOpen)

        self.combox.activated.connect(lambda:self.check_combox())

    def check_combox(self):
        global fileOpen
        if self.combox.currentIndex() == 0:
            self.options = QFileDialog.Options()
            self.options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"Open Template", "","Text File (*.txt)", options=self.options)
            if fileName:
                self.combox.clear()
                self.combox.addItems(["...", fileName])
                self.combox.setCurrentIndex(1)
                self.file = True
                fileOpen = fileName
                self.start_btn.show()
        else:
            self.combox.clear()
            self.combox.addItems(["...", fileOpen])
            self.combox.setCurrentIndex(1)
            self.file = True
            self.start_btn.show()

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            
        painter.drawRect(115,20,397,102)
               
class Make_Temp(QWidget):
    def __init__(self, parent = None):
        super(Make_Temp, self).__init__(parent)
        global enabled_0 
        global enabled_1 
        global value_0  
        global value_1 
        global editMode
        global fileOpen

        self.title_txt = QLabel(self)
        self.title_txt.setText("Study Buddy")
        self.title_txt.setStyleSheet("font: " + str(int(100*multiplier)) + "pt Humble Cafe")
        self.title_txt.move(145,25)

        self.edit_txt = QLabel(self)
        self.edit_txt.setText('Edit File: ')
        self.edit_txt.setStyleSheet("font: " + str(int(24*multiplier)) + "pt Montserrat")
        self.edit_txt.move(15,125)

        self.edit_box = QCheckBox(self)
        self.edit_box.move(125,135)
        self.edit_box.setChecked(editMode)

        self.file_txt = QLabel(self)
        self.file_txt.setText('Choose File: ')
        self.file_txt.setStyleSheet("font: " + str(int(24*multiplier)) + "pt Montserrat")
        self.file_txt.move(330,125)

        self.file_combox = QComboBox(self)
        self.file_combox.move(485,130)
        self.file_combox.setFixedSize(135,25)
        self.file_combox.addItem('...')

        if fileOpen:
            self.file_combox.addItem(fileOpen)

        if editMode == True:
            self.file_txt.show()
            self.file_combox.show()
            self.file_combox.setCurrentIndex(1)
        elif editMode == False:
            self.file_txt.hide()
            self.file_combox.hide()
            self.file_combox.setCurrentIndex(0)

        self.Identi_txt = QLabel(self)
        self.Identi_txt.setText("New File:")
        self.Identi_txt.setStyleSheet("font: " + str(int(32*multiplier)) + "pt Montserrat")
        self.Identi_txt.move(15,175)

        self.Check0 = QCheckBox(self)
        self.Check0.move(175,190)
        self.Check0.setChecked(enabled_0)

        self.textbox_0 = QLineEdit(self)
        self.textbox_0.move(400,260)
        self.textbox_0.resize(40,40)
        self.textbox_0.setMaxLength(4)
        self.textbox_0.setText(str(value_0))

        self.enterVal0_txt = QLabel(self)
        self.enterVal0_txt.setText("Enter the number \n of questions: ")
        self.enterVal0_txt.move(180,250)
        self.enterVal0_txt.setStyleSheet("font: " + str(int(21*multiplier)) + "pt Montserrat")

        self.view0_btn = PicButton(QPixmap("contents/View.png"), self)
        self.view0_btn.move(250,500)

        #self.Multi_txt = QLabel(self)
        #self.Multi_txt.setText("Multiple Choice")
        #self.Multi_txt.setStyleSheet("font: " + str(int(32*multiplier)) + "pt Montserrat")
        #self.Multi_txt.move(330,175)

        #self.Check1 = QCheckBox(self)
        #self.Check1.move(600,185)
        #self.Check1.setChecked(enabled_1)
        #self.Check1.hide()

        #self.textbox_1 = QLineEdit(self)
        #self.textbox_1.move(575,250)
        #self.textbox_1.resize(40,40)
        #self.textbox_1.setMaxLength(4)
        #self.textbox_1.setText(str(value_1))

        #self.enterVal1_txt = QLabel(self)
        #self.enterVal1_txt.setText("Enter the number \n of questions: ")
        #self.enterVal1_txt.move(335,250)
        #self.enterVal1_txt.setStyleSheet("font: " + str(int(21*multiplier)) + "pt Montserrat")

        #self.view1_btn = PicButton(QPixmap("contents/View.png"), self)
        #self.view1_btn.move(420,500)

        self.next_btn = PicButton(QPixmap('contents/Next.png'), self)
        self.next_btn.move(480,650)

        self.back_btn = PicButton(QPixmap('contents/Back.png'), self)
        self.back_btn.move(40,650)
        
        self.Check0.stateChanged.connect(lambda:self.state_checked0(self.Check0))
        #self.Check1.stateChanged.connect(lambda:self.state_checked1(self.Check1))

        if enabled_0 == True:
            self.enterVal0_txt.show()
            self.textbox_0.show()
            self.view0_btn.show()
        elif enabled_0 == False:
            self.enterVal0_txt.hide()
            self.textbox_0.hide()
            self.view0_btn.hide()
        
        #if enabled_1 == True:
        #    self.enterVal1_txt.show()
        #    self.textbox_1.show()
        #    self.view1_btn.show()
        #elif enabled_1 == False:
        #    self.enterVal1_txt.hide()
        #    self.textbox_1.hide()
        #    self.view1_btn.hide()

        self.textbox_0.textChanged.connect(lambda:self.changed_0())
        #self.textbox_1.textChanged.connect(lambda:self.changed_1())

        self.edit_box.stateChanged.connect(lambda:self.edit_Mode())
        self.file_combox.activated.connect(lambda:self.file_sel())

    def loop0(self,state):
        if int(self.textbox_0.text()) > 1:
            state()
        elif self.textbox_0.text() == '0':
            dialog = QDialog(self)
            dialog.setFixedSize(110,75)
        
            enval_txt = QLabel(dialog)
            enval_txt.setText('Enter value first!')
            enval_txt.setStyleSheet('font: ' + str(float(14*multiplier)) + 'pt')

            ok_btn = QPushButton(dialog)
            ok_btn.setText('Okay')
            ok_btn.move(20,30)

            ok_btn.clicked.connect(lambda:dialog.close())
        
            dialog.exec_()
        
    def loop1(self,state):
        if int(self.textbox_1.text()) > 1:
            state()
        elif self.textbox_1.text() == '0':
            dialog = QDialog(self)
            dialog.setFixedSize(110,75)
        
            enval_txt = QLabel(dialog)
            enval_txt.setText('Enter value first!')
            enval_txt.setStyleSheet('font: ' + str(float(14*multiplier)) + 'pt')

            ok_btn = QPushButton(dialog)
            ok_btn.setText('Okay')
            ok_btn.move(20,30)

            ok_btn.clicked.connect(lambda:dialog.close())
        
            dialog.exec_()

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            
        #painter.drawLine(320,150,320,600)

        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            
        painter.drawRect(115,20,397,102)

    def state_checked0(self,b):
        global enabled_0
        if b.isChecked() == True:
            self.textbox_0.show()
            self.enterVal0_txt.show()
            self.view0_btn.show()
            enabled_0 = True
        elif b.isChecked() == False:
            self.textbox_0.hide()
            self.enterVal0_txt.hide()
            self.view0_btn.hide()
            enabled_0 = False

    def state_checked1(self,b):
        global enabled_1
        if b.isChecked() == True:
            self.textbox_1.show()
            self.enterVal1_txt.show()
            self.view1_btn.show()
            enabled_1 = True
        elif b.isChecked() == False:
            self.textbox_1.hide()
            self.enterVal1_txt.hide()
            self.view1_btn.hide()
            enabled_0 = False

    def changed_0(self):
        global value_0
        value_0 = self.textbox_0.text()

    def changed_1(self):
        global value_1
        value_1 = self.textbox_1.text()

    def edit_Mode(self):
        global editMode

        checked = self.edit_box.isChecked()
        if checked == True:
            editMode = True
            self.file_txt.show()
            self.file_combox.show()
        elif checked == False:
            editMode = False
            self.file_txt.hide()
            self.file_combox.hide()
            self.textbox_0.setText('0')
            self.Check0.setChecked(False)

    def file_sel(self):
        global fileOpen

        if self.file_combox.currentIndex() == 0:
            self.options = QFileDialog.Options()
            self.options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"Open Template", "","Text File (*.txt)", options=self.options)
            if fileName:
                self.file_combox.clear()
                self.file_combox.addItems(["...", fileName])
                fileOpen = fileName

                with open(fileOpen,'r'):
                    file_content.read(fileOpen)
                    self.identification = bool(file_content.get('CONFIG','identification'))
                    enabled_0 = self.identification
                    self.Check0.setChecked(self.identification)

                    self.identification_numbers = int(file_content.get('CONFIG','identification_numbers'))
                    value_0 = self.identification_numbers
                    self.textbox_0.setText(str(value_0))

                self.file_combox.setCurrentIndex(1)

        elif self.file_combox.currentIndex() == 1:
            with open(fileOpen,'r'):
                file_content.read(fileOpen)
                self.identification = bool(file_content.get('CONFIG','identification'))
                enabled_0 = self.identification
                self.Check0.setChecked(self.identification)

                self.identification_numbers = int(file_content.get('CONFIG','identification_numbers'))
                value_0 = self.identification_numbers
                self.textbox_0.setText(str(value_0))
            
class About_Temp(QWidget):
    def __init__(self, parent = None):
        super(About_Temp, self).__init__(parent)
        self.title_txt = QLabel(self)
        self.title_txt.setText("Study Buddy")
        self.title_txt.setStyleSheet("font: " + str(int(100*multiplier)) + "pt Humble Cafe")
        self.title_txt.move(145,25)

        self.back_btn = PicButton(QPixmap('contents/Back.png'), self)
        self.back_btn.move(40,650)

        self.multi = multiplier
        self.cur_index0 = 0
        
        if multiplier == 0.6:
            self.cur_index0 = 0
        elif multiplier == 1:
            self.cur_index0 = 1

        self.zoom = zoom
        self.cur_index1 = 0

        if zoom == 1:
            self.cur_index1 = 0
        elif zoom == 1.5:
            self.cur_index1 = 1
        elif zoom == 2:
            self.cur_index1 = 2

        self.ver = QLabel(self)
        self.ver.setText("Version 1.0")
        self.ver.setStyleSheet("font: " + str(int(32*multiplier)) + "pt Montserrat")
        self.ver.move(230,120)

        self.desc_0 = QLabel(self)
        self.desc_0.setText("Made by TetheredAround")
        self.desc_0.setStyleSheet("font: " + str(int(26*multiplier)) + "pt Montserrat")
        self.desc_0.move(160,200)

        self.desc_1 = QLabel(self)
        self.desc_1.setText("Aims to help students, like myself;")
        self.desc_1.setStyleSheet("font: " + str(int(26*multiplier)) + "pt Montserrat")
        self.desc_1.move(100,240)

        self.desc_2 = QLabel(self)
        self.desc_2.setText("By answering templates made by")
        self.desc_2.setStyleSheet("font: " + str(int(26*multiplier)) + "pt Montserrat")
        self.desc_2.move(100,280)

        self.desc_3 = QLabel(self)
        self.desc_3.setText("other students for other students.")
        self.desc_3.setStyleSheet("font: " + str(int(26*multiplier)) + "pt Montserrat")
        self.desc_3.move(100,320)

        self.settings_txt = QLabel(self)
        self.settings_txt.setText("SETTINGS")
        self.settings_txt.setStyleSheet("font: " + str(int(42*multiplier)) + "pt Montserrat")
        self.settings_txt.move(370,395)

        self.platform_txt = QLabel(self)
        self.platform_txt.setText("Platform: ")
        self.platform_txt.setStyleSheet("font: " + str(int(21*multiplier)) + "pt Montserrat")
        self.platform_txt.move(325,465)

        self.combox_0 = QComboBox(self)
        self.combox_0.addItems(["Windows/Linux","Macintosh"])
        self.combox_0.move(500,470)
        self.combox_0.setCurrentIndex(self.cur_index0)

        self.zoom_txt = QLabel(self)
        self.zoom_txt.setText("Zoom\n/Resolution: ")
        self.zoom_txt.setStyleSheet("font: " + str(int(21*multiplier)) + "pt Montserrat")
        self.zoom_txt.move(325,505)
        self.zoom_txt.hide()

        self.combox_1 = QComboBox(self)
        self.combox_1.addItems(["1x","1.5x","2x"])
        self.combox_1.move(500,530)
        self.combox_1.setCurrentIndex(self.cur_index1)
        self.combox_1.hide()

        self.save_btn = PicButton(QPixmap("contents/Save.png"),self)
        self.save_btn.move(415,650)

        self.combox_0.currentIndexChanged.connect(lambda:self.sel_changed0(self.combox_0))
        self.combox_1.currentIndexChanged.connect(lambda:self.sel_changed1(self.combox_1))
        self.save_btn.clicked.connect(lambda:self.save_clicked(self.save_btn))
        
    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            
        painter.drawRect(115,20,397,102)

        painter.drawRect(300,400,339,319)

    def sel_changed0(self, c):
        if c.currentIndex() == 0:
            self.multi = 0.6
        elif c.currentIndex() == 1:
            self.multi = 1

    def sel_changed1(self, c):
        if c.currentIndex() == 0:
            self.zoom = 1
        elif c.currentIndex() == 1:
            self.zoom = 1.5
        elif c.currentIndex() == 2:
            self.zoom = 2

    def save_clicked(self, b):
        config['DEFAULT'] = {
            'multiplier' : str(self.multi),
            'zoom' : str(self.zoom)
        }
        
        with open('config.txt', 'w') as configfile:
            config.write(configfile)
            
        dialog = QDialog(self)
        dialog.setFixedSize(350,75)
        
        reset_txt = QLabel(dialog)
        reset_txt.setText('In order to see changes, please reset the application.')
        reset_txt.setStyleSheet('font: ' + str(float(14*multiplier)) + 'pt')

        yes_btn = QPushButton(dialog)
        yes_btn.setText('Reset Now')
        yes_btn.setDefault(True)
        yes_btn.move(220,30)

        no_btn = QPushButton(dialog)
        no_btn.setText('Reset Later')
        no_btn.move(20,30)

        no_btn.clicked.connect(lambda:dialog.close())
        yes_btn.clicked.connect(lambda:(app.quit(), sys.exit()))
        
        dialog.exec_()

class Make_Temp_Identification(QWidget):
    def __init__(self, parent = None):
        super(Make_Temp_Identification, self).__init__(parent)
        global editMode
        global fileOpen

        questions = {}
        answers = {}
        number = {}
        aTxt = {}

        questions_str = {}
        answers_str = {}

        self.back_btn = PicButton(QPixmap('contents/Back.png'), self)
        self.back_btn.move(40,650)

        self.save_btn = PicButton(QPixmap("contents/Save.png"), self)
        self.save_btn.move(480,650)
        
        self.grid = QGridLayout()

        self.groupBox = QGroupBox()

        self.scroll = QScrollArea(self)
        self.scroll.move(30,30)
        self.scroll.setGeometry(50,30,545,590)

        self.qTxt = QLabel()
        self.qTxt.setText("QUESTIONS")
        self.grid.addWidget(self.qTxt,0,1)

        self.aTxt = QLabel()
        self.aTxt.setText("ANSWERS")
        self.grid.addWidget(self.aTxt,0,3)

        if editMode:
            with open(fileOpen,'r'):
                file_content.read(fileOpen)
                identification_numbers = int(file_content.get('CONFIG','identification_numbers'))
                add_sub_Items = int(value_0) - int(identification_numbers)

                for i in range(int(identification_numbers)):
                    questions_str[i] = file_content.get('IDENTIFICATION_Q','question_'+str(i))
                    answers_str[i] = file_content.get('IDENTIFICATION_A','answer_'+str(i))

                for i in range(int(identification_numbers),int(identification_numbers+add_sub_Items)):
                    questions_str[i] = ''
                    answers_str[i] = ''

                for i in range(int(value_0)):

                    questions[i] = QTextEdit()
                    questions[i].setFixedSize(200,75)
                    questions[i].setText(questions_str[i])

                    number[i] = QLabel()
                    number[i].setText(str(i+1)+". ")
                    self.grid.addWidget(number[i],i+1,0)
                    self.grid.addWidget(questions[i],i+1,1)

                    #self.grid.setHorizontalSpacing(15)

                    answers[i] = QTextEdit()
                    answers[i].setFixedSize(200,75)
                    answers[i].setText(answers_str[i])

                    aTxt[i] = QLabel()
                    aTxt[i].setText("Answer: ")
                    self.grid.addWidget(aTxt[i],i+1,2)
                    self.grid.addWidget(answers[i],i+1,3)
        else:
            for i in range(int(value_0)):
                questions[i] = QTextEdit()
                questions[i].setFixedSize(200,75)
                number[i] = QLabel()
                number[i].setText(str(i+1)+". ")
                self.grid.addWidget(number[i],i+1,0)
                self.grid.addWidget(questions[i],i+1,1)

                self.grid.setHorizontalSpacing(15)

                answers[i] = QTextEdit()
                answers[i].setFixedSize(200,75)
                aTxt[i] = QLabel()
                aTxt[i].setText("Answer: ")
                self.grid.addWidget(aTxt[i],i+1,2)
                self.grid.addWidget(answers[i],i+1,3)
        
        self.groupBox.setLayout(self.grid)
        self.scroll.setWidget(self.groupBox)

        self.save_btn.clicked.connect(lambda:self.save(questions,answers))

    def save(self,q,a):
        global editMode

        if editMode:
            #self.write_toFile(q,a)

            dialog = QDialog(self)
            dialog.setFixedSize(100,75)
            
            saved_txt = QLabel(dialog)
            saved_txt.setText('Saved!')
            saved_txt.move(30,0)
            #saved_txt.setStyleSheet('font: ' + str(float(14*multiplier)) + 'pt')

            okay_btn = QPushButton(dialog)
            okay_btn.setText('Okay!')
            okay_btn.setDefault(True)
            okay_btn.move(15,30)

            okay_btn.clicked.connect(lambda:(self.write_toFile(q,a), dialog.close()))
            
            dialog.exec_()
        else:
            dialog = QDialog(self)
            dialog.setFixedSize(300,75)
            
            filename_txt = QLabel(dialog)
            filename_txt.setText('Please name the file: ')
            filename_txt.setStyleSheet('font: ' + str(float(14*multiplier)) + 'pt')

            self.filebox = QLineEdit(dialog)
            self.filebox.setText("NewFile")
            self.filebox.move(150,0)

            done_btn = QPushButton(dialog)
            done_btn.setText('Done!')
            done_btn.setDefault(True)
            done_btn.move(100,30)

            done_btn.clicked.connect(lambda:(self.write_toFile(q,a), dialog.close()))
            
            dialog.exec_()

    def write_toFile(self,q,a):
        global file_content

        for i in range(int(value_0)):
            self.add_dictQ('Question_'+str(int(i)),q[i].toPlainText())
            self.add_dictA('Answer_'+str(int(i)),a[i].toPlainText())

        self.config_I()

        if editMode:
            with open(fileOpen, 'w+') as file:
                file_content.write(file)
        else:
            with open(str(self.filebox.text())+".txt", 'w+') as file:
                file_content.write(file)

    def add_dictQ(self,key,value):
        file_content["IDENTIFICATION_Q"][key] = value

    def add_dictA(self,key,value):
        file_content["IDENTIFICATION_A"][key] = value
    
    def config_I(self):
        global file_content
        file_content["CONFIG"]['identification'] = 'True'
        file_content["CONFIG"]['identification_numbers'] = str(int(value_0))

#class Make_Temp_Multiplechoice(QWidget):

class  View_Start_Temp(QWidget):
    def __init__(self, parent = None):
        super(View_Start_Temp, self).__init__(parent)
        global ovrall_score
        self.scored_qa = 0

        self.questions = {}
        self.questions_str = {}
        self.answers = {}
        self.answers_str = {}
        self.number = {}
        self.aTxt = {}

        with open(fileOpen,'r'):
            file_content.read(fileOpen)
            self.identification = bool(file_content.get('CONFIG','identification'))
            if self.identification:
                self.identification_numbers = int(file_content.get('CONFIG','identification_numbers'))

                for i in range(int(self.identification_numbers)):
                    self.questions_str[i] = file_content.get('IDENTIFICATION_Q','question_'+str(i))
                    self.answers_str[i] = file_content.get('IDENTIFICATION_A','answer_'+str(i))

        ovrall_score = self.identification_numbers

        self.back_btn = PicButton(QPixmap('contents/Back.png'), self)
        self.back_btn.move(40,650)

        self.check_btn = PicButton(QPixmap('contents/Check.png'), self)
        self.check_btn.move(480,650)

        self.grid = QGridLayout()

        self.groupBox = QGroupBox()

        self.scroll = QScrollArea(self)
        self.scroll.move(30,30)
        self.scroll.setGeometry(50,30,545,590)

        self.qTxt = QLabel()
        self.qTxt.setText("QUESTIONS")
        self.grid.addWidget(self.qTxt,0,1)

        self.a_Txt = QLabel()
        self.a_Txt.setText("ANSWERS")
        self.grid.addWidget(self.a_Txt,0,3)

        for i in range(int(self.identification_numbers)):
            self.questions[i] = QLabel()
            self.questions[i].setText(str(self.questions_str[i]))
            self.questions[i].setWordWrap(True)
            self.questions[i].setFixedSize(200,75)

            self.number[i] = QLabel()
            self.number[i].setText(str(i+1)+". ")

            self.grid.addWidget(self.number[i],i+1,0)
            self.grid.addWidget(self.questions[i],i+1,1)

            self.grid.setHorizontalSpacing(20)

            self.answers[i] = QTextEdit()
            self.answers[i].setFixedSize(200,50)
            self.aTxt[i] = QLabel()
            self.aTxt[i].setText("A: ")
            
            self.grid.addWidget(self.aTxt[i],i+1,2)
            self.grid.addWidget(self.answers[i],i+1,3)
        
        self.groupBox.setLayout(self.grid)
        self.scroll.setWidget(self.groupBox)

    def checking(self,s):
        global prev_score
        checking_bool = True
        ans = 0 

        for i in range(int(self.identification_numbers)):
            if self.answers[i].toPlainText() == '':
                pass
            elif self.answers[i].toPlainText() == self.answers[i].toPlainText():
                ans = ans + 1
            
        if ans >= int(self.identification_numbers*0.5):
            for i in range(int(self.identification_numbers)):
                if self.answers[i].toPlainText().lower() == self.answers_str[i].lower():
                    self.scored_qa = self.scored_qa + 1

        elif ans < int(self.identification_numbers*0.5):
            dialog = QDialog(self)
            dialog.setFixedSize(200,75)
                
            ans_txt = QLabel(dialog)
            ans_txt.setText('Please answer more questions.')
            ans_txt.setStyleSheet('font: ' + str(float(14*multiplier)) + 'pt')

            ok_btn = QPushButton(dialog)
            ok_btn.setText('Okay!')
            ok_btn.setDefault(True)
            ok_btn.move(65,30)

            ok_btn.clicked.connect(lambda:dialog.close())
                
            dialog.exec_()

        prev_score = self.scored_qa
        s()

class View_Score_Temp(QWidget):
    def __init__(self, parent = None):
        super(View_Score_Temp, self).__init__(parent)
        global prev_score
        global ovrall_score

        self.title_txt = QLabel(self)
        self.title_txt.setText("Study Buddy")
        self.title_txt.setStyleSheet("font: " + str(int(100*multiplier)) + "pt Humble Cafe")
        self.title_txt.move(93,25)

        self.passed = QPixmap('contents/Passed.png')
        self.failed = QPixmap('contents/Failed.png')
        self.text = 'None'

        self.image = QLabel(self)

        if prev_score >= int(ovrall_score*0.75):
            self.image.setPixmap(self.passed)
            self.text = 'PASSED'
        elif prev_score < int(ovrall_score/0.75):
            self.image.setPixmap(self.failed)
            self.text = 'FAILED'
        
        self.image.move(140,190)

        self.back_btn = PicButton(QPixmap('contents/Back.png'), self)
        self.back_btn.move(40,450)

        self.result_txt = QLabel(self)
        self.result_txt.setText("Results:")
        self.result_txt.setStyleSheet("font: " + str(int(32*multiplier)) + "pt Montserrat")
        self.result_txt.move(335,190)

        self.score = QLabel(self)
        self.score.setStyleSheet("font: " + str(int(32*multiplier)) + "pt Montserrat")
        self.score.setText(str(prev_score) + '/' + str(ovrall_score))
        self.score.move(335,240)

        self.grading = QLabel(self)
        self.grading.setStyleSheet("font: " + str(int(32*multiplier)) + "pt Montserrat")
        self.grading.setText(self.text)
        self.grading.move(335,300)

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))

        painter.drawRect(63,20,397,102)

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.title = 'Study Buddy'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.setWindowTitle(self.title)
        self.color = QColor(238,238,238)

        self.setWindowIcon(QIcon('contents/Pencil.png'))

        self.center()

        self.start_MainMenu_GUI()
        
        #self.start_Make_Temp_GUI()
        #self.start_About_Temp_GUI()
        #self.start_View_Score_Temp_GUI()

        #Custom font
        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont("contents/Humble Cafe.ttf")
        families = font_db.applicationFontFamilies(font_id)
        custom_Font = QFont("Humble Cafe")
        #QFontDatabase.addApplicationFont("contents/Humble Cafe.ttf")
        
        font_db_1 = QFontDatabase()
        font_id_1 = font_db_1.addApplicationFont("contents/Montserrat-Medium.otf.otf")
        families_1 = font_db_1.applicationFontFamilies(font_id_1)
        custom_Font_1 = QFont("families_1")
        #QFontDatabase.addApplicationFont("contents/Montserrat_Meduim.otf")

    def start_MainMenu_GUI(self):
        MM = Main_Menu
        self.Main_Menu = Main_Menu(self)
        self.Main_Menu.color = self.color
        self.setCentralWidget(self.Main_Menu)

        self.resize(self.Main_Menu.pixmap_pencil.width(), self.Main_Menu.pixmap_pencil.height())
        self.setFixedSize(self.Main_Menu.pixmap_pencil.width(), self.Main_Menu.pixmap_pencil.height())

        self.center()

        self.Main_Menu.choose_temp_btn.clicked.connect(self.start_Choose_Temp_GUI)
        self.Main_Menu.make_temp_btn.clicked.connect(self.start_Make_Temp_GUI)
        self.Main_Menu.about_btn.clicked.connect(self.start_About_Temp_GUI)
        
        self.show()

    def start_Choose_Temp_GUI(self):
        CT = Choose_Temp
        self.Choose_Temp = CT(self)
        self.setCentralWidget(self.Choose_Temp)
        
        self.resize(640,480)
        self.setFixedSize(640,480)
        self.center()

        self.Choose_Temp.back_btn.clicked.connect(self.start_MainMenu_GUI)

        self.Choose_Temp.start_btn.clicked.connect(self.start_View_Start_Temp_GUI)

        self.show()

    def start_Make_Temp_GUI(self):
        MT = Make_Temp
        loop = True
        self.Make_Temp = MT(self)
        self.setCentralWidget(self.Make_Temp)

        self.resize(640,480)
        self.setFixedSize(640,720)
        self.center()

        self.Make_Temp.back_btn.clicked.connect(self.start_MainMenu_GUI)

        self.Make_Temp.view0_btn.clicked.connect(lambda:self.Make_Temp.loop0(self.start_Make_Temp_Identi_GUI))
        #self.Make_Temp.view1_btn.clicked.connect(lambda:self.Make_Temp.loop1(self.start_Make_Temp_Identi_GUI))

        self.show()

    def start_About_Temp_GUI(self):
        AT = About_Temp
        self.About_Temp = About_Temp(self)
        self.setCentralWidget(self.About_Temp)

        self.resize(640,480)
        self.setFixedSize(640,720)
        self.center()

        self.About_Temp.back_btn.clicked.connect(self.start_MainMenu_GUI)

        self.show()
    
    def start_Make_Temp_Identi_GUI(self):
        MTI = Make_Temp_Identification
        self.Make_Temp_Identification = MTI(self)
        self.setCentralWidget(self.Make_Temp_Identification)

        self.resize(640,480)
        self.setFixedSize(640,720)
        self.center()

        self.Make_Temp_Identification.back_btn.clicked.connect(self.start_Make_Temp_GUI)

        self.show()

    def start_View_Start_Temp_GUI(self):
        VST = View_Start_Temp
        self.View_Start_Temp = VST(self)
        self.setCentralWidget(self.View_Start_Temp)

        self.resize(640,480)
        self.setFixedSize(640,720)
        self.center()

        self.show()

        self.View_Start_Temp.back_btn.clicked.connect(self.start_Choose_Temp_GUI)

        self.View_Start_Temp.check_btn.clicked.connect(lambda:self.View_Start_Temp.checking(self.start_View_Score_Temp_GUI))

    def start_View_Score_Temp_GUI(self):
        VScT = View_Score_Temp
        self.View_Score_Temp = VScT(self)
        self.setCentralWidget(self.View_Score_Temp)

        self.resize(523,526)
        self.setFixedSize(523,526)
        self.center()

        self.show()

        self.View_Score_Temp.back_btn.clicked.connect(self.start_MainMenu_GUI)
        
    def center(self):
        self.screen_reso = QDesktopWidget().screenGeometry()

        self.setGeometry(int((self.screen_reso.width()/2) - (self.frameSize().width()/2)),
        int((self.screen_reso.height()/2) - (self.frameSize().height()/2)),
        self.width,
        self.height)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.setStyleSheet('Breeze')

    dpi = QApplication.primaryScreen().logicalDotsPerInch()

    adjusted_height = (QDesktopWidget().screenGeometry().height()/(dpi/96))

    scale = float(((adjusted_height* 0.75)/1440))

    try:
        config.read('config.txt')
    except FileNotFoundError:
        print(f"Error: {e}")

    if config.get('DEFAULT', 'configured') == '0':
        config['DEFAULT']['configured'] = '1'
        config['DEFAULT']['multiplier'] = str(scale)
        with open('config.txt', 'w') as configfile:
            config.write(configfile)
        try:
            subprocess.run([sys.executable, "PyQt_SB.py"], shell=True)
        except Exception as e:
            print(f"Error: {e}")
        QCoreApplication.quit()
    else:
        ex = MainWindow()
        sys.exit(app.exec_())
