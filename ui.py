from imp import reload
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPlainTextEdit, QScrollArea, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont
from textblob import TextBlob

def analyze_sentiment(text):
    try:
        blob = TextBlob(text)
        words_sentiment = {}

        for word in blob.words:
            word_sentiment = TextBlob(word).sentiment.polarity
            words_sentiment[word] = word_sentiment

        return words_sentiment

    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return None
    
def analyze_whole_sentence_sentiment(text):
    blob = TextBlob(text)
    sentence_sentiment = blob.sentiment.polarity
    return round(sentence_sentiment * 100)

def dict_of_words_with_given_sentiment(text, sentiment):
    try:
        sentiment_analysis = analyze_sentiment(text)
        if sentiment_analysis is None:
            return None

        dict_of_words = {}
        for word, sentiments in sentiment_analysis.items():
            if sentiment == "Negative":
                if sentiments < 0:
                    dict_of_words[word] = sentiments

            if sentiment == "Positive":
                if sentiments > 0:
                    dict_of_words[word] = sentiments
        for word, sentiments in dict_of_words.items():
            print(f"{word}: {sentiments}")
        return dict_of_words

    except Exception as e:
        print(f"Error in creating dictionary of words: {e}")
        return None

# PyQt6 application
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Email changer")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #222222; color: #fef9f3;")

        self.label = QLabel("Írd át az emailodat pozitívra vagy negatívra!", self)
        self.label.setStyleSheet("color: white; font-size: 20px;")

        self.EmailLabel = QLabel("Az Email:", self)
        self.EmailLabel.setStyleSheet("color: white; font-size: 14px;")
        
        self.text_input = QPlainTextEdit(self)
        self.text_input.setFixedHeight(150)
        self.text_input.setStyleSheet("background-color: #892CDC; border-radius: 5px; margin-bottom: 20px;")
        
        self.ReplacedLabel = QLabel("A cserélendő szavak listája:", self)
        self.ReplacedLabel.setStyleSheet("color: white; font-size: 14px; border-radius: 5px; margin-top: 25px;")
        
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setFixedHeight(200)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("padding: 5px; border-radius: 5px; margin-bottom: 20px;")

        self.display = QLabel("", self)
        self.display.setFixedHeight(200)
        self.display.setAutoFillBackground(True)
        self.display.setStyleSheet("background-color: #892CDC; border-radius: 5px; margin-bottom: 20px;")
        
        self.scroll_area.setWidget(self.display)

        self.label_select = QLabel("Itt válaszd ki, hogy milyen szavakat szeretnél lecserélni:", self)
        self.label_select.setStyleSheet("color: white")
        self.label_select.setStyleSheet("color: white; font-size: 14px; margin-left: 120px;")

        self.select_input = QComboBox(self)
        self.select_input.addItem("Positive")
        self.select_input.addItem("Negative")
        self.select_input.setFixedSize(100, 50)
        self.select_input.setStyleSheet("background-color: #52057B; border-radius: 5px;")

        self.go_button = QPushButton("Go", self)
        self.go_button.clicked.connect(self.go_button_clicked)
        self.go_button.setFixedSize(100, 50)
        self.go_button.setStyleSheet("background-color: #52057B; border-radius: 5px;")

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        self.cancel_button.setFixedSize(100, 50)
        self.cancel_button.setStyleSheet("background-color: #52057B; border-radius: 5px;")
        
        self.sentiment_score = QLabel(self)
        self.sentiment_score.setStyleSheet("display: none;")


        self.setup_layout()


    def setup_layout(self):

        layout = QVBoxLayout()

        layout.addWidget(self.label)
        layout.addWidget(self.sentiment_score)
        layout.addWidget(self.EmailLabel)
        layout.addWidget(self.text_input)
        layout.addWidget(self.ReplacedLabel)
        layout.addWidget(self.scroll_area)


        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.label_select)
        buttons_layout.addWidget(self.select_input)
        buttons_layout.addWidget(self.go_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def go_button_clicked(self):
        input_text = self.text_input.toPlainText()
        selected_option = self.select_input.currentText()

        try:
            dict_of_words = dict_of_words_with_given_sentiment(input_text, sentiment=selected_option)
            
            first = True
            
            for word, sentiments in dict_of_words.items():
                current_text = self.display.text()
                if first:
                    next_text = f"{word}"
                    first = False
                else:
                    next_text = f"{current_text}\n{word}"
                self.display.setText(f"{next_text}")
                
            sentiment_score = analyze_whole_sentence_sentiment(input_text)
            sentiment_text = f"A szöveg: {sentiment_score}%-ban {'pozitív' if sentiment_score > 0 else 'negatív'}"
            
            self.sentiment_score.setText(sentiment_text)
            self.sentiment_score.setStyleSheet("color: white; font-size: 16px; display: block; text-align: center;")
        except Exception as e:
            print(f"Error in go_button_clicked: {e}")

    def cancel_button_clicked(self):
        self.text_input.clear()
        self.select_input.setCurrentIndex(0)
        self.display.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
