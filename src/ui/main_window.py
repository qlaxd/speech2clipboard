import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTextEdit, QLabel, QStatusBar,
    QComboBox, QAction, QMessageBox, QShortcut, QApplication
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QKeySequence

class MainWindow(QMainWindow):
    """Main application window"""
    
    # Signal to communicate with audio recording thread
    start_recording_signal = pyqtSignal()
    stop_recording_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Window properties
        self.setWindowTitle("Hungarian Speech to Clipboard")
        self.resize(600, 400)
        
        # Create the central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Create UI components
        self._create_menu()
        self._create_toolbar()
        self._create_status_bar()
        self._create_main_ui()
        self._create_shortcuts()
        
        # Recording state
        self.is_recording = False
        self.recording_timer = QTimer(self)
        self.recording_timer.timeout.connect(self._update_recording_time)
        self.recording_time = 0

    def _create_menu(self):
        """Create the menu bar"""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("&Edit")
        
        # Copy action
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.setStatusTip("Copy transcription to clipboard")
        copy_action.triggered.connect(self.copy_to_clipboard)
        edit_menu.addAction(copy_action)
        
        # Clear action
        clear_action = QAction("C&lear", self)
        clear_action.setShortcut("Ctrl+L")
        clear_action.setStatusTip("Clear transcription")
        clear_action.triggered.connect(self.clear_transcription)
        edit_menu.addAction(clear_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        
        # About action
        about_action = QAction("&About", self)
        about_action.setStatusTip("About the application")
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_toolbar(self):
        """Create the toolbar"""
        toolbar = self.addToolBar("Recording")
        toolbar.setMovable(False)
        
        # Record button
        self.record_button = QAction("Record", self)
        self.record_button.setStatusTip("Start recording audio")
        self.record_button.triggered.connect(self.toggle_recording)
        toolbar.addAction(self.record_button)
        
        # Spacer
        spacer = QWidget()
        spacer.setSizePolicy(1, 0)
        toolbar.addWidget(spacer)
    
    def _create_status_bar(self):
        """Create the status bar"""
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        
        # Recording status label
        self.recording_status = QLabel("Ready")
        self.status_bar.addPermanentWidget(self.recording_status)
        
        # Timer label
        self.timer_label = QLabel("00:00")
        self.status_bar.addPermanentWidget(self.timer_label)
    
    def _create_main_ui(self):
        """Create the main UI components"""
        # Recording controls
        controls_layout = QHBoxLayout()
        
        self.record_btn = QPushButton("Record (F2)")
        self.record_btn.setMinimumHeight(50)
        self.record_btn.clicked.connect(self.toggle_recording)
        controls_layout.addWidget(self.record_btn)
        
        self.layout.addLayout(controls_layout)
        
        # Transcription text area
        self.transcription_label = QLabel("Transcription:")
        self.layout.addWidget(self.transcription_label)
        
        self.transcription_text = QTextEdit()
        self.transcription_text.setReadOnly(False)  # Allow editing
        self.layout.addWidget(self.transcription_text)
        
        # Clipboard button
        clipboard_layout = QHBoxLayout()
        
        self.clipboard_btn = QPushButton("Copy to Clipboard (Ctrl+C)")
        self.clipboard_btn.clicked.connect(self.copy_to_clipboard)
        clipboard_layout.addWidget(self.clipboard_btn)
        
        self.clear_btn = QPushButton("Clear (Ctrl+L)")
        self.clear_btn.clicked.connect(self.clear_transcription)
        clipboard_layout.addWidget(self.clear_btn)
        
        self.layout.addLayout(clipboard_layout)
    
    def _create_shortcuts(self):
        """Create keyboard shortcuts"""
        # F2 to start/stop recording
        self.record_shortcut = QShortcut(QKeySequence("F2"), self)
        self.record_shortcut.activated.connect(self.toggle_recording)
        
        # Ctrl+C to copy to clipboard
        self.copy_shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        self.copy_shortcut.activated.connect(self.copy_to_clipboard)
        
        # Ctrl+L to clear transcription
        self.clear_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        self.clear_shortcut.activated.connect(self.clear_transcription)
    
    def toggle_recording(self):
        """Toggle recording state"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording audio"""
        self.is_recording = True
        self.record_btn.setText("Stop (F2)")
        self.recording_status.setText("Recording...")
        self.status_bar.showMessage("Recording in progress...")
        
        # Start the timer
        self.recording_time = 0
        self.timer_label.setText("00:00")
        self.recording_timer.start(1000)  # Update every second
        
        # Emit signal to start recording
        self.start_recording_signal.emit()
    
    def stop_recording(self):
        """Stop recording audio"""
        self.is_recording = False
        self.record_btn.setText("Record (F2)")
        self.recording_status.setText("Processing...")
        self.status_bar.showMessage("Processing audio...")
        
        # Stop the timer
        self.recording_timer.stop()
        
        # Emit signal to stop recording
        self.stop_recording_signal.emit()
    
    def _update_recording_time(self):
        """Update the recording time display"""
        self.recording_time += 1
        minutes = self.recording_time // 60
        seconds = self.recording_time % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
    
    def set_transcription(self, text):
        """Set the transcription text"""
        self.transcription_text.setText(text)
        self.recording_status.setText("Ready")
        self.status_bar.showMessage("Transcription complete", 3000)
    
    def get_transcription(self):
        """Get the current transcription text"""
        return self.transcription_text.toPlainText()
    
    def copy_to_clipboard(self):
        """Copy the transcription to clipboard"""
        text = self.get_transcription()
        if text:
            # This will be implemented by connecting to ClipboardManager
            self.status_bar.showMessage("Copied to clipboard!", 3000)
    
    def clear_transcription(self):
        """Clear the transcription text area"""
        self.transcription_text.clear()
        self.status_bar.showMessage("Transcription cleared", 3000)
    
    def _show_about(self):
        """Show the about dialog"""
        QMessageBox.about(
            self,
            "About Hungarian Speech to Clipboard",
            "Hungarian Speech to Clipboard\n\n"
            "A tool to transcribe Hungarian speech to text "
            "and copy it to the clipboard.\n\n"
            "Version: 1.0.0"
        )
    
    def closeEvent(self, event):
        """Handle application close event"""
        if self.is_recording:
            self.stop_recording()
        event.accept() 