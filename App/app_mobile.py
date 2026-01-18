"""
Mobile entry point for EON-OpenSlicer.
This module provides a simplified mobile interface using Toga.
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import sys
import platform


class EONOpenSlicerMobile(toga.App):
    def startup(self):
        """
        Construct and show the Toga application.
        For mobile platforms (iOS/Android), we provide a simplified interface
        focused on viewing print jobs, monitoring status, and basic controls.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        
        # Title
        title_label = toga.Label(
            'EON-OpenSlicer Mobile',
            style=Pack(padding=5, font_size=20, font_weight='bold')
        )
        main_box.add(title_label)
        
        # Info label
        info_label = toga.Label(
            'Mobile version - View and monitor print jobs',
            style=Pack(padding=5)
        )
        main_box.add(info_label)
        
        # Create tabs for different views
        job_view = self.create_job_view()
        status_view = self.create_status_view()
        settings_view = self.create_settings_view()
        
        # Add buttons for navigation
        button_box = toga.Box(style=Pack(direction=ROW, padding=5))
        
        jobs_button = toga.Button(
            'Print Jobs',
            on_press=self.show_jobs,
            style=Pack(padding=5, flex=1)
        )
        status_button = toga.Button(
            'Status',
            on_press=self.show_status,
            style=Pack(padding=5, flex=1)
        )
        settings_button = toga.Button(
            'Settings',
            on_press=self.show_settings,
            style=Pack(padding=5, flex=1)
        )
        
        button_box.add(jobs_button)
        button_box.add(status_button)
        button_box.add(settings_button)
        
        main_box.add(button_box)
        
        # Content area
        self.content_box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        self.content_box.add(job_view)
        main_box.add(self.content_box)
        
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
    
    def create_job_view(self):
        """Create the print jobs view"""
        view = toga.Box(style=Pack(direction=COLUMN, padding=5))
        
        label = toga.Label(
            'Print Jobs',
            style=Pack(padding=5, font_size=16, font_weight='bold')
        )
        view.add(label)
        
        info = toga.Label(
            'No active print jobs.\n\nConnect to the server to view and manage print jobs.',
            style=Pack(padding=5)
        )
        view.add(info)
        
        # Add a button to refresh
        refresh_button = toga.Button(
            'Refresh Jobs',
            on_press=self.refresh_jobs,
            style=Pack(padding=5)
        )
        view.add(refresh_button)
        
        return view
    
    def create_status_view(self):
        """Create the status view"""
        view = toga.Box(style=Pack(direction=COLUMN, padding=5))
        
        label = toga.Label(
            'Printer Status',
            style=Pack(padding=5, font_size=16, font_weight='bold')
        )
        view.add(label)
        
        info = toga.Label(
            'No printers connected.\n\nConnect to view printer status and monitoring.',
            style=Pack(padding=5)
        )
        view.add(info)
        
        return view
    
    def create_settings_view(self):
        """Create the settings view"""
        view = toga.Box(style=Pack(direction=COLUMN, padding=5))
        
        label = toga.Label(
            'Settings',
            style=Pack(padding=5, font_size=16, font_weight='bold')
        )
        view.add(label)
        
        # Server URL input
        url_label = toga.Label('Server URL:', style=Pack(padding=5))
        view.add(url_label)
        
        self.url_input = toga.TextInput(
            placeholder='http://server:port',
            style=Pack(padding=5)
        )
        view.add(self.url_input)
        
        # Connect button
        connect_button = toga.Button(
            'Connect to Server',
            on_press=self.connect_server,
            style=Pack(padding=5)
        )
        view.add(connect_button)
        
        return view
    
    def show_jobs(self, widget):
        """Show print jobs view"""
        self.content_box.clear()
        self.content_box.add(self.create_job_view())
    
    def show_status(self, widget):
        """Show status view"""
        self.content_box.clear()
        self.content_box.add(self.create_status_view())
    
    def show_settings(self, widget):
        """Show settings view"""
        self.content_box.clear()
        self.content_box.add(self.create_settings_view())
    
    def refresh_jobs(self, widget):
        """Refresh print jobs"""
        self.main_window.info_dialog(
            'Refresh',
            'Jobs refreshed (demo - connect to server for real data)'
        )
    
    def connect_server(self, widget):
        """Connect to server"""
        url = self.url_input.value
        if url:
            self.main_window.info_dialog(
                'Connect',
                f'Connecting to {url}\n(demo - implement server connection)'
            )
        else:
            self.main_window.error_dialog(
                'Error',
                'Please enter a server URL'
            )


def main():
    """Main entry point for mobile app"""
    return EONOpenSlicerMobile(
        'EON-OpenSlicer',
        'edu.uc.eon_openslicer'
    )


if __name__ == '__main__':
    main().main_loop()
