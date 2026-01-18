"""
Unified entry point for EON-OpenSlicer.
Automatically detects the platform and loads the appropriate UI framework.
- Desktop (Windows, Linux, macOS): Uses PyQt5
- Mobile (iOS, Android): Uses Toga
"""
import sys
import platform


def is_mobile_platform():
    """
    Detect if running on a mobile platform.
    Returns True for iOS and Android, False otherwise.
    """
    system = platform.system()
    
    # Check for Android
    if hasattr(sys, 'getandroidapilevel'):
        return True
    
    # Check for iOS
    if system == 'Darwin':
        # Check if running on iOS (not macOS)
        try:
            import ctypes.util
            foundation = ctypes.util.find_library('Foundation')
            if foundation and 'iPhoneOS' in platform.platform():
                return True
        except:
            pass
    
    # Check environment variables that mobile platforms might set
    if 'ANDROID_ROOT' in sys.prefix or 'ANDROID_DATA' in sys.prefix:
        return True
    
    return False


def main():
    """
    Main entry point that delegates to the appropriate UI framework.
    """
    if is_mobile_platform():
        # Import and run mobile version (Toga)
        print("Starting EON-OpenSlicer in mobile mode...")
        try:
            from app_mobile import main as mobile_main
            app = mobile_main()
            return app.main_loop()
        except ImportError as e:
            print(f"Error: Mobile dependencies not installed: {e}")
            print("Please install: pip install toga")
            sys.exit(1)
    else:
        # Import and run desktop version (PyQt5)
        print("Starting EON-OpenSlicer in desktop mode...")
        try:
            from main import main as desktop_main
            return desktop_main()
        except ImportError as e:
            print(f"Error: Desktop dependencies not installed: {e}")
            print("Please install: pip install -r requirements.txt")
            sys.exit(1)


if __name__ == "__main__":
    sys.exit(main() or 0)
