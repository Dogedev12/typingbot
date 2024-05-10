import sys
import pyautogui
import time
from bs4 import BeautifulSoup
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer


def open_html_file(filename, text_to_write):
    with open(filename, 'w') as output:
        output.write(text_to_write)

def load_html_of_current_page(html):
        open_html_file('typing_test.html', html)

def on_page_finished():
    global firstPageLoaded  # Declare firstPageLoaded as global
    if not hasattr(on_page_finished, 'firstPageLoaded'):
        on_page_finished.firstPageLoaded = False
    if on_page_finished.firstPageLoaded:
        print("New page loaded")
    else:
        on_page_finished.firstPageLoaded = True
        # type username, wait for password box, then type password
        username="test"
        pyautogui.typewrite(username+'\n')
        QTimer.singleShot(2000, type_password)       
    
def type_password():
    password = "test"
    pyautogui.typewrite(password+'\n')
    QTimer.singleShot(2000, go_to_Tests)

def go_to_Tests():
    #only works at 1440p
    pyautogui.moveTo(1244, 55)
    pyautogui.leftClick()
    QTimer.singleShot(2000, start_test)

def start_test():
    pyautogui.moveTo(954, 530)
    pyautogui.leftClick()
    QTimer.singleShot(2000, get_test_html)

def get_test_html():
    web.page().runJavaScript("document.documentElement.innerHTML", load_html_of_current_page)
    QTimer.singleShot(2000, get_letter_list)

def get_letter_list():
    with open('typing_test.html', 'r') as html_content:
        soup = BeautifulSoup(html_content, "html.parser")
    # Find all elements with class name "letter", which is what we need to type
    letters = soup.find_all(class_="letter")
    QTimer.singleShot(3000, lambda: press_keys(letters))

def press_keys(letters):
    n = len(letters)
    print(n)
    keys = []
    start_time = time.time()
    words = 1

    for i in range(n):
        letter = letters[i].text    
        if letter == u'\xa0': #nbsp
            keys.append('space')
            words += 1
        else:
            keys.append(letter)
        
    #print(keys)
    pyautogui.press(keys, 1, 0.05)

    end_time = time.time()
    minutes = (end_time-start_time)/60
    print((n/5)/minutes)
    print(words)

app = QApplication(sys.argv)
web = QWebEngineView()
global firstPageLoaded
firstPageLoaded = False
web.load(QUrl("https://typing.com/student/login"))
web.showMaximized()
web.loadFinished.connect(on_page_finished)

# web.close()
sys.exit(app.exec_())