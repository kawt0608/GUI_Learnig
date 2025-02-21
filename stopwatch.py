# stopwatch.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout, QMainWindow
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
import datetime

class Stopwatch(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initMainUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_time = 0  # milliseconds
        self.lap_times = []

        # 現在時刻の表示を開始
        self.current_time_timer = QTimer(self)
        self.current_time_timer.timeout.connect(self.update_current_time)
        self.current_time_timer.start(1000)  # 1秒ごとに更新

        self.is_mini_mode = False  # ミニモードのフラグ

    def initMainUI(self):
        self.setWindowTitle("Stylish Stopwatch")
        self.resize(400, 500)

        # メインウィジェット設定
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # レイアウトを作成
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # 現在時刻を表示するラベル
        self.current_time_label = QLabel("", self)
        self.current_time_label.setAlignment(Qt.AlignCenter)

        # 経過時間を表示するラベル
        self.time_label = QLabel("00:00.0", self)
        self.time_label.setAlignment(Qt.AlignCenter)

        # フルモードのUI要素
        self.full_layout = QVBoxLayout()

        # ボタンとリストウィジェットを追加
        self.button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.reset_button = QPushButton("Reset", self)
        
        self.full_layout.addLayout(self.button_layout)

        self.mini_button = QPushButton("Mini Mode", self)
        self.button_layout.addWidget(self.mini_button)
        
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)
        self.button_layout.addWidget(self.reset_button)
        self.button_layout.setSpacing(10)

        self.lap_button = QPushButton("Lap", self)
        self.button_layout.addWidget(self.lap_button)
        
        self.lap_list_widget = QListWidget(self)
        self.full_layout.addWidget(self.lap_list_widget)

        # ボタンのクリックイベント接続
        self.start_button.clicked.connect(self.start_timer)
        self.stop_button.clicked.connect(self.stop_timer)
        self.reset_button.clicked.connect(self.reset_timer)
        self.lap_button.clicked.connect(self.record_lap)
        self.mini_button.clicked.connect(self.toggle_mini_mode)

        # レイアウトに追加
        self.layout.addWidget(self.current_time_label)
        self.layout.addWidget(self.time_label)
        self.layout.addLayout(self.full_layout)
        self.main_widget.setLayout(self.layout)

        # スタイルシートを設定してデザインを調整
        self.setStyleSheet("""
            QLabel {
                color: #FFEB3B;  /* 強調の黄色 */
                background-color: #000000;  /* 黒背景 */
                padding: 20px;
                border-radius: 10px;
                font-family: 'Arial';
                font-weight: bold;
                font-size: 32px;
            }
            QPushButton {
                background-color: #333333;  /* グレーのボタン */
                color: #FFFFFF;  /* 白い文字 */
                padding: 10px 15px;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #555555;  /* 少し明るいグレー */
            }
            QPushButton:pressed {
                background-color: #222222;  /* ダークグレー */
            }
            QListWidget {
                background-color: #000000;  /* 黒背景 */
                border: none;
                border-radius: 10px;
                font-family: 'Courier New';
                font-size: 16px;
                color: #FFFFFF;  /* 白い文字 */
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border: 1px solid #555555;  /* グレーの境界 */
                margin: 3px;
                border-radius: 5px;
                background-color: #111111;  /* ダーク背景 */
            }
            QWidget {
                background-color: #000000;  /* 全体の黒背景 */
            }
        """)

    def toggle_mini_mode(self):
        if not self.is_mini_mode:
            # ミニモードに切り替え
            self.lap_list_widget.hide()
            self.start_button.hide()
            self.stop_button.hide()
            self.reset_button.hide()
            self.lap_button.hide()
            self.mini_button.setText("Full Mode")
            self.resize(250, 150)
            self.is_mini_mode = True
        else:
            # フルモードに切り替え
            self.lap_list_widget.show()
            self.start_button.show()
            self.stop_button.show()
            self.reset_button.show()
            self.lap_button.show()
            self.mini_button.setText("Mini Mode")
            self.resize(400, 500)
            self.is_mini_mode = False

    def start_timer(self):
        if not self.timer.isActive():
            self.timer.start(100)  # 100ミリ秒ごとにタイマーを更新

    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()

    def reset_timer(self):
        self.stop_timer()
        self.elapsed_time = 0
        self.lap_times = []
        self.time_label.setText("00:00.0")
        self.lap_list_widget.clear()

    def record_lap(self):
        if self.timer.isActive():
            lap_time = self.elapsed_time_format()
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            lap_record = f"Lap: {lap_time} | Recorded At: {current_time}"

            self.lap_times.append(lap_record)
            
            # ラップタイムをQListWidgetに追加
            lap_item = QListWidgetItem(lap_record)
            font = QFont("Courier New", 16)
            lap_item.setFont(font)
            self.lap_list_widget.addItem(lap_item)

            self.save_lap_times()

    def update_timer(self):
        self.elapsed_time += 100
        self.time_label.setText(self.elapsed_time_format())

    def update_current_time(self):
        now = datetime.datetime.now()
        self.current_time_label.setText(now.strftime("%Y-%m-%d %H:%M:%S"))

    def elapsed_time_format(self):
        seconds = (self.elapsed_time // 1000) % 60
        minutes = (self.elapsed_time // 60000)
        centiseconds = (self.elapsed_time // 100) % 10
        return f"{minutes:02}:{seconds:02}.{centiseconds}"

    def save_lap_times(self):
        now = datetime.datetime.now()
        filename = now.strftime("laps_%Y%m%d_%H%M%S.txt")
        with open(filename, 'w') as file:
            for idx, lap_time in enumerate(self.lap_times, 1):
                file.write(f"Lap {idx}: {lap_time}\n")

    def resizeEvent(self, event):
        scaleFactor = min(self.width() / 400, self.height() / 500)
        font_size = int(scaleFactor * 32)  # 強調するために大きく

        font = QFont()
        font.setPointSize(font_size)
        self.current_time_label.setFont(font)
        self.time_label.setFont(font)

        buttons = [self.start_button, self.stop_button, self.reset_button, self.lap_button, self.mini_button]
        for button in buttons:
            buttonFont = QFont()
            buttonFont.setPointSize(int(scaleFactor * 16))
            button.setFont(buttonFont)

        super().resizeEvent(event)
