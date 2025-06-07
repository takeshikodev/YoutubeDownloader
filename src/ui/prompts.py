import sys
import logging
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.box import ROUNDED, DOUBLE, HEAVY
from rich.prompt import Prompt, Confirm
from rich.theme import Theme
from rich.align import Align
from rich.table import Table
from ..models.playlist import PlaylistInfo

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

def print_ffmpeg_instructions():
    """Prints FFmpeg installation instructions based on the OS."""
    
    header = Text()
    header.append("⚠️  ", style="bright_yellow")
    header.append("FFmpeg Required", style="bold bright_yellow")
    header.append("  ⚠️", style="bright_yellow")
    
    content = Text()
    content.append("FFmpeg is essential for audio extraction and MP3 conversion.\n", style="bright_white")
    content.append("Without it, downloads will fail completely.", style="italic bright_red")
    
    console.print(Panel(
        Align.center(content),
        title=header,
        border_style="bright_yellow",
        box=ROUNDED,
        padding=(1, 2)
    ))
    
    console.print()
    
    if sys.platform.startswith('win'):
        windows_panel = Panel(
            Text.from_markup(
                "🪟 [bold bright_blue]Windows Installation:[/bold bright_blue]\n\n"
                "1. Visit [link=https://ffmpeg.org]https://ffmpeg.org[/link]\n"
                "2. Download the Windows build\n"
                "3. Extract to a folder (e.g., C:\\ffmpeg)\n"
                "4. Add the 'bin' folder to your PATH environment variable\n"
                "5. Restart your terminal/command prompt"
            ),
            title="🔧 Installation Guide",
            border_style="bright_blue",
            box=ROUNDED
        )
        console.print(windows_panel)
        
    elif sys.platform.startswith('darwin'): # macOS
        macos_panel = Panel(
            Text.from_markup(
                "🍎 [bold bright_blue]macOS Installation:[/bold bright_blue]\n\n"
                "Using Homebrew (recommended):\n"
                "[bright_green]brew install ffmpeg[/bright_green]\n\n"
                "If you don't have Homebrew:\n"
                "Visit [link=https://brew.sh]https://brew.sh[/link] first"
            ),
            title="🔧 Installation Guide",
            border_style="bright_blue",
            box=ROUNDED
        )
        console.print(macos_panel)
        
    else: # Linux
        linux_panel = Panel(
            Text.from_markup(
                "🐧 [bold bright_blue]Linux Installation:[/bold bright_blue]\n\n"
                "Debian/Ubuntu:\n"
                "[bright_green]sudo apt update && sudo apt install ffmpeg[/bright_green]\n\n"
                "Red Hat/CentOS/Fedora:\n"
                "[bright_green]sudo dnf install ffmpeg[/bright_green]\n\n"
                "Arch Linux:\n"
                "[bright_green]sudo pacman -S ffmpeg[/bright_green]"
            ),
            title="🔧 Installation Guide",
            border_style="bright_blue",
            box=ROUNDED
        )
        console.print(linux_panel)
    
    console.print()

def get_user_input_with_default(prompt_message: str, default_value: str = None) -> str:
    """Gets user input with an optional default value using Rich Prompt."""
    return Prompt.ask(
        Text.from_markup(prompt_message),
        default=default_value,
        console=console
    )

def get_playlist_url_prompt() -> str:
    """Asks the user for the YouTube playlist URL."""
    
    url_panel = Panel(
        Text.from_markup(
            "🎵 [bold bright_magenta]Enter YouTube Content[/bold bright_magenta]\n\n"
            "Supported formats:\n"
            "• Playlist URLs\n"
            "• Individual video URLs\n"
            "• Channel URLs\n"
            "• YouTube Music playlists"
        ),
        title="📥 Input Required",
        border_style="bright_magenta",
        box=ROUNDED
    )
    console.print(url_panel)
    
    return Prompt.ask(
        "[bold bright_blue]🔗 YouTube URL[/bold bright_blue]",
        console=console
    )

