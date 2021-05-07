
#############################################################################
##
## Heat Transfer Simulation Using Markov Chain Monte Carlo. 
## 
## Rob Steve
## Special thanks to Joe Jackson
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

        self.show_mat = False

        styleLabel = QLabel('''Heat Transfer Simulation
        ''')
        help_btn = QPushButton('?')
        help_btn.clicked.connect(self.dialog)

        disableWidgetsCheckBox = QCheckBox("&Show matrix")

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        disableWidgetsCheckBox.toggled.connect(self.matrixToggle)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(help_btn)
        topLayout.addStretch(1)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Heat Transfer Simulator")
        self.resize(600, 400)
    def matrixToggle(self):
        self.show_mat = True
        return

    def dialog(self):
        mbox = QMessageBox()

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
                
        mbox.exec_()

    def matDialog(self, table):
        d = QDialog()
        d.layout = QVBoxLayout()
        d.label = QLabel('\n'.join(table))
        d.layout.addWidget(d.label)
        d.setLayout(d.layout)
        d.setWindowTitle("Generated Matrix")
        d.exec_()

    def pointDialog(self, string):
        mbox = QMessageBox()

        mbox.setText("Results")
        mbox.setInformativeText(string)
                
        mbox.exec_()

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Make a model selection:")

        radioButton1 = QRadioButton("Heat Tranfer")
        radioButton2 = QRadioButton("Escape Probability")
        radioButton1.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
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


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_()) 
