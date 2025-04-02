#!/usr/bin/env python3
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QComboBox, QCheckBox,
    QProgressBar, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSlot
from PyQt6.QtGui import QIcon, QFont, QPixmap

from downloader import DownloadWorker, clean_youtube_url

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class YouTubeDownloaderUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlanYD")
        self.setMinimumSize(600, 500)
        self.setWindowIcon(QIcon(resource_path("FlanYDLogo.ico")))
        
        # Initialize variables
        self.url_list = []
        self.current_download_index = 0
        self.download_thread = None
        self.download_worker = None
        self.is_downloading = False
        self.keep_video = True

        # Set up the UI
        self.init_ui()
    
    def init_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add logo and title at the top
        header_layout = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(resource_path("FlanYDLogo.png"))
        logo_pixmap = logo_pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setFixedSize(48, 48)
        
        # Title
        title_label = QLabel("FlanYD")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        # Add separator after header
        header_separator = QFrame()
        header_separator.setFrameShape(QFrame.Shape.HLine)
        header_separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(header_separator)
        
        # URL input section
        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL...")
        self.url_input.returnPressed.connect(self.add_url)
        
        add_button = QPushButton("+")
        add_button.setFixedSize(30, 30)
        add_button.clicked.connect(self.add_url)
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input, 1)
        url_layout.addWidget(add_button)
        
        main_layout.addLayout(url_layout)
        
        # URL list section
        list_label = QLabel("Added URLs:")
        main_layout.addWidget(list_label)
        
        self.url_list_widget = QListWidget()
        self.url_list_widget.setAlternatingRowColors(True)
        self.url_list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.url_list_widget.setMinimumHeight(150)
        main_layout.addWidget(self.url_list_widget)
        
        # URL list buttons
        list_buttons_layout = QHBoxLayout()
        
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected_url)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_url_list)
        
        list_buttons_layout.addWidget(self.remove_button)
        list_buttons_layout.addWidget(self.clear_button)
        list_buttons_layout.addStretch()

        self.keep_video_checkbox = QCheckBox("Keep Video")
        self.keep_video_checkbox.setChecked(True)
        self.keep_video_checkbox.stateChanged.connect(self.set_keep_video)
        list_buttons_layout.addWidget(self.keep_video_checkbox)
        
        format_label = QLabel("Format:")
        list_buttons_layout.addWidget(format_label)
        self.format_dropdown = QComboBox()
        self.format_dropdown.addItems(["any", "mp4", "mp3", "wav"])
        self.format_dropdown.setCurrentText("any")
        list_buttons_layout.addWidget(self.format_dropdown)
        
        
        main_layout.addLayout(list_buttons_layout)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)
        
        # Download controls
        controls_layout = QHBoxLayout()
        
        self.download_button = QPushButton("Download All")
        self.download_button.clicked.connect(self.start_download)
        self.download_button.setMinimumHeight(40)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_download)
        self.cancel_button.setEnabled(False)
        self.cancel_button.setMinimumHeight(40)
        
        controls_layout.addWidget(self.download_button)
       
        controls_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(controls_layout)
        
        # Current download progress
        current_label = QLabel("Current download:")
        main_layout.addWidget(current_label)
        
        current_progress_layout = QHBoxLayout()
        self.current_progress_bar = QProgressBar()
        self.current_progress_bar.setRange(0, 100)
        self.current_progress_bar.setValue(0)
        self.current_progress_bar.setTextVisible(True)
        self.current_progress_bar.setFormat("%p%")
        
        self.current_file_label = QLabel("")
        
        current_progress_layout.addWidget(self.current_progress_bar)
        current_progress_layout.addWidget(self.current_file_label)
        
        main_layout.addLayout(current_progress_layout)
        
        # Overall progress
        overall_label = QLabel("Overall progress:")
        main_layout.addWidget(overall_label)
        
        overall_progress_layout = QHBoxLayout()
        self.overall_progress_bar = QProgressBar()
        self.overall_progress_bar.setRange(0, 100)
        self.overall_progress_bar.setValue(0)
        self.overall_progress_bar.setTextVisible(True)
        
        self.overall_status_label = QLabel("")
        
        overall_progress_layout.addWidget(self.overall_progress_bar)
        overall_progress_layout.addWidget(self.overall_status_label)
        
        main_layout.addLayout(overall_progress_layout)
        
        # Status bar at the bottom
        self.statusBar().showMessage("Ready")
    
    def add_url(self):
        url = self.url_input.text().strip()
        if not url:
            return
            
        # Basic validation - check if it looks like a YouTube URL
        if "youtube.com" not in url and "youtu.be" not in url:
            QMessageBox.warning(self, "Invalid URL", "Please enter a valid YouTube URL.")
            return
        
        # Clean the URL to remove unnecessary parameters
        clean_url = clean_youtube_url(url)
            
        # Add to our internal list and the list widget
        if clean_url not in self.url_list:
            self.url_list.append(clean_url)
            self.url_list_widget.addItem(clean_url)
            self.url_input.clear()
            self.update_ui_state()
    
    def remove_selected_url(self):
        selected_items = self.url_list_widget.selectedItems()
        if not selected_items:
            return
            
        for item in selected_items:
            url = item.text()
            row = self.url_list_widget.row(item)
            self.url_list_widget.takeItem(row)
            if url in self.url_list:
                self.url_list.remove(url)
                
        self.update_ui_state()
    
    def clear_url_list(self):
        self.url_list.clear()
        self.url_list_widget.clear()
        self.update_ui_state()
    
    def update_ui_state(self):
        has_urls = len(self.url_list) > 0
        self.download_button.setEnabled(has_urls and not self.is_downloading)
        self.remove_button.setEnabled(has_urls and not self.is_downloading)
        self.clear_button.setEnabled(has_urls and not self.is_downloading)
        self.cancel_button.setEnabled(self.is_downloading)
        self.url_input.setEnabled(not self.is_downloading)
    
    def set_keep_video(self, state):
        self.keep_video = state == Qt.CheckState.Checked
    
    def start_download(self):
        if not self.url_list:
            return
            
        self.is_downloading = True
        self.current_download_index = 0
        self.update_ui_state()
        
        # Reset progress bars
        self.current_progress_bar.setValue(0)
        self.overall_progress_bar.setValue(0)
        self.current_file_label.setText("")
        self.overall_status_label.setText(f"(0/{len(self.url_list)} videos)")
        
        # Start the download process
        self.download_next_video()
    
    def download_next_video(self):
        if self.current_download_index >= len(self.url_list):
            # All downloads completed
            self.is_downloading = False
            self.update_ui_state()
            self.statusBar().showMessage("All downloads completed")
            return
            
        # Get the next URL to download
        url = self.url_list[self.current_download_index]
        self.statusBar().showMessage(f"Downloading: {url}")
        
        # Create worker and thread
        self.download_worker = DownloadWorker()
        self.download_thread = QThread()
        self.download_worker.moveToThread(self.download_thread)
        
        # Connect signals
        self.download_thread.started.connect(lambda: self.download_worker.download_video(url, self.format_dropdown.currentText(), self.keep_video))
        self.download_worker.progress_changed.connect(self.update_progress)
        self.download_worker.download_finished.connect(self.on_download_finished)
        
        # Start the thread
        self.download_thread.start()
    
    @pyqtSlot(str, float, dict)
    def update_progress(self, url, progress, info_dict):
        # Update current download progress
        self.current_progress_bar.setValue(int(progress))
        
        # Show the filename
        title = info_dict.get('title', 'Unknown')
        self.current_file_label.setText(title)
        
        # Update overall progress
        total_progress = ((self.current_download_index + progress/100) / len(self.url_list)) * 100
        self.overall_progress_bar.setValue(int(total_progress))
        self.overall_status_label.setText(f"({self.current_download_index+1}/{len(self.url_list)} videos)")
    
    @pyqtSlot(str, bool, str)
    def on_download_finished(self, url, success, message):
        # Clean up thread and worker
        if self.download_thread:
            self.download_thread.quit()
            self.download_thread.wait()
        
        # Update status
        self.statusBar().showMessage(message)
        
        # Show error message if download failed
        if not success:
            if not message.startswith("Download cancelled"):
                QMessageBox.critical(self, "Download Error", f"Failed to download: {url}\n\n{message}")
            else:
                self.statusBar().showMessage("Download cancelled")
        
        # Move to next download
        self.current_download_index += 1
        
        # Update overall progress
        overall_percent = (self.current_download_index / len(self.url_list)) * 100
        self.overall_progress_bar.setValue(int(overall_percent))
        self.overall_status_label.setText(f"({self.current_download_index}/{len(self.url_list)} videos)")
        
        # Continue with next download if not cancelled
        if self.is_downloading:
            self.download_next_video()
    
    def cancel_download(self):
        if self.download_worker:
            self.download_worker.cancel()
        
        self.statusBar().showMessage("Download cancelled")
        self.is_downloading = False
        self.update_ui_state()
    
    def closeEvent(self, event):
        # Cancel any ongoing downloads before closing
        if self.is_downloading and self.download_worker:
            self.download_worker.cancel()
            if self.download_thread:
                self.download_thread.quit()
                self.download_thread.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use Fusion style for a consistent look
    
    try:
        # Check if resources exist
        icon_path = resource_path("FlanYDLogo.ico")
        logo_path = resource_path("FlanYDLogo.png")
        
        if not os.path.exists(icon_path) or not os.path.exists(logo_path):
            QMessageBox.warning(None, "Resource Warning", 
                               f"Some resources could not be found:\n"
                               f"{'Icon missing' if not os.path.exists(icon_path) else ''}\n"
                               f"{'Logo missing' if not os.path.exists(logo_path) else ''}\n\n"
                               f"The application will still run, but some visual elements may be missing.")
        
        window = YouTubeDownloaderUI()
        window.show()
        
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Startup Error", 
                           f"An error occurred while starting the application:\n\n{str(e)}")
        sys.exit(1)
