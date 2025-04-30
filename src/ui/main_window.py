import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTextEdit, QLabel, QStatusBar,
    QComboBox, QAction, QMessageBox, QShortcut, QApplication,
    QFrame, QSizePolicy, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QKeySequence, QFont, QColor, QPalette, QPixmap

class StyleHelper:
    """Helper class for UI styling"""
    
    # Color palette
    PRIMARY_COLOR = "#2979ff"  # Blue
    SECONDARY_COLOR = "#455a64"  # Dark bluish gray
    ACCENT_COLOR = "#f44336"  # Red for recording
    BACKGROUND_COLOR = "#f5f5f5"  # Light gray
    TEXT_COLOR = "#212121"  # Almost black
    LIGHT_TEXT = "#ffffff"  # White
    
    @staticmethod
    def set_button_style(button, primary=True, accent=False):
        """Apply custom style to button"""
        if accent:
            color = StyleHelper.ACCENT_COLOR
            text_color = StyleHelper.LIGHT_TEXT
        elif primary:
            color = StyleHelper.PRIMARY_COLOR
            text_color = StyleHelper.LIGHT_TEXT
        else:
            color = StyleHelper.SECONDARY_COLOR
            text_color = StyleHelper.LIGHT_TEXT
        
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: {text_color};
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
            QPushButton:pressed {{
                background-color: {color}aa;
            }}
        """)
    
    @staticmethod
    def set_text_area_style(text_edit):
        """Apply custom style to text edit"""
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 8px;
                selection-background-color: {StyleHelper.PRIMARY_COLOR}80;
            }}
        """)
        
        # Set font
        font = QFont("Arial", 10)
        text_edit.setFont(font)
    
    @staticmethod
    def set_frame_style(frame):
        """Apply custom style to frame"""
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }}
        """)
    
    @staticmethod
    def set_label_style(label, heading=False):
        """Apply custom style to label"""
        if heading:
            label.setStyleSheet(f"""
                QLabel {{
                    color: {StyleHelper.SECONDARY_COLOR};
                    font-weight: bold;
                    font-size: 14px;
                }}
            """)
        else:
            label.setStyleSheet(f"""
                QLabel {{
                    color: {StyleHelper.TEXT_COLOR};
                }}
            """)

class MainWindow(QMainWindow):
    """Main application window"""
    
    # Signal to communicate with audio recording thread
    start_recording_signal = pyqtSignal()
    stop_recording_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Window properties
        self.setWindowTitle("Hungarian Speech to Clipboard")
        self.resize(700, 500)
        
        # Set application style
        self._set_application_style()
        
        # Create the central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
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
    
    def _set_application_style(self):
        """Set global application style"""
        # Set application palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(StyleHelper.BACKGROUND_COLOR))
        palette.setColor(QPalette.WindowText, QColor(StyleHelper.TEXT_COLOR))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.Text, QColor(StyleHelper.TEXT_COLOR))
        palette.setColor(QPalette.Button, QColor(StyleHelper.BACKGROUND_COLOR))
        palette.setColor(QPalette.ButtonText, QColor(StyleHelper.TEXT_COLOR))
        palette.setColor(QPalette.Link, QColor(StyleHelper.PRIMARY_COLOR))
        palette.setColor(QPalette.Highlight, QColor(StyleHelper.PRIMARY_COLOR))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        self.setPalette(palette)
        
        # Set window style
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {StyleHelper.BACKGROUND_COLOR};
            }}
            QStatusBar {{
                background-color: {StyleHelper.SECONDARY_COLOR};
                color: {StyleHelper.LIGHT_TEXT};
            }}
            QMenuBar {{
                background-color: {StyleHelper.SECONDARY_COLOR};
                color: {StyleHelper.LIGHT_TEXT};
            }}
            QMenuBar::item:selected {{
                background-color: {StyleHelper.PRIMARY_COLOR};
            }}
            QMenu {{
                background-color: {StyleHelper.SECONDARY_COLOR};
                color: {StyleHelper.LIGHT_TEXT};
                border: 1px solid #cccccc;
            }}
            QMenu::item:selected {{
                background-color: {StyleHelper.PRIMARY_COLOR};
            }}
            QToolBar {{
                background-color: {StyleHelper.SECONDARY_COLOR};
                border-bottom: 1px solid #cccccc;
                spacing: 5px;
            }}
            QToolButton {{
                background-color: transparent;
                color: {StyleHelper.LIGHT_TEXT};
                border: none;
                padding: 5px;
            }}
            QToolButton:hover {{
                background-color: {StyleHelper.PRIMARY_COLOR};
                border-radius: 4px;
            }}
        """)

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
        self.record_action = QAction("Record", self)
        self.record_action.setStatusTip("Start recording audio")
        self.record_action.triggered.connect(self.toggle_recording)
        toolbar.addAction(self.record_action)
        
        # Spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
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
        self.timer_label.setStyleSheet("padding-right: 10px;")
        self.status_bar.addPermanentWidget(self.timer_label)
    
    def _create_main_ui(self):
        """Create the main UI components"""
        # App title and description
        header_layout = QVBoxLayout()
        
        title_label = QLabel("Hungarian Speech to Clipboard")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2979ff;
            margin-bottom: 5px;
        """)
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Record speech, convert to text, and copy to clipboard")
        subtitle_label.setStyleSheet("""
            font-size: 14px;
            color: #455a64;
            margin-bottom: 15px;
        """)
        header_layout.addWidget(subtitle_label)
        
        # Add a separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0;")
        
        self.layout.addLayout(header_layout)
        self.layout.addWidget(separator)
        
        # Recording controls
        controls_layout = QHBoxLayout()
        
        # Recording visualization frame
        self.visualization_frame = QFrame()
        self.visualization_frame.setFrameShape(QFrame.StyledPanel)
        self.visualization_frame.setMinimumHeight(60)
        self.visualization_frame.setMaximumHeight(60)
        StyleHelper.set_frame_style(self.visualization_frame)
        
        # Status indicator
        self.status_indicator = QProgressBar()
        self.status_indicator.setRange(0, 100)
        self.status_indicator.setValue(0)
        self.status_indicator.setTextVisible(False)
        self.status_indicator.setStyleSheet("""
            QProgressBar {
                background-color: #f5f5f5;
                border: none;
                border-radius: 4px;
                height: 5px;
            }
            QProgressBar::chunk {
                background-color: #2979ff;
                border-radius: 4px;
            }
        """)
        
        viz_layout = QVBoxLayout(self.visualization_frame)
        viz_layout.addWidget(QLabel("Recording status:"))
        viz_layout.addWidget(self.status_indicator)
        
        controls_layout.addWidget(self.visualization_frame)
        
        self.record_btn = QPushButton("Record (F2)")
        self.record_btn.setMinimumHeight(60)
        self.record_btn.setIconSize(QSize(24, 24))
        self.record_btn.clicked.connect(self.toggle_recording)
        StyleHelper.set_button_style(self.record_btn, accent=True)
        controls_layout.addWidget(self.record_btn)
        
        self.layout.addLayout(controls_layout)
        
        # Transcription text area
        self.transcription_label = QLabel("Transcription:")
        StyleHelper.set_label_style(self.transcription_label, heading=True)
        self.layout.addWidget(self.transcription_label)
        
        self.transcription_text = QTextEdit()
        self.transcription_text.setReadOnly(False)  # Allow editing
        self.transcription_text.setMinimumHeight(150)
        StyleHelper.set_text_area_style(self.transcription_text)
        self.layout.addWidget(self.transcription_text)
        
        # Clipboard button
        clipboard_layout = QHBoxLayout()
        
        self.clipboard_btn = QPushButton("Copy to Clipboard (Ctrl+C)")
        self.clipboard_btn.clicked.connect(self.copy_to_clipboard)
        StyleHelper.set_button_style(self.clipboard_btn)
        clipboard_layout.addWidget(self.clipboard_btn)
        
        self.clear_btn = QPushButton("Clear (Ctrl+L)")
        self.clear_btn.clicked.connect(self.clear_transcription)
        StyleHelper.set_button_style(self.clear_btn, primary=False)
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
        self.record_btn.setText("Stop Recording (F2)")
        StyleHelper.set_button_style(self.record_btn, accent=True)
        self.recording_status.setText("Recording...")
        self.status_bar.showMessage("Recording in progress...")
        
        # Update status indicator
        self._animate_recording()
        
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
        StyleHelper.set_button_style(self.record_btn, accent=False)
        self.recording_status.setText("Processing...")
        self.status_bar.showMessage("Processing audio...")
        
        # Update status indicator
        self.status_indicator.setValue(0)
        self.status_indicator.setStyleSheet("""
            QProgressBar {
                background-color: #f5f5f5;
                border: none;
                border-radius: 4px;
                height: 5px;
            }
            QProgressBar::chunk {
                background-color: #2979ff;
                border-radius: 4px;
            }
        """)
        
        # Stop the timer
        self.recording_timer.stop()
        
        # Emit signal to stop recording
        self.stop_recording_signal.emit()
    
    def _animate_recording(self):
        """Animate the recording indicator"""
        # Update status indicator style to indicate recording
        self.status_indicator.setStyleSheet("""
            QProgressBar {
                background-color: #f5f5f5;
                border: none;
                border-radius: 4px;
                height: 8px;
            }
            QProgressBar::chunk {
                background-color: #f44336;
                border-radius: 4px;
            }
        """)
        
        # Start animation
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._update_animation)
        self.animation_timer.start(50)  # Update every 50ms
    
    def _update_animation(self):
        """Update the animation for recording visualization"""
        if not self.is_recording:
            self.animation_timer.stop()
            return
            
        # Simple bouncing animation
        current = self.status_indicator.value()
        if current >= 100:
            self.animation_direction = -1
        elif current <= 0:
            self.animation_direction = 1
            
        self.status_indicator.setValue(current + self.animation_direction * 5)
    
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