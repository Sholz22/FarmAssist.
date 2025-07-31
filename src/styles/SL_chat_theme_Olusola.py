import streamlit as st
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class ThemeConfig:
    """Configuration class for theme customization."""
    primary_color: str = "#026607"
    secondary_color: str = "#035509"
    accent_color: str = "#014405"
    background_light: str = "#f8f9fa"
    background_dark: str = "#e9ecef"
    text_color: str = "#333"
    border_radius: str = "15px"
    button_radius: str = "25px"
    shadow_color: str = "rgba(2, 102, 7, 0.3)"
    # New background image properties
    background_image_url: Optional[str] = None
    background_opacity: float = 0.1
    background_size: str = "cover"
    background_position: str = "center"
    background_repeat: str = "no-repeat"
    background_attachment: str = "fixed"

class StreamlitChatTheme:
    """A reusable CSS theme class for Streamlit chat applications."""
    
    def __init__(self, config: Optional[ThemeConfig] = None):
        """Initialize the theme with custom configuration."""
        self.config = config or ThemeConfig()
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def apply_theme(self, hide_streamlit_branding: bool = True) -> None:
        """Apply the complete theme to the Streamlit app."""
        css = self._build_css(hide_streamlit_branding)
        st.markdown(css, unsafe_allow_html=True)
    
    def _build_css(self, hide_branding: bool) -> str:
        """Build the complete CSS string."""
        css_parts = []
        
        if hide_branding:
            css_parts.append(self._get_branding_css())
        
        css_parts.extend([
            self._get_background_css(),
            self._get_main_container_css(),
            self._get_chat_message_css(),
            self._get_form_css(),
            self._get_button_css(),
            self._get_title_css(),
            self._get_tab_css(),
            self._get_file_uploader_css(),
            self._get_responsive_css()
        ])
        
        return f"<style>{''.join(css_parts)}</style>"
    
    def _get_branding_css(self) -> str:
        """CSS to hide Streamlit branding."""
        return """
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        """
    
    def _get_background_css(self) -> str:
        """CSS for background image styling."""
        if not self.config.background_image_url:
            return ""
        
        # Extract RGB values from primary color for green overlay
        primary_rgb = self._hex_to_rgb(self.config.primary_color)
        
        return f"""
        /* Background image styling */
        .stApp {{
            background: linear-gradient(
                rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, {1 - self.config.background_opacity}),
                rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, {1 - self.config.background_opacity})
            ), url('{self.config.background_image_url}');
            background-size: {self.config.background_size};
            background-position: {self.config.background_position};
            background-repeat: {self.config.background_repeat};
            background-attachment: {self.config.background_attachment};
        }}
        
        /* Ensure content is readable over background */
        .main .block-container {{
            background: rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.92);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.3);
        }}
        """
    
    def _get_main_container_css(self) -> str:
        """CSS for main container styling."""
        return """
        /* Main container styling */
        .main > div {
            padding-top: 1rem;
        }
        """
    
    def _get_chat_message_css(self) -> str:
        """CSS for chat message styling."""
        return f"""
        /* Chat message styling - consistent for both light and dark modes */
        .user-message {{
            background: {self.config.secondary_color};
            color: white;
            padding: 15px 20px;
            border-radius: 20px 20px 5px 20px;
            margin: 10px 0 10px 20%;
            backdrop-filter: blur(10px);
        }}
        
        .bot-message {{
            background: {self.config.background_dark};
            color: {self.config.text_color};
            padding: 15px 20px;
            border-radius: 20px 20px 20px 5px;
            margin: 10px 20% 10px 0;
            border-left: 4px solid {self.config.primary_color};
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }}
        
        .message-header {{
            font-weight: bold;
            font-size: 0.9em;
            margin-bottom: 8px;
            opacity: 0.9;
        }}
        
        .message-content {{
            line-height: 1.5;
            word-wrap: break-word;
        }}
        """
    
    def _get_form_css(self) -> str:
        """CSS for form styling."""
        return f"""
        /* Form styling - consistent for both light and dark modes */
        .stTextArea textarea {{
            border: 2px solid {self.config.primary_color};
            border-radius: {self.config.border_radius};
            padding: 15px;
            font-size: 16px;
            transition: all 0.3s ease;
            background: #e8f5e8 !important;
            backdrop-filter: blur(5px);
            color: #000000 !important;
            caret-color: #000000 !important;
        }}
        
        .stTextArea textarea::placeholder {{
            color: #666666 !important;
            opacity: 0.7;
        }}
        
        .stTextArea textarea:focus {{
            border-color: {self.config.secondary_color};
            box-shadow: 0 0 0 3px rgba(2, 102, 7, 0.1);
            background: #e8f5e8 !important;
            caret-color: #000000 !important;
        }}
        
        .stTextInput input {{
            border: 2px solid {self.config.primary_color};
            border-radius: 10px;
            padding: 12px 15px;
            font-size: 16px;
            transition: all 0.3s ease;
            background: #e8f5e8 !important;
            backdrop-filter: blur(5px);
            color: #000000 !important;
            caret-color: #000000 !important;
        }}
        
        .stTextInput input::placeholder {{
            color: #666666 !important;
            opacity: 0.7;
        }}
        
        .stTextInput input:focus {{
            border-color: {self.config.secondary_color};
            box-shadow: 0 0 0 3px rgba(2, 102, 7, 0.1);
            background: #e8f5e8 !important;
            caret-color: #000000 !important;
        }}
        """
    
    def _get_button_css(self) -> str:
        """CSS for button styling."""
        return f"""
        /* Button styling */
        .stButton button {{
            border-radius: {self.config.button_radius};
            border: none !important;
            font-weight: 600;
            padding: 12px 24px;
            transition: all 0.3s ease;
            cursor: pointer;
            backdrop-filter: blur(10px);
        }}
        
        .stButton button[kind="primary"] {{
            background: {self.config.secondary_color};
            color: white;
            box-shadow: 0 4px 15px {self.config.shadow_color};
            border: none !important;
        }}
        
        .stButton button[kind="primary"]:hover {{
            background: {self.config.secondary_color} !important;
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(2, 102, 7, 0.4);
            border: none !important;
        }}
        
        .stButton button[kind="secondary"] {{
            background: {self.config.background_dark};
            color: {self.config.primary_color};
            border: none !important;
            width: 100%;
            text-align: left;
            margin: 5px 0;
        }}
        
        .stButton button[kind="secondary"]:hover {{
            background: {self.config.secondary_color};
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px {self.config.shadow_color};
            border: none !important;
        }}
        
        /* Form submit button - Special styling for Start Chatting and Send Message */
        .stForm button {{
            background: {self.config.secondary_color} !important;
            color: white !important;
            border: none !important;
            border-radius: {self.config.button_radius};
            padding: 12px 30px;
            font-weight: 600;
            font-size: 16px;
            width: 100%;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }}
        
        .stForm button:hover {{
            background: {self.config.secondary_color} !important;
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(2, 102, 7, 0.4);
            border: none !important;
        }}
        """
    
    def _get_tab_css(self) -> str:
        """CSS for tab styling."""
        return f"""
        /* Tab styling - consistent for both light and dark modes */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            height: 40px;
            padding-left: 20px;
            padding-right: 20px;
            background-color: transparent;
            border-radius: 10px 10px 0 0;
            border: none;
            color: white !important;
            font-weight: 600;
            transition: all 0.3s ease;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            transform: translateY(-2px);
            background-color: rgba(255, 255, 255, 0.1);
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {self.config.secondary_color} !important;
            color: white !important;
            border: none !important;
            border-bottom: 2px solid white !important;
            text-shadow: none;
        }}
        
        .stTabs [data-baseweb="tab-panel"] {{
            padding: 20px;
            border: none;
            border-radius: 0 10px 10px 10px;
            background-color: rgba(255, 255, 255, 0.05);
        }}
        
        /* Remove any red borders from tabs */
        .stTabs [data-baseweb="tab"]:focus {{
            outline: none !important;
            border: none !important;
        }}
        
        .stTabs [data-baseweb="tab"]:active {{
            outline: none !important;
            border: none !important;
        }}
        """
    
    def _get_file_uploader_css(self) -> str:
        """CSS for file uploader styling."""
        return f"""
        /* File uploader styling */
        .stFileUploader > div > div > div > div {{
            border: 2px dashed {self.config.primary_color};
            border-radius: {self.config.border_radius};
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .stFileUploader > div > div > div > div:hover {{
            border-color: {self.config.secondary_color};
            background: rgba(255, 255, 255, 0.95);
        }}
        
        /* Browse files button */
        .stFileUploader button {{
            background: {self.config.secondary_color} !important;
            color: white !important;
            border: none !important;
            border-radius: {self.config.button_radius} !important;
            padding: 8px 16px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }}
        
        .stFileUploader button:hover {{
            background: {self.config.secondary_color} !important;
            color: white !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 15px rgba(2, 102, 7, 0.4) !important;
        }}
        
        /* File uploader text */
        .stFileUploader small {{
            color: {self.config.text_color};
        }}
        """
    
    def _get_title_css(self) -> str:
        """CSS for title styling."""
        return f"""
        /* Title styling - consistent for both light and dark modes */
        h1 {{
            color: white !important;
            text-align: center;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        }}
        
        h2 {{
            color: white !important;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        }}
        
        h3 {{
            color: white !important;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 400;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
        }}
        
        /* General text styling for consistent appearance */
        .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
            color: white !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
        }}
        
        /* Form labels and text */
        .stForm label, .stForm p, .stForm div {{
            color: white !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
        }}
        
        /* Subheader styling - Enhanced for better visibility */
        .stSubheader, .stSubheader > div, .stSubheader p {{
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important;
        }}
        
        /* Any div containing text should be white */
        div[data-testid="stMarkdownContainer"] p {{
            color: white !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
        }}
        
        /* Ensure all paragraph text is white with shadow */
        p {{
            color: white !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
        }}
        """
    
    def _get_responsive_css(self) -> str:
        """CSS for responsive design."""
        return """
        /* Responsive design */
        @media (max-width: 768px) {
            .user-message, .bot-message {
                margin-left: 5%;
                margin-right: 5%;
            }
            
            .stButton button {
                font-size: 14px;
                padding: 10px 20px;
            }
            
            .main .block-container {
                margin: 0.5rem;
                padding: 1rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: 35px;
                padding-left: 15px;
                padding-right: 15px;
                font-size: 14px;
            }
        }
        """
    
    def display_chat_message(self, user_msg: str, bot_reply: str, user_name: str, bot_name: str = "Assistant") -> None:
        """Display a chat message pair with the theme styling."""
        # User message
        st.markdown(
            f"""
            <div class="user-message">
                <div class="message-header">👤 {user_name}</div>
                <div class="message-content">{user_msg}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Bot reply
        st.markdown(
            f"""
            <div class="bot-message">
                <div class="message-header">🤖 {bot_name}</div>
                <div class="message-content">{bot_reply}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Predefined theme configurations
class ThemePresets:
    """Predefined theme configurations for different use cases."""
    
    @staticmethod
    def green_farm_theme() -> ThemeConfig:
        """Original green farm theme with forest background."""
        return ThemeConfig(
            primary_color="#000000",
            secondary_color="#035509",
            accent_color="#014405",
            background_image_url="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2560&q=80",
            background_opacity=0.15,
            shadow_color="rgba(2, 102, 7, 0.3)"
        )
    
    @staticmethod
    def green_farm_field_theme() -> ThemeConfig:
        """Green farm theme with agricultural field background."""
        return ThemeConfig(
            primary_color="#026607",
            secondary_color="#035509",
            accent_color="#014405",
            background_image_url="https://images.unsplash.com/photo-1500595046743-cd271d694d30?ixlib=rb-4.0.3&auto=format&fit=crop&w=2574&q=80",
            background_opacity=0.12,
            shadow_color="rgba(2, 102, 7, 0.3)"
        )
    
    @staticmethod
    def green_meadow_theme() -> ThemeConfig:
        """Green theme with meadow background."""
        return ThemeConfig(
            primary_color="#026607",
            secondary_color="#035509",
            accent_color="#014405",
            background_image_url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2570&q=80",
            background_opacity=0.1,
            shadow_color="rgba(2, 102, 7, 0.3)"
        )
    
    @staticmethod
    def blue_tech_theme() -> ThemeConfig:
        """Blue tech theme."""
        return ThemeConfig(
            primary_color="#2196F3",
            secondary_color="#1976D2",
            accent_color="#0D47A1",
            shadow_color="rgba(33, 150, 243, 0.3)"
        )
    
    @staticmethod
    def purple_creative_theme() -> ThemeConfig:
        """Purple creative theme."""
        return ThemeConfig(
            primary_color="#9C27B0",
            secondary_color="#7B1FA2",
            accent_color="#4A148C",
            shadow_color="rgba(156, 39, 176, 0.3)"
        )
    
    @staticmethod
    def orange_energy_theme() -> ThemeConfig:
        """Orange energy theme."""
        return ThemeConfig(
            primary_color="#FF9800",
            secondary_color="#F57C00",
            accent_color="#E65100",
            shadow_color="rgba(255, 152, 0, 0.3)"
        )

# Usage example
def example_usage():
    """Example of how to use the StreamlitChatTheme class with background images."""
    
    # Option 1: Use green farm theme with forest background
    theme = StreamlitChatTheme(ThemePresets.green_farm_theme())
    theme.apply_theme()
    
    # Option 2: Use green farm field theme
    field_theme = StreamlitChatTheme(ThemePresets.green_farm_field_theme())
    field_theme.apply_theme()
    
    # Option 3: Create custom theme with your own background
    custom_config = ThemeConfig(
        primary_color="#026607",
        secondary_color="#035509",
        accent_color="#014405",
        background_image_url="https://your-custom-image-url.jpg",
        background_opacity=0.15,
        background_size="cover",
        background_position="center",
        background_attachment="fixed"
    )
    custom_theme = StreamlitChatTheme(custom_config)
    custom_theme.apply_theme()
    
    # Option 4: No background image (original theme)
    no_bg_theme = StreamlitChatTheme()
    no_bg_theme.apply_theme()
    
    # Display chat messages
    theme.display_chat_message(
        "Hello, how can I help you with your farming questions today?",
        "Hi! I'm here to assist you with agricultural advice, crop management, and farming best practices.",
        "Farmer John"
    )

if __name__ == "__main__":
    example_usage()