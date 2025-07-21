# Copyright (C) 2025 IIJanII
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys, os
import json
from sourcehold.tool.convert.aiv.exports import to_json
from sourcehold.aivs.AIV import AIV
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFileDialog, QLineEdit, QLabel, QFrame, \
    QCheckBox, QComboBox, QMessageBox
from PyQt6.QtGui import QPalette, QColor, QIcon
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # attributes
        self.files = []
        self.save_folder = ""
        self.bool_convert_units = True
        self.cmbbx_widgets_convert_unit = []
        self.lbl_wigets_convert_unit = []
        self.dict_units = {"None": 0,
                           "Boiling Oil": 1,
                           "Mangonel": 2,
                           "Ballista": 3,
                           "Trebuchet": 4,
                           "Fireballista": 5,
                           "Archer": 6,
                           "Crossbowman": 7,
                           "Spearmen": 8,
                           "Pikeman": 9,
                           "Maceman": 10,
                           "Swordsman": 11,
                           "Knight": 12,
                           "Slave": 13,
                           "Slinger": 14,
                           "Assassin": 15,
                           "Arabian Bowmen": 16,
                           "Horse Archer": 17,
                           "Arabian Swordsman": 18,
                           "Fire Thrower": 19,
                           "Brazier": 20,
                           "FLG?": 21,
                           "Sentinel": 9023,
                           "Eunuch": 9024,
                           "Skirmisher": 9026,
                           "Not discovered yet": 0}
        self.lst_bedouin_units = ["Skirmisher", "Sapper", "Camel Lancer", "Heavy Camel", "Demolisher", "Eunuch",
                                  "Healer", "Ambusher"]
        self.cwd = os.getcwd()

        self.setWindowTitle("AIV to AIVJson")
        self.setFixedSize(360, 470)  # fix the window size
        self.setWindowIcon(QIcon(os.path.join(self.cwd, "images", "icon.png")))

        # Create a central widget and install it on the QMainWindow
        central = QWidget(self)
        central.setObjectName("central")
        background = os.path.join(self.cwd, "images", "background.png").replace("\\", "/")
        central.setStyleSheet(f"""
                    #central {{
                        background-image: url({background});
                        background-repeat: no-repeat;
                        background-position: left;
                    }}
                """)
        self.setCentralWidget(central)

        # button for help
        self.btn_help = QPushButton("Help", parent=central)
        self.btn_help.setGeometry(0, 0, 30, 20)
        self.btn_help.clicked.connect(self.help)
        self.btn_help.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
            }
            QPushButton:hover {
                /* optional hover effect */
                text-decoration: underline;
            }
        """)

        # button for credit
        self.btn_credit = QPushButton("Credits", parent=central)
        self.btn_credit.setGeometry(320, 0, 40, 20)
        self.btn_credit.clicked.connect(self.credits)
        self.btn_credit.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: white;
                        border: none;
                    }
                    QPushButton:hover {
                        /* optional hover effect */
                        text-decoration: underline;
                    }
                """)
        lbl_credit = QLabel("Tool made by IIJanII, converter made by gynt (sourcehold)", parent=central)
        lbl_credit.setGeometry(25, 450, 340, 20)
        lbl_credit.setStyleSheet(("""
                    QLabel {
                        background-color: transparent;
                        color: white;
                        border: none;
                    }
                """))

        # frame left
        self.frame_left = QFrame(parent=central)
        self.frame_left.setGeometry(20, 95, 320, 280)
        self.frame_left.setAutoFillBackground(True)
        pal = self.frame_left.palette()
        pal.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255, 200))
        self.frame_left.setPalette(pal)

        # frame right for convert units
        self.frame_convert_units = QFrame(parent=central)
        self.frame_convert_units.setGeometry(360, 95, 350, 280)
        self.frame_convert_units.setAutoFillBackground(True)
        pal = self.frame_convert_units.palette()
        pal.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255, 200))
        self.frame_convert_units.setPalette(pal)

        # convert unit widgets
        lbl_convert_units = QLabel("Click \"+\" to convert units to bedouin units:", parent=self.frame_left)
        lbl_convert_units.setGeometry(20, 20, 250, 30)
        self.btn_convert_units = QPushButton("+", parent=self.frame_left)
        self.btn_convert_units.setGeometry(270, 20, 30, 30)
        self.btn_convert_units.clicked.connect(self.open_unit_convertion)

        # Checkbox if apple farms should be converted to beduin barracks
        self.cbx = QCheckBox("Convert \"apple-farm\" to \"bedouin stockade\"", parent=self.frame_left)
        self.cbx.setGeometry(20, 50, 300, 30)
        self.cbx.setChecked(True)

        # button to browse for files
        btn_select_files = QPushButton("Browse...", parent=self.frame_left)
        btn_select_files.setGeometry(220, 110, 80, 30)
        btn_select_files.clicked.connect(self.choose_file)
        # line edit to display chosen files
        self.le_select_files = QLineEdit(parent=self.frame_left)
        self.le_select_files.setReadOnly(True)
        self.le_select_files.setGeometry(20, 110, 200, 30)
        # label selected files
        lbl_selected_files = QLabel("Selected AIV_Files:", parent=self.frame_left)
        lbl_selected_files.setGeometry(20, 85, 200, 30)

        # button to browse for files
        btn_save_folder = QPushButton("Browse...", parent=self.frame_left)
        btn_save_folder.setGeometry(220, 170, 80, 30)
        btn_save_folder.clicked.connect(self.select_save_folder)
        # line edit to display chosen files
        self.le_save_folder = QLineEdit(parent=self.frame_left)
        self.le_save_folder.setReadOnly(True)
        self.le_save_folder.setGeometry(20, 170, 200, 30)
        # label selected files
        lbl_selected_files = QLabel("Save Folder (optional):", parent=self.frame_left)
        lbl_selected_files.setGeometry(20, 145, 200, 30)

        # button
        self.btn_start_conversion = QPushButton("Convert .aiv to .aivjson", parent=self.frame_left)
        self.btn_start_conversion.setGeometry(20, 230, 280, 30)
        self.btn_start_conversion.clicked.connect(self.start_conversion)

    def help(self):
        mb = QMessageBox(self)
        mb.setWindowTitle("Help")
        mb.setTextFormat(Qt.TextFormat.RichText)
        mb.setIcon(QMessageBox.Icon.NoIcon)  # Icon-Typ
        mb.setText("Click \"Browse...\" and select the AIV files you wish to convert to .aivjson. The default folder "
                   "ist \"aiv\", but you can browse for your own folder. Optionally, you can specify a save folder "
                   "where the new files will be stored; otherwise, the converted files will be saved in the folder"
                   " \"aivjson\".<br><br>Since the old AIV Editor doesn't support the new Bedouin units, there's a "
                   "small workaround for Bedouin Lords: In the AIV Editor, place an \"apple farm\" where you want to "
                   "position the \"Bedouin stockade\". For the units, place a placeholder unit (for example, knights) "
                   "where you intend the Bedouin units to be placed. Then click the \"+\" and map the placeholder unit "
                   "to the desired Bedouin unit. Currently, only two Bedouin units have been identified (Nomad uses "
                   "Skirmisher and Kahin uses Eunuchs if you start with many troops. Technically, sentinel7.aivjson "
                   "contains a new unit, but i will not be placed. Could be Demolishers or Healers).<br><br>You can "
                   "find the link to the old AIV Editor <a href='http://stronghold.heavengames.com/downloads/getfile."
                   "php?id=7534&dd=1&s=0d0177bca23f6e96037b2db2b895c38f'>here</a>.")
        mb.exec()

    def credits(self):
        mb = QMessageBox(self)
        mb.setWindowTitle("Credits")
        mb.setTextFormat(Qt.TextFormat.RichText)
        mb.setIcon(QMessageBox.Icon.NoIcon)  # Icon-Typ
        mb.setText("Special thanks to gynt and his team from \"Sourcehold\"! They did the most work decoding the .aiv "
                   "files. See <a href='https://github.com/sourcehold/sourcehold-maps'>Sourcehold</a> for more "
                   "information. <br><br>Thanks also to the UCP team, from where I got the inspiration for the design. "
                   "Visit them here: <a href='https://unofficialcrusaderpatch.github.io'>UCP</a><br><br> And thanks to"
                   " Firefly for developing the Stronghold Crusader Definitive Edition!")
        mb.exec()

    def open_unit_convertion(self):
        if self.bool_convert_units:
            self.bool_convert_units = False
            self.btn_convert_units.setText("-")
            self.setFixedSize(730, 470)
            self.btn_credit.setGeometry(690, 0, 40, 20)

            # create comboxes
            for i in range(0, 8):
                self.cmbbx_widgets_convert_unit.append(QComboBox(parent=self.frame_convert_units))
                self.cmbbx_widgets_convert_unit[i].setGeometry(20, 20 + 30 * i, 200, 30)
                self.cmbbx_widgets_convert_unit[i].addItems(list(self.dict_units.keys())[:20])
                self.cmbbx_widgets_convert_unit[i].show()
                self.lbl_wigets_convert_unit.append(
                    QLabel("to:  " + self.lst_bedouin_units[i], parent=self.frame_convert_units))
                self.lbl_wigets_convert_unit[i].setGeometry(240, 20 + 30 * i, 150, 30)
                self.lbl_wigets_convert_unit[i].show()
                if i in [1, 2, 3, 4, 6, 7]:
                    self.cmbbx_widgets_convert_unit[i].addItems(["Not discovered yet"])
                    self.cmbbx_widgets_convert_unit[i].setCurrentText("Not discovered yet")
                    self.cmbbx_widgets_convert_unit[i].setDisabled(True)
        else:
            self.bool_convert_units = True
            self.btn_convert_units.setText("+")
            self.setFixedSize(360, 470)
            self.btn_credit.setGeometry(320, 0, 40, 20)
            for i in range(0, 8):
                # delete convert unit combox
                self.cmbbx_widgets_convert_unit[i].setParent(None)
                self.cmbbx_widgets_convert_unit[i].deleteLater()
                self.lbl_wigets_convert_unit[i].setParent(None)
                self.lbl_wigets_convert_unit[i].deleteLater()
            # reset lists
            self.cmbbx_widgets_convert_unit = []
            self.lbl_wigets_convert_unit = []

    def choose_file(self):
        self.files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select AIV-Files",  # dialog title
            os.path.join(self.cwd, "aiv"),  # starting directory
            "AIV-Files (*.aiv)"  # file filters
        )
        if self.files:
            names = ""
            for file in self.files:
                name = os.path.basename(file)
                names = names + name + ", "
            self.le_select_files.setText(names)

    def select_save_folder(self):
        self.save_folder = QFileDialog.getExistingDirectory(
            self,
            "Select save folder",  # dialog title
            os.path.join(self.cwd, "aivjson"),  # starting directory
        )
        if self.save_folder:
            self.le_save_folder.setText(self.save_folder)

    def start_conversion(self):
        # change button to inform user
        self.btn_start_conversion.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                    }
                    """)
        self.btn_start_conversion.setText("Conversion is running...")
        self.btn_start_conversion.repaint()
        lst_aiv_json_files = []
        finished = 0
        todo = len(self.files)
        for file in self.files:
            # load aiv-File and convert to json
            aiv = AIV().from_file(file)
            aiv_json = to_json(aiv)
            aiv_json = aiv_json.replace('\n', '')
            aiv_json = aiv_json.replace(" ", "")

            # convert apple farm to bedouin stockade if wished
            if self.cbx.isChecked():
                aiv_json = aiv_json.replace("\"itemType\":72", "\"itemType\":79")
            # convert units to bedouin units if wished (bool inverted)
            if not self.bool_convert_units:
                for i, cmbbx in enumerate(self.cmbbx_widgets_convert_unit):
                    # check if bedouin id is known
                    if self.lst_bedouin_units[i] in self.dict_units:
                        unit_id = self.dict_units[cmbbx.currentText()]
                        # check if unit should be converted
                        if unit_id:
                            # get bedouin unit id
                            bedouin_unit_id = self.dict_units[self.lst_bedouin_units[i]]
                            # change unit to bedouin unit
                            aiv_json = aiv_json.replace("\"itemType\":" + str(unit_id) + ",", "\"itemType\":" +
                                                        str(bedouin_unit_id) + ",")

            aiv_json = json.loads(aiv_json)

            # rescale objects positions
            for frame in aiv_json["frames"]:
                for i, position in enumerate(frame["tilePositionOfsets"]):
                    y = int(str(position)[:2])
                    x = int(str(position)[2:])
                    y = 99 - y
                    x = 99 - x
                    frame["tilePositionOfsets"][i] = int(f"{y:02d}{x:02d}")
            for unit in aiv_json["miscItems"]:
                y = int(str(unit["positionOfset"])[:2])
                x = int(str(unit["positionOfset"])[2:])
                y = 99 - y
                x = 99 - x
                unit["positionOfset"] = int(f"{y:02d}{x:02d}")

            # add finished file to list
            lst_aiv_json_files.append(aiv_json)
            finished += 1

        # create new file path
        if self.save_folder:
            for i, file in enumerate(self.files):
                name = os.path.splitext(os.path.basename(file))[0]
                self.files[i] = os.path.join(self.save_folder, name) + ".aivjson"
        else:
            for i, file in enumerate(self.files):
                name = os.path.splitext(os.path.basename(file))[0]
                self.files[i] = os.path.join(self.cwd, "aivjson", name) + ".aivjson"

        # save files
        for aiv_json, file in zip(lst_aiv_json_files, self.files):
            with open(file, 'w', encoding='utf-8-sig') as f:
                json.dump(aiv_json, f, separators=(',', ':'))

        # clear images
        lst_aiv_json_files.clear()
        self.files.clear()
        self.le_select_files.setText("")

        # user information
        QMessageBox.information(self,
                                "Information",
                                str(finished) + "/" + str(todo) + " files converted!")
        # button back to default
        self.btn_start_conversion.setStyleSheet("""
                            QPushButton {
                                background-color: lightgray;
                            }
                            """)
        self.btn_start_conversion.setText("Convert .aiv to .aivjson")
        self.btn_start_conversion.repaint()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