def format_duration(seconds: int) -> str:
    """Format duration in seconds to human readable format."""
    if not seconds:
        return "Unknown"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def display_playlist_info_prompt(playlist_info: PlaylistInfo):
    """Displays playlist information to the user."""
    
    info_table = Table(show_header=False, padding=(0, 1), expand=True)
    info_table.add_column("Field", style="bold bright_cyan", width=18)
    info_table.add_column("Value", style="bright_white")
    
    info_table.add_row("🎵 Title:", f"[bold]{playlist_info.title}[/bold]")
    info_table.add_row("👤 Uploader:", f"[bold]{playlist_info.uploader or 'Unknown'}[/bold]")
    info_table.add_row("📊 Total Videos:", f"[bold bright_green]{playlist_info.video_count}[/bold bright_green]")
    info_table.add_row("⏱️  Duration:", f"[bold bright_yellow]{playlist_info.get_formatted_duration()}[/bold bright_yellow]")
    
    if playlist_info.description:
        description = playlist_info.description.splitlines()[0][:80] + '...' if len(playlist_info.description) > 80 else playlist_info.description.splitlines()[0]
        info_table.add_row("📝 Description:", f"[italic]{description}[/italic]")
    else:
        info_table.add_row("📝 Description:", "[dim]No description available[/dim]")
    
    console.print(Panel(
        info_table,
        title="🎼 [bold bright_green]Playlist Information[/bold bright_green] 🎼",
        border_style="bright_green",
        box=ROUNDED,
        padding=(1, 2)
    ))
    
    if playlist_info.videos and len(playlist_info.videos) > 0:
        console.print()
        sample_text = Text()
        sample_text.append("📋 Sample Videos:\n", style="bold bright_cyan")
        
        for i, video in enumerate(playlist_info.videos[:3]):
            duration_str = f" ({format_duration(video.duration)})" if video.duration else ""
            sample_text.append(f"  {i+1}. {video.title}{duration_str}\n", style="bright_white")
        
        if len(playlist_info.videos) > 3:
            sample_text.append(f"  ... and {len(playlist_info.videos) - 3} more videos", style="dim")
        
        console.print(Panel(
            sample_text,
            border_style="bright_blue",
            box=ROUNDED
        ))

def confirm_download_prompt() -> bool:
    """Asks the user for confirmation to start the download."""
    
    console.print()
    
    confirm_panel = Panel(
        Text.from_markup(
            "🚀 [bold bright_yellow]Ready to Download?[/bold bright_yellow]\n\n"
            "The download process will begin and may take some time\n"
            "depending on the number of videos and your internet speed."
        ),
        title="⚡ Confirmation",
        border_style="bright_yellow",
        box=ROUNDED
    )
    console.print(confirm_panel)
    
    return Confirm.ask(
        "[bold bright_green]🎯 Start downloading now?[/bold bright_green]",
        default=True,
        console=console,
        show_default=True
    )

def show_progress_message():
    """Shows a progress message."""
    progress_panel = Panel(
        Text.from_markup(
            "⏳ [bold bright_cyan]Processing...[/bold bright_cyan]\n\n"
            "Fetching playlist information from YouTube.\n"
            "This may take a few moments for large playlists."
        ),
        title="🔄 Please Wait",
        border_style="bright_cyan",
        box=ROUNDED
    )
    console.print(progress_panel)

def show_success_message(output_dir: str):
    """Shows a success message."""
    success_panel = Panel(
        Text.from_markup(
            f"✅ [bold bright_green]Download Complete![/bold bright_green]\n\n"
            f"📁 Files saved to: [bold]{output_dir}[/bold]\n"
            f"🎉 Enjoy your music!"
        ),
        title="🎊 Success",
        border_style="bright_green",
        box=DOUBLE
    )
    console.print(success_panel)

def show_error_message(error: str):
    """Shows a error message."""
    error_panel = Panel(
        Text.from_markup(
            f"❌ [bold bright_red]Error Occurred[/bold bright_red]\n\n"
            f"💥 {error}\n\n"
            f"Please check your connection and try again."
        ),
        title="⚠️  Error",
        border_style="bright_red",
        box=HEAVY
    )
    console.print(error_panel)