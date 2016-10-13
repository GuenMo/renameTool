# coding:utf-8

from PySide import QtGui, QtCore

import control.namesControl as namesControl
reload(namesControl)

class RenameUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(RenameUI, self).__init__(parent)
        
        # Window
        self.setWindowTitle('Rename Tool')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedWidth(320) 
        self.setFixedHeight(280)
        
        # Layout
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setContentsMargins(5,5,5,5)
        mainLayout.setSpacing(0)
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        
        renameWidget  = RenameWidget(self)
        replaceWidget = ReplaceWidget(self) 
        
        mainLayout.addWidget(renameWidget)
        mainLayout.addWidget(replaceWidget)
        
        self.setLayout(mainLayout)

class RenameWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(RenameWidget, self).__init__(parent)
        mainLayout = QtGui.QVBoxLayout() 
        mainLayout.setContentsMargins(5,5,5,5)
        mainLayout.setSpacing(2)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.setLayout(mainLayout)
        
        renameSplitter = Splitter('RENAME')
        splitter1 = Splitter(shadow=False, color=(60,60,60))
        splitter2 = Splitter(shadow=False, color=(60,60,60))
        splitter3 = Splitter(shadow=False, color=(60,60,60))
        
        # nameLayout
        nameLayout = QtGui.QHBoxLayout()
        nameLayout.setContentsMargins(4,0,4,0)
        nameLayout.setSpacing(2)
        
        nameLabel = QtGui.QLabel('New Name:')
        nameLabel.setFixedWidth(55)
        self.nameLine  = QtGui.QLineEdit()
        regEx     = QtCore.QRegExp('^(?!^_)[a-zA-Z_]+')
        #regEx     = QtCore.QRegExp('^[a-zA-Z][a-zA-Z_]+')
        nameValidator = QtGui.QRegExpValidator(regEx, self.nameLine)
        self.nameLine.setValidator(nameValidator)
        
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameLine)
        
        # multLayout
        multLayout = QtGui.QHBoxLayout()
        multLayout.setContentsMargins(4,0,4,0)
        multLayout.setSpacing(2)
        
        multLabel = QtGui.QLabel('Multiples Naming Method:')
        self.multCombo = QtGui.QComboBox()
        self.multCombo.addItem('Numbers (0-9)')
        self.multCombo.addItem('Letters (a-z)')
        self.multCombo.setFixedWidth(110)
        
        multLayout.addWidget(multLabel)
        multLayout.addWidget(self.multCombo)
        
        # multOptionLayout
        multOptionLayout = QtGui.QHBoxLayout()
        multOptionLayout.setContentsMargins(4,0,4,0)
        multOptionLayout.setSpacing(2)
        
        self.paddingLabel = QtGui.QLabel('No. Padding:')
        self.paddingSpin  = QtGui.QSpinBox()
        self.paddingSpin.setFixedWidth(40)
        self.paddingSpin.setMinimum(0)
        self.paddingSpin.setMaximum(10)
        
        self.lowerRadio = QtGui.QRadioButton('Lowercase')
        self.lowerRadio.setVisible(False)
        self.lowerRadio.setFixedHeight(23)
        self.lowerRadio.setChecked(True)
        self.upperRadio = QtGui.QRadioButton('Uppercase')
        self.upperRadio.setVisible(False)
        self.upperRadio.setFixedHeight(23)
        
        multOptionLayout.addWidget(self.paddingLabel)
        multOptionLayout.addWidget(self.paddingSpin)
        #multOptionLayout.addSpacerItem(QtGui.QSpacerItem(5,5,QtGui.QSizePolicy.Expanding))
        multOptionLayout.addWidget(self.lowerRadio)
        multOptionLayout.addWidget(self.upperRadio)
        
        # multOptionLayout
        fixLayout = QtGui.QHBoxLayout()
        fixLayout.setContentsMargins(4,0,4,0)
        fixLayout.setSpacing(2)
         
        self.prefixCheck = QtGui.QCheckBox('Prefix:')
        self.prefixLine  = QtGui.QLineEdit()
        self.prefixLine.setEnabled(False)
        self.prefixLine.setFixedWidth(85)
        prefixValidator = QtGui.QRegExpValidator(regEx, self.prefixLine)
        self.prefixLine.setValidator(prefixValidator)
    
        self.suffixCheck = QtGui.QCheckBox('Suffix:')
        self.suffixLine  = QtGui.QLineEdit()
        self.suffixLine.setEnabled(False)
        self.suffixLine.setFixedWidth(85)
        suffixRegEx    = QtCore.QRegExp('[0-9a-zA-Z_]+^(?!^_)')
        suffiValidator = QtGui.QRegExpValidator(suffixRegEx, self.suffixLine)
        self.suffixLine.setValidator(suffiValidator)
        
        fixLayout.addWidget(self.prefixCheck)
        fixLayout.addWidget(self.prefixLine)
        fixLayout.addSpacerItem(QtGui.QSpacerItem(5,5,QtGui.QSizePolicy.Expanding))
        fixLayout.addWidget(self.suffixCheck)
        fixLayout.addWidget(self.suffixLine)
        
        # bttnLayout
        bttnLayout = QtGui.QHBoxLayout()
        bttnLayout.setContentsMargins(4,0,4,0)
        bttnLayout.setSpacing(2)
        
        self.previewLabel = QtGui.QLabel('e.g.')
        self.renameBttn  = QtGui.QPushButton('Rename')
        self.renameBttn.setFixedSize(55, 20)
        
        bttnLayout.addWidget(self.previewLabel)
        bttnLayout.addWidget(self.renameBttn)

        mainLayout.addWidget(renameSplitter)
        mainLayout.addLayout(nameLayout)
        mainLayout.addWidget(splitter1)
        mainLayout.addLayout(multLayout)
        mainLayout.addLayout(multOptionLayout)
        mainLayout.addWidget(splitter2)
        mainLayout.addLayout(fixLayout)
        mainLayout.addWidget(splitter3)
        mainLayout.addLayout(bttnLayout)
        
        # Connections
        self.prefixCheck.stateChanged.connect(self.prefixLine.setEnabled)
        self.suffixCheck.stateChanged.connect(self.suffixLine.setEnabled)
        self.prefixCheck.stateChanged.connect(self._updatePreviewRename)
        self.suffixCheck.stateChanged.connect(self._updatePreviewRename)
        
        self.multCombo.currentIndexChanged.connect(self._toggleMultNameMethod)
        
        self.multCombo.currentIndexChanged.connect(self._updatePreviewRename)
        self.lowerRadio.clicked.connect(self._updatePreviewRename)
        self.upperRadio.clicked.connect(self._updatePreviewRename)
        self.paddingSpin.valueChanged.connect(self._updatePreviewRename)
        self.nameLine.textChanged.connect(self._updatePreviewRename)
        self.prefixLine.textChanged.connect(self._updatePreviewRename)
        self.suffixLine.textChanged.connect(self._updatePreviewRename)
        
        self.renameBttn.clicked.connect(self.rename)
        
        self._updatePreviewRename()
        
    def _toggleMultNameMethod(self, index):
        self.lowerRadio.setVisible(index)
        self.upperRadio.setVisible(index)
        self.paddingLabel.setVisible(not(index))
        self.paddingSpin.setVisible(not(index))
    
    def _getRenameSetting(self):
        text = self.nameLine.text()
        
        namingMethod = bool(self.multCombo.currentIndex())
        
        padding = 0
        upper   = True
        if namingMethod == 0:
            padding = self.paddingSpin.value()
        else:
            upper = self.upperRadio.isChecked()
            
        prefix = ''
        suffix = ''
        if self.prefixCheck.isChecked():
            prefix = self.prefixLine.text().strip()
        if self.suffixCheck.isChecked():
            suffix = self.suffixLine.text().strip()
            
        return [text, prefix, suffix, padding, namingMethod, upper]
    
    def _updatePreviewRename(self):
        previewText = ''
        
        text, prefix, suffix, padding, namingMethod, upper = self._getRenameSetting()
        
        if not text:
            self.previewLabel.setText('<font color=#646464>e.g.</font>')
            return
        
        if prefix: previewText += '{}'.format(prefix)
        previewText += '{}'.format(text)
        
        if namingMethod:
            if upper: previewText += 'A'
            else:     previewText += 'a'
        else:
            previewText += '{}'.format(padding * '0') + '1'
            
        if suffix: previewText += '{}'.format(suffix)
        
        self.previewLabel.setText('<font color=#646464>e.g. "{}"</font>'.format(previewText))
    
    def rename(self):   
        namesControl.rename(*self._getRenameSetting())
        
class ReplaceWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ReplaceWidget, self).__init__(parent)
        mainLayout = QtGui.QVBoxLayout() 
        mainLayout.setContentsMargins(5,5,5,5)
        mainLayout.setSpacing(2)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.setLayout(mainLayout)
        
        replaceSplitter = Splitter('FIND/REPLACE')
        splitter1 = Splitter(shadow=False, color=(60,60,60))
        splitter2 = Splitter(shadow=False, color=(60,60,60))
        
        # findLayout
        findLayout = QtGui.QHBoxLayout()
        findLayout.setContentsMargins(4,0,4,0)
        findLayout.setSpacing(2)
        
        findLabel = QtGui.QLabel('Find:')
        findLabel.setFixedWidth(55)
        self.findLine  = QtGui.QLineEdit()
        
        findLayout.addWidget(findLabel)
        findLayout.addWidget(self.findLine)
        
        # replaceLayout
        replaceLayout = QtGui.QHBoxLayout()
        replaceLayout.setContentsMargins(4,0,4,0)
        replaceLayout.setSpacing(2)
        
        replaceLabel = QtGui.QLabel('Replace:')
        replaceLabel.setFixedWidth(55)
        self.replaceLine  = QtGui.QLineEdit()
        
        replaceLayout.addWidget(replaceLabel)
        replaceLayout.addWidget(self.replaceLine)
        
        # selectionLayout
        selectionLayout = QtGui.QHBoxLayout()
        selectionLayout.setContentsMargins(4,0,4,0)
        selectionLayout.setSpacing(2)
        
        selectionLabel = QtGui.QLabel('Selection Mode:')
        self.allRadio       = QtGui.QRadioButton('All')
        self.allRadio.setFixedHeight(19)
        self.allRadio.setChecked(True)
        self.selectdRadio   = QtGui.QRadioButton('Selected')
        self.selectdRadio.setFixedHeight(19)
        
        selectionLayout.addWidget(selectionLabel)
        selectionLayout.addSpacerItem(QtGui.QSpacerItem(5,5,QtGui.QSizePolicy.Expanding))
        selectionLayout.addWidget(self.allRadio)
        selectionLayout.addWidget(self.selectdRadio)
        
        # replaceBttnLayout
        replaceBttnLayout = QtGui.QHBoxLayout()
        replaceBttnLayout.setContentsMargins(4,0,4,0)
        replaceBttnLayout.setSpacing(2)
        
        replaceBttn = QtGui.QPushButton('Repalce')
        replaceBttn.setFixedSize(55, 20)
        
        replaceBttnLayout.addSpacerItem(QtGui.QSpacerItem(5,5,QtGui.QSizePolicy.Expanding))
        replaceBttnLayout.addWidget(replaceBttn)
        
        mainLayout.addWidget(replaceSplitter)
        mainLayout.addLayout(findLayout)
        mainLayout.addLayout(replaceLayout)
        mainLayout.addWidget(splitter1)
        mainLayout.addLayout(selectionLayout)
        mainLayout.addWidget(splitter2)
        mainLayout.addLayout(replaceBttnLayout)
        
        # Connection
        replaceBttn.clicked.connect(self.replace)
        
    def replace(self):
        findStr     = self.findLine.text().strip()
        replaceStr = self.replaceLine.text().strip()
        flag = 'selected'
        
        if self.allRadio.isChecked():
            flag = 'all'
        namesControl.findReplace(findStr, replaceStr, flag)
        
