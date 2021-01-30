import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.QtCore import QFile, QTextStream
import pyperclip
import passwordgen
import filesave
import Algorithm
import webbrowser
import os.path
from os import path
from cryptography.fernet import Fernet
import BreezeStyleSheets.breeze_resources as breeze



class FileSave(QDialog):
	def __init__(self):
		super(FileSave, self).__init__()
		self.ui = filesave.Ui_Dialog()
		self.ui.setupUi(self)
		self.ui.saveButton.clicked.connect(self.save)
		if not path.exists('mykey.key'):
			self.key = Fernet.generate_key()
			try:
				with open ('mykey.key', 'xb') as mykey:
					mykey.write(self.key)
			except FileExistsError:
				None
		else:
			with open ('mykey.key', 'rb') as self.mykey:
				self.key=self.mykey.read()
        
		self.f = Fernet(self.key)
		self.passman = ''
		self.text=''

	def save(self):
		
		self.accounttype = self.ui.accounttypeLine.text()
		self.webURL = self.ui.websiteURLLine.text()
		self.username = self.ui.usernameLine.text()
		self.password = self.ui.passwordLine.text()
		if path.exists("passman.txt"):
			self.accounts = open("passman.txt",'rb')
			zz = self.accounts.read()
			if zz != b'':
				yy = self.f.decrypt(zz)
				self.text = yy.decode()
		self.text = self.text + "\ntype=" + self.accounttype + "\nwebURL=" + self.webURL + "\nusername=" + self.username + "\npassword=" + self.password
		self.passman = self.f.encrypt(self.text.encode())
		try:
			with open ('passman.txt', 'wb') as myfile:
				myfile.write(self.passman)
		except FileExistsError:
			print('no file')
		self.close()

class MyApp(QDialog):
	def __init__(self):
		super(MyApp, self).__init__()
		self.password = ""
		self.ui = passwordgen.Ui_Dialog()
		self.ui.setupUi(self)
		self.ui.generateButton.clicked.connect(self.generate)
		self.ui.copyButton.clicked.connect(self.copy)
		self.ui.filesaveButton.clicked.connect(self.filesave)
		self.FileSave = FileSave()
		self.FileSave.ui.saveButton.clicked.connect(self.dialogclose)
		self.ui.tabWidget.setCurrentIndex(0)
		self.ui.comboBox.addItem("Select Type of Account")
		self.ui.comboBox.insertSeparator(1)
		self.ui.tabWidget.currentChanged.connect(self.options)
		self.ui.comboBox.currentTextChanged.connect(self.dispoption)
		self.ui.editaccountButton.clicked.connect(self.editaccount)
		self.ui.openURLButton.clicked.connect(self.openURL)
		self.ui.copyusernameButton.clicked.connect(self.copyusername)
		self.ui.copypasswordButton.clicked.connect(self.copypassword)
		self.ui.lightButton.clicked.connect(lambda: self.toggle_stylesheet("BreezeStyleSheets/light.qss"))
		self.ui.darkButton.clicked.connect(lambda: self.toggle_stylesheet("BreezeStyleSheets/dark.qss"))
		self.ui.sunnyButton.clicked.connect(lambda: self.toggle_stylesheet("BreezeStyleSheets/sunny.qss"))
		self.ui.defaultButton.clicked.connect(lambda: self.toggle_stylesheet("BreezeStyleSheets/default.qss"))
		self.toggle_stylesheet("BreezeStyleSheets/sunny.qss")

		self.ui.statusbar.setText("Ready")
		self.FileSave.close()
		self.ui.comboBox.setDuplicatesEnabled(True)

		self.show()
	def generate(self):
		self.passwordlength = self.ui.passLine.value()
		self.password = Algorithm.generator(self.passwordlength)
		self.ui.password.setText(self.password)
		self.ui.statusbar.setText("New Password Generated")

	def copy(self):
		pyperclip.copy(self.ui.password.text())
		self.ui.statusbar.setText("Copied to Clipboard")

	def filesave(self):
		self.FileSave.ui.passwordLine.setText(self.password)
		self.options()
		self.dispoption()
		self.FileSave.show()

	def dialogclose(self):
		self.ui.statusbar.setText("Saved to File")
		self.options()
		self.dispoption()
		
	def options(self):
		if path.exists("passman.txt"):
			self.accounts = open("passman.txt",'rb')
			z = self.accounts.read()
			if z != b'':
				y = self.FileSave.f.decrypt(z)
				self.line = y.decode()
				realline = self.line.splitlines()
				self.fields = []
				for item in realline:
					try:
						x = item.split("=")
						self.fields.append(x[1])
					except IndexError:
						None

				for i in range(0,len(self.fields),4):
					if self.ui.comboBox.findText(self.fields[i]) == -1:
						self.ui.comboBox.addItem(self.fields[i])
				

	def dispoption(self):
		if path.exists("passman.txt"):

			if self.ui.comboBox.currentText() in self.fields:
				try:
					self.options()
					self.ui.websiteURLLine.setText(self.fields[self.fields.index(self.ui.comboBox.currentText())+1])
					self.ui.usernameLine.setText(self.fields[self.fields.index(self.ui.comboBox.currentText())+2])
					self.ui.passwordLine.setText(self.fields[self.fields.index(self.ui.comboBox.currentText())+3])
				except IndexError:
					None
			else:
				self.ui.websiteURLLine.setText("")
				self.ui.usernameLine.setText("")
				self.ui.passwordLine.setText("")

	def editaccount(self):
		self.FileSave.ui.accounttypeLine.setText(self.ui.comboBox.currentText())
		self.FileSave.ui.websiteURLLine.setText(self.ui.websiteURLLine.text())
		self.FileSave.ui.usernameLine.setText(self.ui.usernameLine.text())
		self.FileSave.ui.passwordLine.setText(self.ui.passwordLine.text())
		try:
			self.line = self.line.replace("\npassword="+self.fields[self.fields.index(self.ui.comboBox.currentText())+3],"")
			self.line = self.line.replace("\nusername="+self.fields[self.fields.index(self.ui.comboBox.currentText())+2],"")
			self.line = self.line.replace("\nwebURL="+self.fields[self.fields.index(self.ui.comboBox.currentText())+1],"")
			self.line = self.line.replace("\ntype="+self.fields[self.fields.index(self.ui.comboBox.currentText())],"")
		except ValueError:
			None
		self.lined = self.FileSave.f.encrypt(self.line.encode())
		try:
			with open ('passman.txt', 'wb') as myfile:
				myfile.write(self.lined)
		except FileExistsError:
			print('no file')
		self.options
		self.FileSave.show()

	def openURL(self):
		webbrowser.open("http://" + self.ui.websiteURLLine.text())

	def copyusername(self):
		pyperclip.copy(self.ui.usernameLine.text())
		self.ui.statusbar.setText("Copied to Clipboard")

	def copypassword(self):
		pyperclip.copy(self.ui.passwordLine.text())
		self.ui.statusbar.setText("Copied to Clipboard")

	def toggle_stylesheet(self,path):
		app = QApplication.instance()
		if app is None:
			raise RuntimeError("No Qt Application Found.")

		file = QFile(path)
		file.open(QFile.ReadOnly | QFile.Text)
		stream = QTextStream(file)
		app.setStyleSheet(stream.readAll())

if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = MyApp()
	w.show()
	sys.exit(app.exec_())
