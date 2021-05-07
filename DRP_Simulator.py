
#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################
import sys
import os
import math
import random
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QMessageBox)


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        #styleComboBox = QComboBox()
        #styleComboBox.addItems(QStyleFactory.keys())

        self.show_mat = False

        styleLabel = QLabel('''Heat Transfer Simulation
        ''')
        help_btn = QPushButton('?')
        help_btn.clicked.connect(self.dialog)
        #styleLabel.setBuddy(styleComboBox)

        #self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        #self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Show matrix")

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        #self.createBottomLeftTabWidget()
        #self.createBottomRightGroupBox()
        #self.createProgressBar()

        #styleComboBox.activated[str].connect(self.changeStyle)
        #self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(self.matrixToggle)
        #disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        #disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(help_btn)
        #topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        #topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        #mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        #mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        #mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Heat Transfer Simulator")
        self.resize(600, 400)
        #self.changeStyle('Macintosh')
    def matrixToggle(self):
        self.show_mat = True
        return

    def dialog(self):
        mbox = QMessageBox()
        print('hi')
        #mbox.setIcon(Information)

        mbox.setText("About this program")
        mbox.setInformativeText('''

    DRP SP2021
        @author: Robert Steve
        @mentor: Joe Jackson

    Description:
    Creates a N x N matrix A, with heat supplied at the top right
    defined by the user input heat factor H, s.t.:
            heat = H**2 - i*H, 
            so as i (the distance from the top right corner)
            increases the heat value approaches 0 (where H ~ N)
            h(A[N - i][0]) = H**2 - i*H,
            ...
            h(A[N - N][0]) = 1.

    Randomly walks t number of times from some user-given point (a, b) 
    where (0, 0) is the top left corner. The average of these points is
    equal to the heat value at point (a, b), given a sufficiently large t.

    ''')

        #mbox.setDetailedText(''' ''')
                
        mbox.exec_()

    def matDialog(self, table):
        d = QDialog()
        d.layout = QVBoxLayout()
        d.label = QLabel('\n'.join(table))
        d.layout.addWidget(d.label)
        d.setLayout(d.layout)
        d.setWindowTitle("Generated Matrix")
        d.exec_()
        #mbox = QMessageBox()
        #mbox.setIcon(Information)

        #mbox.setText("Resulting Matrix")
        #mbox.setInformativeText('\n'.join(table))

        #mbox.setDetailedText(''' ''')
                
        #mbox.exec_()

    def pointDialog(self, string):
        mbox = QMessageBox()
        #mbox.setIcon(Information)

        mbox.setText("Results")
        mbox.setInformativeText(string)

        #mbox.setDetailedText(''' ''')
                
        mbox.exec_()

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        #self.changePalette()


    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Make a model selection:")

        radioButton1 = QRadioButton("Heat Tranfer")
        radioButton2 = QRadioButton("Escape Probability")
        #radioButton3 = QRadioButton("Radio button 3")
        radioButton1.setChecked(True)

        #checkBox = QCheckBox("Tri-state check box")
        #checkBox.setTristate(True)
        #checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        #layout.addWidget(radioButton3)
        #layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)    

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Set Values")

        self.N = QLineEdit()
        self.N.setPlaceholderText('N (defines an NxN matrix)')
        self.H = QLineEdit()
        self.H.setPlaceholderText('Heat factor')
        self.a = QLineEdit()
        self.a.setPlaceholderText('Coordinate of interest (a, b)')
        self.b = QLineEdit()
        self.b.setPlaceholderText('Coordinate of interest (a, b)')
        self.T = QLineEdit()
        self.T.setPlaceholderText('Number of trials')

        spacing = QLabel(" ")


        
        defaultPushButton = QPushButton("Run")
        #defaultPushButton.setDefault(True)
               
        defaultPushButton.clicked.connect(lambda: self.mainSim())


        layout = QVBoxLayout()
        layout.addWidget(self.N)
        layout.addWidget(self.H)
        layout.addWidget(self.a)
        layout.addWidget(self.b)
        layout.addWidget(self.T)
        layout.addWidget(spacing)

        layout.addWidget(defaultPushButton)

        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)


    def mainSim(self):
        if self.N.text() == '' or self.H.text() == '' or self.a.text() == '' or self.b.text() == '' or self.T.text() == '':
            print('failed')
            return
        print('MAIN SIM!')
        N = int(self.N.text())
        H = int(self.H.text())
        a = int(self.a.text()) - 1
        b = int(self.b.text()) - 1
        T = int(self.T.text())

        A = []

        a_old = a
        b_old = b

        for _ in range(N):
            A.append(np.zeros((N,), dtype=int).tolist())

        for i in range(N):
            heat = H**2 - i*H
            if heat < .1:
                A[-(i+1)][0] = 0
            else:
                A[-(i+1)][0] = heat

    
        for i in range(1, N):
            heat = H**2 - i*H
            if heat < .1:
                A[N-1][i] = 0
            else:
                A[N-1][i] = heat


        A[a-1][b] = '%'


        A = np.asmatrix(A)

        A = np.rot90(np.fliplr(A))

        A = A.tolist()

         
        s = [[str(e) for e in row] for row in A]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        ###################
        ###DIALOG BOX FOR A

        if self.show_mat == True:
            self.matDialog(table)

        A[b][a - 1] = 0
        

        a_orig = b
        b_orig = a-1

        a = a_orig
        b = b_orig

        res = []
        for _ in range(T):
            while a != N - 1 and b != N - 1 and a != 0 and b != 0:
                val = random.randint(1, 4)
                ## Up
                if val == 1:
                    a += 1
                ## Right
                elif val == 2:
                    b += 1
                ## Down
                elif val == 3:
                    a -= 1
                ## Left
                else:
                    b -= 1
            res.append(float(A[a][b]))
            a = a_orig
            b = b_orig

        heat = round((sum(res) / len(res)), 4)

        string = "In t ({}) of trials, the point ({}, {}) has a heat value of {}.".format(T, a_old, b_old, heat)
        self.pointDialog(string)


        B = A
        res = []

        for i in range(1, N-1):
            for j in range(1, N-1):
                col_orig = i
                cell_orig = j
                for _ in range(T):
                    while i != N - 1 and j != N - 1 and i != 0 and j != 0:
                        val = random.randint(1, 4)
                        ## Up
                        if val == 1:
                            i += 1
                        ## Right
                        elif val == 2:
                            j += 1
                        ## Down
                        elif val == 3:
                            i -= 1
                        ## Left
                        else:
                            j -= 1
                    res.append(float(B[i][j]))
                    i = col_orig
                    j = cell_orig

                B[i][j] = round((sum(res) / len(res)), 4)
                res = []

        df = pd.DataFrame(B).astype(float)
        sns.heatmap(df)
        plt.show()

        return

    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n" 
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Group 3")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)

        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.Password)

        spinBox = QSpinBox(self.bottomRightGroupBox)
        spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Horizontal, self.bottomRightGroupBox)
        slider.setValue(40)

        scrollBar = QScrollBar(Qt.Horizontal, self.bottomRightGroupBox)
        scrollBar.setValue(60)

        dial = QDial(self.bottomRightGroupBox)
        dial.setValue(30)
        dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        layout.addWidget(spinBox, 1, 0, 1, 2)
        layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        layout.addWidget(scrollBar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_()) 
