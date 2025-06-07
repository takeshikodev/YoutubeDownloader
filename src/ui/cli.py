import logging
import time
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.box import DOUBLE, ROUNDED
from rich.theme import Theme
from rich.align import Align
from rich.table import Table

from ..config.config_manager import ConfigManager
from ..services.youtube_service import YouTubeService
from .prompts import (
    get_playlist_url_prompt,
    display_playlist_info_prompt,
    confirm_download_prompt,
    print_ffmpeg_instructions,
    get_user_input_with_default,
    show_progress_message,
    show_success_message,
    show_error_message
)

custom_theme = Theme({
    "info": "bright_cyan",
    "warning": "bright_yellow",
    "error": "bold bright_red",
    "success": "bold bright_green",
    "prompt": "bold bright_blue",
    "default": "bright_white",
    "accent": "bright_magenta",
    "highlight": "bold bright_yellow"
})

console = Console(theme=custom_theme)
logger = logging.getLogger(__name__)

class CLI:
    """Command line interface"""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.config = self.config_manager.config
        self.youtube_service = YouTubeService(self.config.dict())
        self._configure_logging()

    def _configure_logging(self):
        """Configures logging based on the application's configuration."""
        log_level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger.setLevel(log_level)

    def _show_welcome(self):
        """Shows a welcome screen."""
        title_art = Text()
        title_art.append("🎵 YouTube Music Downloader 🎵", style="bold bright_magenta")
        
        subtitle = Text()
        subtitle.append("Download your favorite YouTube music and playlists", style="italic bright_cyan")
        
        welcome_panel = Panel(
            Align.center(title_art + "\n" + subtitle),
            border_style="bright_magenta",
            box=DOUBLE,
            padding=(1, 2)
        )
        
        console.print(welcome_panel)
        console.print()

    def run(self):
        """Starts the CLI application"""
        self._show_welcome()
        
        print_ffmpeg_instructions()
        logger.info("Application started.")

        self._interactive_config_setup()

        playlist_url = get_playlist_url_prompt()
        if not playlist_url:
            show_error_message("No URL provided. Please restart the application.")
            return

        is_valid, message = self.youtube_service.validator.validate_url(playlist_url)
        if not is_valid:
            show_error_message(f"Invalid URL: {message}")
            return

        show_progress_message()
        
        playlist_info = self.youtube_service.get_playlist_info(playlist_url)

        if playlist_info:
            display_playlist_info_prompt(playlist_info)
            
            if confirm_download_prompt():
                download_panel = Panel(
                    Text.from_markup(
                        f"🚀 [bold bright_green]Starting Download[/bold bright_green]\n\n"
                        f"📁 Destination: [bold]{self.config.output_directory}[/bold]\n"
                        f"🎵 Quality: [bold]{self.config.audio_quality}[/bold]\n"
                        f"📊 Videos: [bold]{playlist_info.video_count}[/bold]"
                    ),
                    title="⬇️  Download Started",
                    border_style="bright_green",
                    box=ROUNDED
                )
                console.print(download_panel)
                
                self.youtube_service.download_playlist(playlist_url)
                show_success_message(self.config.output_directory)
            else:
                cancel_panel = Panel(
                    Text.from_markup("❌ [bold bright_yellow]Download Cancelled[/bold bright_yellow]\n\nNo files were downloaded."),
                    title="🛑 Cancelled",
                    border_style="bright_yellow",
                    box=ROUNDED
                )
                console.print(cancel_panel)
        else:
            show_error_message("Could not retrieve playlist information. Please check the URL and try again.")

        logger.info("Application finished.")
        
        goodbye_panel = Panel(
            Text.from_markup(
                "👋 [bold bright_cyan]Thank you for using YouTube Music Downloader![/bold bright_cyan]\n\n"
                "🎵 Enjoy your music! 🎵"
            ),
            title="✨ Goodbye",
            border_style="bright_cyan",
            box=ROUNDED
        )
        console.print(goodbye_panel)
        time.sleep(2)

    def _interactive_config_setup(self):
        """Allows user to override config settings."""
        
        config_header = Panel(
            Text.from_markup(
                "⚙️  [bold bright_blue]Configuration Setup[/bold bright_blue]\n\n"
                "Customize your download preferences below.\n"
                "Press Enter to use default values."
            ),
            title="🔧 Settings",
            border_style="bright_blue",
            box=ROUNDED
        )
        console.print(config_header)
        console.print()

        settings_table = Table(title="📋 Current Settings", box=ROUNDED)
        settings_table.add_column("Setting", style="bold bright_cyan")
        settings_table.add_column("Current Value", style="bright_yellow")
        settings_table.add_column("Description", style="bright_white")

        current_proxy = self.config.proxy_url if self.config.proxy_url else "None"
        settings_table.add_row("🌐 Proxy", current_proxy, "HTTP/SOCKS proxy for connections")
        
        proxy_input = get_user_input_with_default(
            f"🌐 [bold bright_blue]Proxy URL[/bold bright_blue] (current: [highlight]{current_proxy}[/highlight])",
            current_proxy
        )
        
        if proxy_input.lower() == "none" or not proxy_input:
            self.config_manager.update_config(proxy_url=None)
            logger.info("Proxy disabled by user.")
        elif proxy_input != current_proxy:
            if self.youtube_service.validator.validate_proxy_url(proxy_input):
                self.config_manager.update_config(proxy_url=proxy_input)
                logger.info(f"Proxy updated to: {proxy_input}")
                console.print(f"✅ [success]Proxy updated successfully![/success]")
            else:
                console.print(f"❌ [error]Invalid proxy URL format. Using previous setting.[/error]")
                logger.warning(f"Invalid proxy URL entered: {proxy_input}")

        console.print()

        current_output_dir = self.config.output_directory
        output_dir_input = get_user_input_with_default(
            f"📁 [bold bright_blue]Output Directory[/bold bright_blue] (current: [highlight]{current_output_dir}[/highlight])",
            current_output_dir
        )
        
        if output_dir_input != current_output_dir:
            self.config_manager.update_config(output_directory=output_dir_input)
            logger.info(f"Output directory updated to: {output_dir_input}")
            console.print(f"✅ [success]Output directory updated![/success]")

        console.print()

        current_audio_quality = self.config.audio_quality
        audio_quality_input = get_user_input_with_default(
            f"🎵 [bold bright_blue]Audio Quality[/bold bright_blue] (e.g., 128k, 320k, current: [highlight]{current_audio_quality}[/highlight])",
            current_audio_quality
        ).lower()
        
        try:
            temp_config = self.config_manager.config.copy(update={'audio_quality': audio_quality_input})
            self.config_manager.update_config(audio_quality=temp_config.audio_quality)
            logger.info(f"Audio quality updated to: {temp_config.audio_quality}")
            console.print(f"✅ [success]Audio quality updated![/success]")
        except ValueError as e:
            console.print(f"❌ [error]Invalid audio quality: {e}. Using previous setting.[/error]")
            logger.warning(f"Invalid audio quality entered: {audio_quality_input}. Error: {e}")

        console.print()

        current_display_progress_bar = "yes" if self.config.display_progress_bar else "no"
        display_progress_bar_input = get_user_input_with_default(
            f"📊 [bold bright_blue]Display Progress Bar[/bold bright_blue] (yes/no, current: [highlight]{current_display_progress_bar}[/highlight])",
            current_display_progress_bar
        ).lower()
        
        new_value = display_progress_bar_input in ['yes', 'y', 'да', '1', 'true']
        if new_value != self.config.display_progress_bar:
            self.config_manager.update_config(display_progress_bar=new_value)
            logger.info(f"Display progress bar set to: {new_value}")
            console.print(f"✅ [success]Progress bar setting updated![/success]")
        
        complete_panel = Panel(
            Text.from_markup("✅ [bold bright_green]Configuration Complete![/bold bright_green]\n\nReady to download music!"),
            title="🎉 Ready",
            border_style="bright_green",
            box=ROUNDED
        )
        console.print(complete_panel)
        console.print()