class Splitter(QtGui.QWidget):
    def __init__(self, text=None, shadow=True, color=(150,150,150), parent=None):
        super(Splitter, self).__init__(parent)
        
        self.setMinimumHeight(2)
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(0)
        mainLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.setLayout(mainLayout)
        
        # firstLine
        firstLine = QtGui.QFrame()
        firstLine.setFrameStyle(QtGui.QFrame.HLine)
        
        # Line Style     
        mainColor     = 'rgba({},{},{},255)'.format(color[0],color[1],color[2])
        shadowColor   = 'rgba(45,45,45,255)'
        border_bottom = ''
        
        if shadow:
            border_bottom = 'border-bottom:1px solid {}'.format(shadowColor)
        
        styleSheet = 'border:0px solid rgba(0,0,0,0); \
                      background-color: {}; \
                      max-height:1px; \
                      {} rgba(45,45,45,255);'.format(mainColor, border_bottom)
        
        mainLayout.addWidget(firstLine)
        firstLine.setStyleSheet(styleSheet)
        
        # label
        if text is None:
            return 
        firstLine.setMaximumWidth(5)
        
        font     = QtGui.QFont()
        font.setBold(True)
        textWith = QtGui.QFontMetrics(font)
        width    = textWith.width(text) + 6
        label    = QtGui.QLabel(text)
        label.setFont(font)
        label.setMaximumWidth(width)
        label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        # secondLine
        secondLine = QtGui.QFrame()
        secondLine.setFrameStyle(QtGui.QFrame.HLine)
        
        # mainLayout
       
        mainLayout.addWidget(label)
        mainLayout.addWidget(secondLine)

        secondLine.setStyleSheet(styleSheet)

def main():
    global win
    try:
        win.close()
        win.deleteLater()
    except: 
        pass
    win = RenameUI()
    win.show()

