import pyperclip
import sys
import subprocess

class ClipboardManager:
    """
    Manages copying text to the system clipboard.
    Handles cross-platform clipboard operations.
    """
    
    @staticmethod
    def copy_to_clipboard(text):
        """
        Copy text to the system clipboard.
        
        Args:
            text: The text to copy to the clipboard
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Try the pyperclip library first (cross-platform)
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"Pyperclip error: {e}")
            
            # Fallback methods based on platform
            try:
                platform = sys.platform
                if platform == 'linux' or platform.startswith('linux'):
                    # Linux fallback using xclip or xsel
                    try:
                        process = subprocess.Popen(
                            ['xclip', '-selection', 'clipboard'],
                            stdin=subprocess.PIPE, close_fds=True
                        )
                        process.communicate(input=text.encode('utf-8'))
                        return True
                    except:
                        try:
                            process = subprocess.Popen(
                                ['xsel', '-ib'],
                                stdin=subprocess.PIPE, close_fds=True
                            )
                            process.communicate(input=text.encode('utf-8'))
                            return True
                        except:
                            return False
                
                elif platform == 'darwin':
                    # macOS fallback
                    process = subprocess.Popen(
                        ['pbcopy'],
                        stdin=subprocess.PIPE, close_fds=True
                    )
                    process.communicate(input=text.encode('utf-8'))
                    return True
                
                elif platform == 'win32':
                    # Windows fallback
                    subprocess.run(['clip'], input=text.encode('utf-8'), check=True)
                    return True
                
                return False
            
            except Exception as e2:
                print(f"Clipboard fallback error: {e2}")
                return False
    
    @staticmethod
    def get_from_clipboard():
        """
        Get text from the system clipboard.
        
        Returns:
            str: Text from clipboard or empty string if failed
        """
        try:
            return pyperclip.paste()
        except Exception as e:
            print(f"Error getting clipboard content: {e}")
            return "" 