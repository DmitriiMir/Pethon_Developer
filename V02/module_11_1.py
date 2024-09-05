from PySide6.QtWidgets import QFileDialog, QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QRadioButton, \
    QVBoxLayout, QWidget
from PySide6.QtGui import QIcon
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from scipy.interpolate import griddata
import tempfile
from pandas.api.types import is_numeric_dtype
from pandas.plotting import register_matplotlib_converters
import numpy as np
import webbrowser

register_matplotlib_converters()


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class CombinedCSVViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.radio_var = None
        self.radio_graphs = None
        self.csv_data = None
        self.file_path = None

        self.create_widgets()

    def create_widgets(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Кнопки
        self.btn_open = QPushButton("Открыть файл", self)
        self.btn_open.clicked.connect(self.open_file)
        layout.addWidget(self.btn_open)

        self.btn_show = QPushButton("Показать", self)
        self.btn_show.clicked.connect(self.show_data)
        layout.addWidget(self.btn_show)

        self.btn_clear = QPushButton("Очистить", self)
        self.btn_clear.clicked.connect(self.clear_data)
        layout.addWidget(self.btn_clear)

        self.btn_help = QPushButton("Справка", self)
        self.btn_help.clicked.connect(self.show_help)
        layout.addWidget(self.btn_help)

        # Комбобоксы
        self.combo1_label = QLabel("Показания прибора 1 (X):", self)
        layout.addWidget(self.combo1_label)
        self.combo1 = QComboBox(self)
        layout.addWidget(self.combo1)

        self.combo2_label = QLabel("Показания прибора 2 (Y):", self)
        layout.addWidget(self.combo2_label)
        self.combo2 = QComboBox(self)
        layout.addWidget(self.combo2)

        self.combo3_label = QLabel("Дистанция (Z):", self)
        layout.addWidget(self.combo3_label)
        self.combo3 = QComboBox(self)
        layout.addWidget(self.combo3)

        # Выбор языка
        self.language_label = QLabel("Change Language:", self)
        layout.addWidget(self.language_label)
        self.language_combo = QComboBox(self)
        self.language_combo.addItems(
            ["Русский", "English", "Português", "Español", "Français", "Deutsch", "Italiano", "Polski", "Türkçe",
             "العربية", "中文", "日本語"])
        self.language_combo.currentIndexChanged.connect(self.change_language)
        layout.addWidget(self.language_combo)

        # Радиокнопки
        self.radio_var = "Графики"
        self.radio_graphs = QRadioButton("Графики", self)
        self.radio_graphs.setChecked(True)
        self.radio_graphs.toggled.connect(lambda: self.set_radio_var("Графики"))
        layout.addWidget(self.radio_graphs)

        self.radio_histograms = QRadioButton("Гистограммы", self)
        self.radio_histograms.toggled.connect(lambda: self.set_radio_var("Гистограммы"))
        layout.addWidget(self.radio_histograms)

        self.radio_surface = QRadioButton("3D-поверхность", self)
        self.radio_surface.toggled.connect(lambda: self.set_radio_var("3D-поверхность"))
        layout.addWidget(self.radio_surface)

        central_widget.setLayout(layout)

    def open_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)")
        if file_path:
            self.file_path = file_path
            self.csv_data = pd.read_csv(file_path)
            self.update_combobox_values()

    def update_combobox_values(self):
        if self.csv_data is not None:
            columns = self.csv_data.columns
            for combo, label in zip([self.combo1, self.combo2, self.combo3],
                                    [self.combo1_label, self.combo2_label, self.combo3_label]):
                combo.clear()
                combo.addItem("")
                combo.addItems(columns)

    def set_radio_var(self, value):
        self.radio_var = value

    def show_data(self):
        if self.csv_data is not None:
            column1 = self.combo1.currentText()
            column2 = self.combo2.currentText()
            distance_col = self.combo3.currentText()

            plt.close('all')

            if self.radio_var == "Графики":
                if column1 and not column2 and not distance_col:
                    self.plot_single_column(column1, "График " + column1)
                elif column1 and column2 and not distance_col:
                    self.plot_double_columns(column1, column2, "График " + column1 + " и " + column2)
                elif column1 and column2 and distance_col:
                    self.plot_all_columns(column1, column2, distance_col, "График " + column1 + " и " + column2)
            elif self.radio_var == "Гистограммы":
                if column1 and not column2 and not distance_col:
                    self.plot_single_column_histogram(column1, "Гистограмма " + column1)
                elif column1 and column2 and not distance_col:
                    self.plot_double_columns_histogram(column1, column2, "Гистограмма " + column1 + " и " + column2)
                elif column1 and column2 and distance_col:
                    self.plot_all_columns_histogram(column1, column2, distance_col,
                                                    "Гистограмма " + column1 + " и " + column2)
            elif self.radio_var == "3D-поверхность":
                if column1 and column2 and distance_col:
                    self.plot_surface(column1, column2, distance_col, "3D-поверхность")

    def plot_single_column(self, column, title):
        plt.figure()
        plt.plot(self.csv_data[column], label=column)
        plt.xlabel("Отсчет")
        plt.ylabel("Показания")
        plt.title(title)
        plt.legend()
        plt.show()

    def plot_double_columns(self, column1, column2, title):
        plt.figure()
        plt.plot(self.csv_data[column1], label=column1)
        plt.plot(self.csv_data[column2], label=column2)
        plt.xlabel("Отсчет")
        plt.ylabel("Показания")
        plt.title(title)
        plt.legend()
        plt.show()

    def plot_all_columns(self, column1, column2, distance_col, title):
        plt.figure()

        if is_numeric_dtype(self.csv_data[distance_col]):
            plt.plot(self.csv_data[distance_col], self.csv_data[column1], label=column1)
            plt.plot(self.csv_data[distance_col], self.csv_data[column2], label=column2)
            plt.xlabel(distance_col)
        else:
            plt.plot(self.csv_data[distance_col], self.csv_data[column1], label=column1)
            plt.plot(self.csv_data[distance_col], self.csv_data[column2], label=column2)
            plt.xlabel("Дистанция")

        plt.ylabel("Показания")
        plt.title(title)
        plt.legend()

        if is_numeric_dtype(self.csv_data[distance_col]):
            plt.gcf().autofmt_xdate()

        plt.show()

    def plot_single_column_histogram(self, column, title):
        plt.figure()
        sns.histplot(self.csv_data[column], kde=True, color='skyblue', bins=10)
        plt.xlabel("Показания")
        plt.title(title)
        plt.show()

    def plot_double_columns_histogram(self, column1, column2, title):
        plt.figure()
        sns.histplot(self.csv_data[column1], kde=True, color='skyblue', bins=10, label=column1)
        sns.histplot(self.csv_data[column2], kde=True, color='salmon', bins=10, label=column2)
        plt.xlabel("Показания")
        plt.title(title)
        plt.legend()
        plt.show()

    def plot_all_columns_histogram(self, column1, column2, distance_col, title):
        plt.figure()

        if is_numeric_dtype(self.csv_data[distance_col]):
            sns.histplot(x=self.csv_data[distance_col], y=self.csv_data[column1], kde=True, color='skyblue',
                         label=column1)
            sns.histplot(x=self.csv_data[distance_col], y=self.csv_data[column2], kde=True, color='salmon',
                         label=column2)
            plt.xlabel(distance_col)
        else:
            sns.histplot(x=self.csv_data[distance_col], y=self.csv_data[column1], kde=True, color='skyblue',
                         label=column1)
            sns.histplot(x=self.csv_data[distance_col], y=self.csv_data[column2], kde=True, color='salmon',
                         label=column2)
            plt.xlabel("Дистанция")

        plt.ylabel("Показания")
        plt.title(title)
        plt.legend()

        if is_numeric_dtype(self.csv_data[distance_col]):
            plt.gcf().autofmt_xdate()

        plt.show()

    def plot_surface(self, x_col, y_col, z_col, title):
        max_points = 1000
        step = max(1, len(self.csv_data) // max_points)

        x = np.array(self.csv_data[x_col][::step])
        y = np.array(self.csv_data[y_col][::step])
        z = np.array(self.csv_data[z_col][::step])

        xi = np.linspace(min(x), max(x), 100)
        yi = np.linspace(min(y), max(y), 100)
        xi, yi = np.meshgrid(xi, yi)

        zi = griddata((x, y), z, (xi, yi), method='linear')

        fig = go.Figure(data=[go.Surface(z=zi, x=xi, y=yi)])
        fig.update_layout(scene=dict(
            xaxis_title=f"{x_col} (X)",
            yaxis_title=f"{y_col} (Y)",
            zaxis_title=f"{z_col} (Высота)",
        ))

        temp_html_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        fig.write_html(temp_html_file.name)
        temp_html_file.close()

        webbrowser.open("file://" + temp_html_file.name)

    def clear_data(self):
        self.combo1.setCurrentIndex(0)
        self.combo2.setCurrentIndex(0)
        self.combo3.setCurrentIndex(0)
        self.file_path = None
        self.csv_data = None

    def change_language(self, index):
        if index == 0:
            self.translate("ru")  # Русский
        elif index == 1:
            self.translate("en")  # Английский
        elif index == 2:
            self.translate("pt")  # Португальский
        elif index == 3:
            self.translate("es")  # Испанский
        elif index == 4:
            self.translate("fr")  # Французский
        elif index == 5:
            self.translate("de")  # Немецкий
        elif index == 6:
            self.translate("it")  # Итальянский
        elif index == 7:
            self.translate("pl")  # Польский
        elif index == 8:
            self.translate("tr")  # Турецкий
        elif index == 9:
            self.translate("ar")  # Арабский
        elif index == 10:
            self.translate("zh")  # Китайский
        elif index == 11:
            self.translate("ja")  # Японский

    def translate(self, lang):
        if lang == "ru":
            self.btn_open.setText("Открыть файл")
            self.btn_show.setText("Показать")
            self.btn_clear.setText("Очистить")
            self.btn_help.setText("Справка")
            self.language_label.setText("Выбор языка:")
            self.combo1_label.setText("Показания прибора 1 (X):")
            self.combo2_label.setText("Показания прибора 2 (Y):")
            self.combo3_label.setText("Дистанция (Z):")
            self.radio_graphs.setText("Графики")
            self.radio_histograms.setText("Гистограммы")
            self.radio_surface.setText("3D-поверхность")
            self.show_help("ru")

        elif lang == "en":
            self.btn_open.setText("Open File")
            self.btn_show.setText("Show")
            self.btn_clear.setText("Clear")
            self.btn_help.setText("Help")
            self.language_label.setText("Change Language:")
            self.combo1_label.setText("Device 1 Readings (X):")
            self.combo2_label.setText("Device 2 Readings (Y):")
            self.combo3_label.setText("Distance (Z):")
            self.radio_graphs.setText("Graphs")
            self.radio_histograms.setText("Histograms")
            self.radio_surface.setText("3D Surface")
            self.show_help(lang)

        elif lang == "pt":
            self.btn_open.setText("Abrir Arquivo")
            self.btn_show.setText("Mostrar")
            self.btn_clear.setText("Limpar")
            self.btn_help.setText("Ajuda")
            self.language_label.setText("Alterar Idioma:")
            self.combo1_label.setText("Leituras Dispositivo 1 (X):")
            self.combo2_label.setText("Leituras Dispositivo 2 (Y):")
            self.combo3_label.setText("Distância (Z):")
            self.radio_graphs.setText("Gráficos")
            self.radio_histograms.setText("Histogramas")
            self.radio_surface.setText("Superfície 3D")
            self.show_help(lang)

        elif lang == "es":
            self.btn_open.setText("Abrir Archivo")
            self.btn_show.setText("Mostrar")
            self.btn_clear.setText("Limpiar")
            self.btn_help.setText("Ayuda")
            self.language_label.setText("Cambiar Idioma:")
            self.combo1_label.setText("Lecturas Dispositivo 1 (X):")
            self.combo2_label.setText("Lecturas Dispositivo 2 (Y):")
            self.combo3_label.setText("Distancia (Z):")
            self.radio_graphs.setText("Gráficos")
            self.radio_histograms.setText("Histogramas")
            self.radio_surface.setText("Superficie 3D")
            self.show_help(lang)

        elif lang == "fr":
            self.btn_open.setText("Ouvrir le fichier")
            self.btn_show.setText("Afficher")
            self.btn_clear.setText("Effacer")
            self.btn_help.setText("Aide")
            self.language_label.setText("Choix de la langue :")
            self.combo1_label.setText("Lecture du dispositif 1 (X) :")
            self.combo2_label.setText("Lecture du dispositif 2 (Y) :")
            self.combo3_label.setText("Distance (Z) :")
            self.radio_graphs.setText("Graphiques")
            self.radio_histograms.setText("Histogrammes")
            self.radio_surface.setText("Surface 3D")
            self.show_help(lang)

        elif lang == "de":
            self.btn_open.setText("Datei öffnen")
            self.btn_show.setText("Anzeigen")
            self.btn_clear.setText("Löschen")
            self.btn_help.setText("Hilfe")
            self.language_label.setText("Sprache ändern:")
            self.combo1_label.setText("Gerät 1 Messwerte (X):")
            self.combo2_label.setText("Gerät 2 Messwerte (Y):")
            self.combo3_label.setText("Entfernung (Z):")
            self.radio_graphs.setText("Diagramme")
            self.radio_histograms.setText("Histogramme")
            self.radio_surface.setText("3D-Oberfläche")
            self.show_help(lang)

        elif lang == "it":
            self.btn_open.setText("Apri File")
            self.btn_show.setText("Mostra")
            self.btn_clear.setText("Cancella")
            self.btn_help.setText("Aiuto")
            self.language_label.setText("Cambia Lingua:")
            self.combo1_label.setText("Lettura Dispositivo 1 (X):")
            self.combo2_label.setText("Lettura Dispositivo 2 (Y):")
            self.combo3_label.setText("Distanza (Z):")
            self.radio_graphs.setText("Grafici")
            self.radio_histograms.setText("Istogrammi")
            self.radio_surface.setText("Superficie 3D")
            self.show_help(lang)

        elif lang == "pl":
            self.btn_open.setText("Otwórz Plik")
            self.btn_show.setText("Pokaż")
            self.btn_clear.setText("Wyczyść")
            self.btn_help.setText("Pomoc")
            self.language_label.setText("Zmień Język:")
            self.combo1_label.setText("Odczyty Urządzenia 1 (X):")
            self.combo2_label.setText("Odczyty Urządzenia 2 (Y):")
            self.combo3_label.setText("Odległość (Z):")
            self.radio_graphs.setText("Wykresy")
            self.radio_histograms.setText("Histogramy")
            self.radio_surface.setText("Powierzchnia 3D")
            self.show_help(lang)

        elif lang == "tr":
            self.btn_open.setText("Dosya Aç")
            self.btn_show.setText("Göster")
            self.btn_clear.setText("Temizle")
            self.btn_help.setText("Yardım")
            self.language_label.setText("Dil Değiştir:")
            self.combo1_label.setText("Cihaz 1 Okumaları (X):")
            self.combo2_label.setText("Cihaz 2 Okumaları (Y):")
            self.combo3_label.setText("Uzaklık (Z):")
            self.radio_graphs.setText("Grafikler")
            self.radio_histograms.setText("Histogramlar")
            self.radio_surface.setText("3D Yüzey")
            self.show_help(lang)

        elif lang == "ar":
            self.btn_open.setText("فتح الملف")
            self.btn_show.setText("عرض")
            self.btn_clear.setText("مسح")
            self.btn_help.setText("مساعدة")
            self.language_label.setText("تغيير اللغة:")
            self.combo1_label.setText("قراءات الجهاز 1 (X):")
            self.combo2_label.setText("قراءات الجهاز 2 (Y):")
            self.combo3_label.setText("المسافة (Z):")
            self.radio_graphs.setText("الرسوم البيانية")
            self.radio_histograms.setText("الهيستوغرامات")
            self.radio_surface.setText("السطح ثلاثي الأبعاد")
            self.show_help(lang)

        elif lang == "zh":
            self.btn_open.setText("打开文件")
            self.btn_show.setText("显示")
            self.btn_clear.setText("清除")
            self.btn_help.setText("帮助")
            self.language_label.setText("选择语言：")
            self.combo1_label.setText("设备1读数（X）：")
            self.combo2_label.setText("设备2读数（Y）：")
            self.combo3_label.setText("距离（Z）：")
            self.radio_graphs.setText("图表")
            self.radio_histograms.setText("直方图")
            self.radio_surface.setText("3D表面")
            self.show_help(lang)

        elif lang == "ja":
            self.btn_open.setText("ファイルを開く")
            self.btn_show.setText("表示する")
            self.btn_clear.setText("クリア")
            self.btn_help.setText("ヘルプ")
            self.language_label.setText("言語の変更:")
            self.combo1_label.setText("デバイス1の読み取り値（X）:")
            self.combo2_label.setText("デバイス2の読み取り値（Y）:")
            self.combo3_label.setText("距離（Z）:")
            self.radio_graphs.setText("グラフ")
            self.radio_histograms.setText("ヒストグラム")
            self.radio_surface.setText("3Dサーフェス")
            self.show_help(lang)

    def show_help(self):
        help_files = {
            "ru": "help/00_Help_manual_ru.html",
            "en": "help/01_Help_manual_en.html",
            "pt": "help/02_Help_manual_pt.html",
            "es": "help/03_Help_manual_es.html",
            "fr": "help/04_Help_manual_fr.html",
            "de": "help/05_Help_manual_de.html",
            "it": "help/06_Help_manual_it.html",
            "pl": "help/07_Help_manual_pl.html",
            "tr": "help/08_Help_manual_tr.html",
            "ar": "help/09_Help_manual_ar.html",
            "zh": "help/10_Help_manual_zh.html",
            "ja": "help/11_Help_manual_ja.html",
        }

        current_index = self.language_combo.currentIndex()
        language_code = {
            0: "ru",
            1: "en",
            2: "pt",
            3: "es",
            4: "fr",
            5: "de",
            6: "it",
            7: "pl",
            8: "tr",
            9: "ar",
            10: "zh",
            11: "ja"
        }.get(current_index)

        if language_code in help_files:
            full_path = resource_path(help_files[language_code])
            webbrowser.open_new_tab(full_path)


if __name__ == "__main__":
    app = QApplication([])
    app.setApplicationName("GraphPythonMag_v02")
    app_icon = QIcon(resource_path("rick.ico"))
    app.setWindowIcon(app_icon)
    window = CombinedCSVViewer()
    window.show()
    sys.exit(app.exec())
