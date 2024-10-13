import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QLineEdit, QFormLayout
from PySide6.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation


class MeteorFlightApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.trajectory_line = None
        self.body = None
        self.setWindowTitle("Meteor Flight")
        self.setGeometry(100, 100, 800, 600)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        main_layout = QVBoxLayout(self.main_widget)

        input_layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.velocity_input = QLineEdit(self)
        self.angle_input = QLineEdit(self)
        self.height_input = QLineEdit(self)

        form_layout.addRow("Начальная скорость (м/с):", self.velocity_input)
        form_layout.addRow("Угол броска (градусы):", self.angle_input)
        form_layout.addRow("Высота запуска (м):", self.height_input)

        input_layout.addLayout(form_layout)

        self.button_animate = QPushButton("Анимировать движение", self)
        self.button_animate.clicked.connect(self.animate_trajectory)
        input_layout.addWidget(self.button_animate)

        self.button_pause = QPushButton("Пауза", self)
        self.button_pause.clicked.connect(self.pause_animation)
        input_layout.addWidget(self.button_pause)

        self.button_clear = QPushButton("Очистить", self)
        self.button_clear.clicked.connect(self.clear_inputs_and_plot)
        input_layout.addWidget(self.button_clear)

        # Стиль кнопок
        button_style = """
            QPushButton {
                background-color: green;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: blue;
            }
            QPushButton:pressed {
                background-color: red;
            }
        """
        self.button_animate.setStyleSheet(button_style)
        self.button_pause.setStyleSheet(button_style)
        self.button_clear.setStyleSheet(button_style)

        # Логотип программы, можно закомментировать блок или добавить картинку в папку со скриптом
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("./_Meteor_flight.jpg") # Ссылка на картинку
        logo_label.setPixmap(logo_pixmap)
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(200, 200)

        top_layout = QHBoxLayout()
        top_layout.addLayout(input_layout)
        top_layout.addWidget(logo_label) # Закомментировать, если нет картинки

        main_layout.addLayout(top_layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)
        self.init_plot()

        self.ani = None
        self.is_paused = False

    def init_plot(self):
        self.ax.clear()
        self.trajectory_line, = self.ax.plot([], [], 'ro', markersize=3, label="Траектория")
        self.body = self.ax.scatter([], [], color='blue', s=50, label="Метеор")
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 50)
        self.ax.set_xlabel("Расстояние (м)")
        self.ax.set_ylabel("Высота (м)")
        self.ax.grid(True)
        self.canvas.draw()

    def animate_trajectory(self):
        if self.ani:
            self.ani.event_source.stop()
            self.ani = None

        try:
            velocity = float(self.velocity_input.text())
            angle_deg = float(self.angle_input.text())
            height = float(self.height_input.text()) + 0.001
        except ValueError:
            self.show_error("Пожалуйста, введите числовые значения!")
            return
        # Логика
        angle_rad = np.radians(angle_deg)
        g = 9.81

        v_x = velocity * np.cos(angle_rad)
        v_y = velocity * np.sin(angle_rad)

        t_flight = (v_y + np.sqrt(v_y ** 2 + 2 * g * height)) / g

        self.t = np.linspace(0, t_flight, num=500)

        # Вычисление координат
        self.x = v_x * self.t
        self.y = height + v_y * self.t - 0.5 * g * self.t ** 2

        # Настройка графика
        self.ax.set_xlim(0, max(self.x))
        self.ax.set_ylim(0, max(self.y) + 1)

        self.ani = FuncAnimation(self.figure, self.update_plot, frames=len(self.t), interval=20, blit=False)
        self.canvas.draw()

    def update_plot(self, frame):
        if self.y[frame] <= 0 or frame == len(self.t) - 1:
            if self.ani:
                self.ani.event_source.stop()
            return self.trajectory_line, self.body

        self.trajectory_line.set_data(self.x[:frame], self.y[:frame])
        self.body.set_offsets([[self.x[frame], self.y[frame]]])

        return self.trajectory_line, self.body

    def pause_animation(self):
        if self.ani:
            if self.is_paused:
                self.ani.event_source.start()
                self.button_pause.setText("Пауза")
            else:
                self.ani.event_source.stop()
                self.button_pause.setText("Продолжить")
            self.is_paused = not self.is_paused

    def clear_inputs_and_plot(self):
        if self.ani:
            self.ani.event_source.stop()
            self.ani = None

        self.velocity_input.clear()
        self.angle_input.clear()
        self.height_input.clear()

        self.init_plot()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MeteorFlightApp()
    window.show()
    sys.exit(app.exec())
