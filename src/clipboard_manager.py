import sys
import subprocess
import os

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
            # pyperclip.copy(text)
            # return True
            raise Exception("Skipping pyperclip")
        except Exception as e:
            print(f"Pyperclip error: {e}")
            
            # Fallback methods based on platform
            try:
                platform = sys.platform
                if platform == 'linux' or platform.startswith('linux'):
                    # Check for Wayland environment first
                    wayland_display = os.environ.get('WAYLAND_DISPLAY')
                    if wayland_display:
                        try:
                            # Wayland clipboard using wl-copy
                            process = subprocess.run(
                                ['wl-copy'],
                                input=text.encode('utf-8'),
                                check=True
                            )
                            return True
                        except Exception as wayland_err:
                            print(f"Wayland clipboard error: {wayland_err}")
                            # Continue to X11 fallbacks if wl-copy fails
                    
                    # Linux X11 fallback using xclip or xsel
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
            #return pyperclip.paste()
            raise Exception("Skipping pyperclip")
        except Exception as e:
            print(f"Error getting clipboard content: {e}")
            
            # Fallback methods based on platform
            try:
                platform = sys.platform
                if platform == 'linux' or platform.startswith('linux'):
                    # Check for Wayland environment first
                    wayland_display = os.environ.get('WAYLAND_DISPLAY')
                    if wayland_display:
                        try:
                            # Wayland clipboard using wl-paste
                            result = subprocess.run(
                                ['wl-paste'], 
                                stdout=subprocess.PIPE,
                                check=True
                            )
                            return result.stdout.decode()
                        except Exception as wayland_err:
                            print(f"Wayland clipboard paste error: {wayland_err}")
                            # Continue to X11 fallbacks if wl-paste fails
                
                # Add other platform fallbacks if needed
            
            except Exception as e2:
                print(f"Clipboard fallback error: {e2}")
            
            return "" 