import sys
import os
import json
import subprocess
from PyQt6.QtWidgets import (QApplication, QSystemTrayIcon, QMenu, 
                             QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSpinBox, QPushButton, QMessageBox, QWidget)
from PyQt6.QtCore import QTimer, pyqtSignal, Qt
from PyQt6.QtGui import QIcon, QAction, QCursor
import classes.config as config

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Alarm Settings")
        self.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        
        on_layout = QHBoxLayout()
        on_layout.addWidget(QLabel("ON Duration (minutes):"))
        self.on_duration_spin = QSpinBox()
        self.on_duration_spin.setRange(1, 999)
        self.on_duration_spin.setValue(20)
        on_layout.addWidget(self.on_duration_spin)
        layout.addLayout(on_layout)
        
        off_layout = QHBoxLayout()
        off_layout.addWidget(QLabel("OFF Duration (minutes):"))
        self.off_duration_spin = QSpinBox()
        self.off_duration_spin.setRange(1, 999)
        self.off_duration_spin.setValue(20)
        off_layout.addWidget(self.off_duration_spin)
        layout.addLayout(off_layout)
        
        cycles_layout = QHBoxLayout()
        cycles_layout.addWidget(QLabel("Cycles (0 = forever):"))
        self.cycles_spin = QSpinBox()
        self.cycles_spin.setRange(0, 999)
        self.cycles_spin.setValue(0)
        cycles_layout.addWidget(self.cycles_spin)
        layout.addLayout(cycles_layout)
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.center_on_screen()
        self.load_settings()
    
    def load_settings(self):
        try:
            with open('_config.json', 'r') as f:
                settings = json.load(f)
                self.on_duration_spin.setValue(settings.get('on_duration', 1200) // 60)
                self.off_duration_spin.setValue(settings.get('off_duration', 1200) // 60)
                self.cycles_spin.setValue(settings.get('cycles', 0))
        except FileNotFoundError:
            pass
    
    def get_settings(self):
        return {
            'on_duration': self.on_duration_spin.value() * 60,
            'off_duration': self.off_duration_spin.value() * 60,
            'cycles': self.cycles_spin.value()
        }
    
    def center_on_screen(self):
        # Get the screen where the cursor currently is
        screen = QApplication.screenAt(QCursor.pos())
        if not screen:
            screen = QApplication.primaryScreen()
        
        screen_geometry = screen.availableGeometry()
        dialog_geometry = self.frameGeometry()
        
        center_point = screen_geometry.center()
        dialog_geometry.moveCenter(center_point)
        self.move(dialog_geometry.topLeft())


class AlarmTrayApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        
        self.tray_icon = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_tick)
        
        self.is_running = False
        self.current_cycle = 0
        self.total_cycles = 0
        self.is_on_phase = True
        self.on_duration = 1200
        self.off_duration = 1200
        
        self.load_settings()
        self.setup_tray()
        
    def load_settings(self):
        try:
            with open('_config.json', 'r') as f:
                settings = json.load(f)
                self.on_duration = settings.get('on_duration', 1200)
                self.off_duration = settings.get('off_duration', 1200)
                self.total_cycles = settings.get('cycles', 0)
        except FileNotFoundError:
            pass
    
    def setup_tray(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, "System Tray", "System tray is not available on this system.")
            sys.exit(1)
        
        self.tray_icon = QSystemTrayIcon(self)
        self.update_tray_icon()
        
        menu = QMenu()
        
        self.start_stop_action = QAction("Start", self)
        self.start_stop_action.triggered.connect(self.toggle_alarm)
        menu.addAction(self.start_stop_action)
        
        settings_action = QAction("Change Settings", self)
        settings_action.triggered.connect(self.show_settings)
        menu.addAction(settings_action)
        
        menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit)
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()
    
    def update_tray_icon(self):
        if self.is_running:
            icon_path = "alarming_cycle_icon_on.png"
            tooltip = f"Alarm Running - Cycle {self.current_cycle}"
            if self.is_on_phase:
                tooltip += " (ON)"
            else:
                tooltip += " (OFF)"
        else:
            icon_path = "alarming_cycle_icon_off.png"
            tooltip = "Alarm Stopped"
        
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setToolTip(tooltip)
    
    def toggle_alarm(self):
        if self.is_running:
            self.stop_alarm()
        else:
            self.start_alarm()
    
    def start_alarm(self):
        self.is_running = True
        self.current_cycle = 0
        self.is_on_phase = True
        self.start_stop_action.setText("Stop")
        
        self.next_cycle()
        self.update_tray_icon()
    
    def stop_alarm(self):
        self.is_running = False
        self.timer.stop()
        self.start_stop_action.setText("Start")
        self.update_tray_icon()
    
    def next_cycle(self):
        if not self.is_running:
            return
        
        if self.is_on_phase:
            self.current_cycle += 1
            if self.total_cycles > 0 and self.current_cycle > self.total_cycles:
                self.alarm_complete()
                return
            
            print(f"Cycle {self.current_cycle}: ON for {self.on_duration} seconds.")
            self.play_sound_async(config.get_config_value("on_soundfx_path", ""))
            self.timer.start(self.on_duration * 1000)
        else:
            print(f"Cycle {self.current_cycle}: OFF for {self.off_duration} seconds.")
            self.play_sound_async(config.get_config_value("off_soundfx_path", ""))
            self.timer.start(self.off_duration * 1000)
        
        self.is_on_phase = not self.is_on_phase
        self.update_tray_icon()
    
    def timer_tick(self):
        self.timer.stop()
        self.next_cycle()
    
    def alarm_complete(self):
        print("Alarm cycles complete!")
        self.play_sound_async(config.get_config_value("end_soundfx_path", ""))
        self.stop_alarm()
    
    def play_sound_async(self, sound_path):
        if sound_path and os.path.exists(sound_path):
            subprocess.Popen(['pw-play', sound_path], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
    
    def show_settings(self):
        self.dummy_parent = QWidget()
        self.dummy_parent.setWindowFlags(Qt.WindowType.Tool)  # Optional: hides it from the taskbar
        self.dummy_parent.hide()
        dialog = SettingsDialog(parent=self.dummy_parent)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            settings = dialog.get_settings()
            self.on_duration = settings['on_duration']
            self.off_duration = settings['off_duration']
            self.total_cycles = settings['cycles']

if __name__ == "__main__":
    app = AlarmTrayApp(sys.argv)
    sys.exit(app.exec())
