"""
Krystal Mobile Application - Modern Power Structure Mapping Interface
GPL v3
"""

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.animation import Animation
from kivy.uix.modalview import ModalView

# KivyMD Components
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDRoundFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.chip import MDChip
from kivymd.uix.list import MDList, OneLineListItem, OneLineIconListItem, TwoLineListItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.slider import MDSlider
from kivymd.icon_definitions import md_icons

# Core functionality
from krystal.power_mapper import PowerMapper, create_sample_network
from krystal.data_sources import LittleSisClient, NewsClient


class WelcomeScreen(MDScreen):
    """Modern welcome screen with animations and engaging design"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "welcome"
        self.build_ui()
    
    def build_ui(self):
        # Main layout with gradient background
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(40),
            spacing=dp(30),
            md_bg_color=[0.95, 0.95, 0.98, 1]  # Light blue-gray
        )
        
        # Animated header section
        header_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            size_hint_y=0.4,
            adaptive_height=False
        )
        
        # Animated icon
        self.icon_label = MDLabel(
            text="🔍",
            font_style="H2",
            theme_text_color="Custom",
            text_color=[0.2, 0.5, 0.8, 1],
            halign="center",
            size_hint_y=0.6
        )
        
        # App title with gradient text effect
        title_layout = MDBoxLayout(orientation="vertical", spacing=dp(5))
        title_label = MDLabel(
            text="KRYSTAL",
            font_style="H4",
            bold=True,
            theme_text_color="Custom",
            text_color=[0.1, 0.3, 0.6, 1],
            halign="center"
        )
        subtitle_label = MDLabel(
            text="Power Structure Mapper",
            font_style="Subtitle1",
            theme_text_color="Secondary",
            halign="center"
        )
        
        title_layout.add_widget(title_label)
        title_layout.add_widget(subtitle_label)
        
        header_layout.add_widget(self.icon_label)
        header_layout.add_widget(title_layout)
        
        # Features carousel
        features_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            size_hint_y=0.4,
            elevation=2,
            radius=[dp(15), dp(15), dp(15), dp(15)]
        )
        
        features_title = MDLabel(
            text="Discover Hidden Connections",
            font_style="H6",
            theme_text_color="Primary",
            halign="center"
        )
        
        features_list = MDBoxLayout(orientation="vertical", spacing=dp(10))
        
        features = [
            ("🔍", "Analyze news articles for power structures"),
            ("📊", "Visualize relationship networks"),
            ("🏛️", "Track corporate and government ties"),
            ("🔒", "Privacy-first, no data collection")
        ]
        
        for icon, text in features:
            feature_item = MDBoxLayout(orientation="horizontal", spacing=dp(15))
            icon_label = MDLabel(
                text=icon,
                font_style="Body1",
                size_hint_x=0.2
            )
            text_label = MDLabel(
                text=text,
                font_style="Body2",
                theme_text_color="Secondary",
                size_hint_x=0.8
            )
            feature_item.add_widget(icon_label)
            feature_item.add_widget(text_label)
            features_list.add_widget(feature_item)
        
        features_card.add_widget(features_title)
        features_card.add_widget(features_list)
        
        # Action buttons
        action_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            size_hint_y=0.2
        )
        
        self.start_button = MDRaisedButton(
            text="Start Analysis",
            size_hint_y=None,
            height=dp(50),
            md_bg_color=[0.2, 0.6, 0.8, 1],
            elevation=4
        )
        self.start_button.bind(on_press=self.start_analysis)
        
        sample_button = MDFlatButton(
            text="Try Sample Data",
            size_hint_y=None,
            height=dp(40),
            theme_text_color="Custom",
            text_color=[0.2, 0.6, 0.8, 1]
        )
        sample_button.bind(on_press=self.show_sample)
        
        action_layout.add_widget(self.start_button)
        action_layout.add_widget(sample_button)
        
        # Assemble main layout
        main_layout.add_widget(header_layout)
        main_layout.add_widget(features_card)
        main_layout.add_widget(action_layout)
        
        self.add_widget(main_layout)
        
        # Start animations
        Clock.schedule_once(self.animate_entrance, 0.5)
    
    def animate_entrance(self, dt):
        """Animate the welcome screen entrance"""
        anim = Animation(opacity=1, duration=0.8)
        anim.start(self.icon_label)
        
        # Bounce animation for icon
        anim_icon = Animation(font_size=dp(80), duration=0.5, t='out_back')
        anim_icon.start(self.icon_label)
    
    def start_analysis(self, instance):
        """Navigate to analysis screen with animation"""
        # Button press animation
        anim = Animation(md_bg_color=[0.1, 0.4, 0.6, 1], duration=0.1) + \
               Animation(md_bg_color=[0.2, 0.6, 0.8, 1], duration=0.1)
        anim.start(instance)
        
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'analysis'), 0.3)
    
    def show_sample(self, instance):
        """Show sample data preview"""
        sample_dialog = MDDialog(
            title="Sample Analysis",
            text="This will load a demonstration with sample power structure data showing how Krystal analyzes relationships between corporations, government entities, and influential organizations.",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=[0.5, 0.5, 0.5, 1],
                    on_release=lambda x: sample_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Load Sample",
                    md_bg_color=[0.2, 0.6, 0.8, 1],
                    on_release=lambda x: self.load_sample_data(sample_dialog)
                ),
            ],
        )
        sample_dialog.open()
    
    def load_sample_data(self, dialog):
        """Load sample data and navigate to analysis"""
        dialog.dismiss()
        self.manager.current = 'analysis'
        analysis_screen = self.manager.get_screen('analysis')
        Clock.schedule_once(lambda dt: analysis_screen.load_sample_data(), 0.5)


class AnalysisScreen(MDScreen):
    """Modern analysis screen with enhanced UX"""
    
    progress_value = NumericProperty(0)
    status_text = StringProperty("Ready to analyze power structures")
    is_analyzing = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "analysis"
        
        # Initialize core components
        self.mapper = PowerMapper()
        self.news_client = NewsClient()
        self.littlesis_client = LittleSisClient()
        
        self.dialog = None
        self.build_ui()
    
    def build_ui(self):
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Top App Bar
        self.top_bar = MDTopAppBar(
            title="Power Analysis",
            elevation=4,
            md_bg_color=[0.2, 0.6, 0.8, 1],
            specific_text_color=[1, 1, 1, 1],
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[
                ["information-outline", lambda x: self.show_help()],
                ["cog", lambda x: self.show_settings()],
            ]
        )
        main_layout.add_widget(self.top_bar)
        
        # Content area
        content_layout = MDBoxLayout(orientation="vertical", padding=dp(20), spacing=dp(20))
        
        # Input Card
        input_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            elevation=2,
            radius=[dp(15), dp(15), dp(15), dp(15)]
        )
        
        input_title = MDLabel(
            text="Analyze Power Structures",
            font_style="H6",
            theme_text_color="Primary"
        )
        
        self.url_input = MDTextField(
            hint_text="Enter news URL or search terms...",
            mode="round",
            size_hint_y=None,
            height=dp(56),
            icon_left="magnify"
        )
        
        # Analysis type chips
        chip_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), adaptive_height=True)
        analysis_types = [
            ("News Article", "newspaper"),
            ("Organization", "office-building"),
            ("Person", "account"),
            ("Topic", "tag-multiple")
        ]
        
        self.active_chip = None
        for text, icon in analysis_types:
            chip = MDChip(
                text=text,
                icon=icon,
                check=True,
                color=[0.2, 0.6, 0.8, 1]
            )
            chip.bind(on_press=lambda x, t=text: self.set_analysis_type(x, t))
            chip_layout.add_widget(chip)
            if text == "News Article":
                self.active_chip = chip
                chip.active = True
        
        # Action buttons
        button_layout = MDBoxLayout(orientation="horizontal", spacing=dp(15), adaptive_height=True)
        
        self.analyze_btn = MDRaisedButton(
            text="Start Analysis",
            size_hint_x=0.7,
            md_bg_color=[0.2, 0.6, 0.8, 1],
            on_release=self.analyze_article
        )
        
        sample_btn = MDFlatButton(
            text="Quick Sample",
            size_hint_x=0.3,
            theme_text_color="Custom",
            text_color=[0.5, 0.5, 0.5, 1],
            on_release=lambda x: self.load_sample_data()
        )
        
        button_layout.add_widget(self.analyze_btn)
        button_layout.add_widget(sample_btn)
        
        input_card.add_widget(input_title)
        input_card.add_widget(self.url_input)
        input_card.add_widget(chip_layout)
        input_card.add_widget(button_layout)
        content_layout.add_widget(input_card)
        
        # Progress Card
        self.progress_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            elevation=2,
            radius=[dp(15), dp(15), dp(15), dp(15)],
            opacity=0  # Hidden initially
        )
        
        progress_title = MDLabel(
            text="Analysis Progress",
            font_style="H6",
            theme_text_color="Primary"
        )
        
        self.status_label = MDLabel(
            text=self.status_text,
            font_style="Body1",
            theme_text_color="Secondary"
        )
        
        self.progress_bar = MDProgressBar(
            value=self.progress_value,
        )
        
        self.progress_card.add_widget(progress_title)
        self.progress_card.add_widget(self.status_label)
        self.progress_card.add_widget(self.progress_bar)
        content_layout.add_widget(self.progress_card)
        
        # Results Section
        results_title = MDLabel(
            text="Analysis Results",
            font_style="H6",
            theme_text_color="Primary"
        )
        content_layout.add_widget(results_title)
        
        # Scrollable results
        self.results_scroll = MDScrollView()
        self.results_layout = MDList()
        self.results_scroll.add_widget(self.results_layout)
        content_layout.add_widget(self.results_scroll)
        
        main_layout.add_widget(content_layout)
        self.add_widget(main_layout)
    
    def set_analysis_type(self, chip, analysis_type):
        """Set the active analysis type"""
        if self.active_chip:
            self.active_chip.active = False
        chip.active = True
        self.active_chip = chip
        self.top_bar.title = f"{analysis_type} Analysis"
    
    def analyze_article(self, instance):
        """Start analysis with enhanced UX"""
        query = self.url_input.text.strip()
        if not query:
            self.show_snackbar("Please enter a URL or search terms")
            return
        
        if self.is_analyzing:
            return
        
        self.is_analyzing = True
        self.analyze_btn.disabled = True
        self.analyze_btn.text = "Analyzing..."
        
        # Show progress card with animation
        anim = Animation(opacity=1, duration=0.3)
        anim.start(self.progress_card)
        
        # Clear previous results
        self.results_layout.clear_widgets()
        
        # Add initial status item
        initial_item = TwoLineListItem(
            text="Starting analysis...",
            secondary_text="Preparing to map power structures"
        )
        self.results_layout.add_widget(initial_item)
        
        # Start analysis process
        Clock.schedule_once(lambda dt: self._perform_analysis(query), 0.5)
    
    def _perform_analysis(self, query):
        """Perform analysis with detailed progress updates"""
        try:
            steps = [
                (20, "Searching for relevant content..."),
                (40, "Extracting entities and organizations..."),
                (60, "Mapping relationships and connections..."),
                (80, "Analyzing power structures..."),
                (95, "Finalizing results..."),
                (100, "Analysis complete!")
            ]
            
            def update_step(step_index):
                if step_index < len(steps):
                    progress, status = steps[step_index]
                    self.update_progress(progress, status)
                    
                    # Update the status in results list
                    if step_index > 0:
                        self.results_layout.children[0].text = status
                        self.results_layout.children[0].secondary_text = f"Progress: {progress}%"
                    
                    # Schedule next step
                    Clock.schedule_once(lambda dt: update_step(step_index + 1), 1)
                else:
                    # Analysis complete
                    self._analysis_complete(query)
            
            # Start the step-by-step progress
            update_step(0)
            
        except Exception as e:
            self._analysis_error(str(e))
    
    def _analysis_complete(self, query):
        """Handle analysis completion"""
        try:
            # Simulate getting results (replace with actual analysis)
            articles = self.news_client.search_news(query, max_results=3)
            entities = self.littlesis_client.search_entities(query)
            
            relationships = []
            for entity in entities[:5]:  # Limit for demo
                connections = self.littlesis_client.get_entity_connections(entity['id'])
                relationships.extend(connections)
            
            # Perform actual analysis
            analysis = self.mapper.analyze_network(entities, relationships)
            
            # Clear loading item and display results
            self.results_layout.clear_widgets()
            self.display_analysis_results(analysis, articles[0] if articles else {"title": query})
            
            # Reset UI state
            self.is_analyzing = False
            self.analyze_btn.disabled = False
            self.analyze_btn.text = "Start Analysis"
            
            # Hide progress card after delay
            Clock.schedule_once(lambda dt: Animation(opacity=0, duration=0.5).start(self.progress_card), 2)
            
            self.show_snackbar("Analysis completed successfully!")
            
        except Exception as e:
            self._analysis_error(str(e))
    
    def _analysis_error(self, error_msg):
        """Handle analysis errors"""
        self.is_analyzing = False
        self.analyze_btn.disabled = False
        self.analyze_btn.text = "Start Analysis"
        
        self.results_layout.clear_widgets()
        error_item = TwoLineListItem(
            text="Analysis Failed",
            secondary_text=error_msg
        )
        self.results_layout.add_widget(error_item)
        
        self.show_snackbar("Analysis failed - please try again")
    
    def update_progress(self, value, status):
        """Update progress with animation"""
        Animation(progress_value=value, duration=0.5).start(self)
        self.status_text = status
        self.status_label.text = status
    
    def load_sample_data(self, instance=None):
        """Load sample data with enhanced UX"""
        self.url_input.text = "technology sector influence"
        self.analyze_article(None)
    
    def display_analysis_results(self, analysis, article):
        """Display beautiful analysis results"""
        # Article header
        article_item = TwoLineListItem(
            text=article.get('title', 'Analysis Results'),
            secondary_text=f"Source: {article.get('source', 'Krystal Analysis')}",
            bg_color=[0.95, 0.95, 0.98, 1]
        )
        self.results_layout.add_widget(article_item)
        
        # Summary card
        summary_item = TwoLineListItem(
            text="Network Summary",
            secondary_text=f"{analysis['summary']['entity_count']} entities • {analysis['summary']['relationship_count']} relationships • Density: {analysis['summary']['network_density']:.3f}"
        )
        self.results_layout.add_widget(summary_item)
        
        # Top influencers
        if analysis['influence_rankings']:
            influencers_header = OneLineListItem(text="🏆 Most Influential Entities")
            self.results_layout.add_widget(influencers_header)
            
            for i, entity in enumerate(analysis['influence_rankings'][:5]):
                influencer_item = TwoLineListItem(
                    text=f"{i+1}. {entity['name']}",
                    secondary_text=f"Influence score: {entity.get('influence_score', 0):.1f} • {entity.get('type', 'Entity').title()}"
                )
                self.results_layout.add_widget(influencer_item)
        
        # Key findings
        if analysis.get('key_findings'):
            findings_header = OneLineListItem(text="🔍 Key Findings")
            self.results_layout.add_widget(findings_header)
            
            for finding in analysis['key_findings'][:3]:
                finding_item = OneLineListItem(text=f"• {finding}")
                self.results_layout.add_widget(finding_item)
        
        # Action buttons
        actions_header = OneLineListItem(text="📤 Export & Share")
        self.results_layout.add_widget(actions_header)
        
        # Would add export buttons here in a real implementation
    
    def show_snackbar(self, message):
        """Show a snackbar message"""
        # In a real implementation, use MDApp.get_running_app().show_snackbar(message)
        print(f"Snackbar: {message}")  # Placeholder
    
    def go_back(self):
        """Return to welcome screen"""
        self.manager.current = 'welcome'
    
    def show_help(self):
        """Show help dialog"""
        help_dialog = MDDialog(
            title="How to Use Krystal",
            text="1. Enter a news URL or search terms\n2. Select analysis type\n3. View power structure mapping\n4. Explore connections and influence scores\n\nKrystal helps you uncover hidden relationships between powerful entities in news media.",
            buttons=[
                MDFlatButton(
                    text="Got it",
                    theme_text_color="Custom",
                    text_color=[0.2, 0.6, 0.8, 1],
                    on_release=lambda x: help_dialog.dismiss()
                ),
            ],
        )
        help_dialog.open()
    
    def show_settings(self):
        """Show settings dialog"""
        settings_dialog = MDDialog(
            title="Settings",
            type="custom",
            content_cls=MDBoxLayout(
                orientation="vertical",
                spacing=dp(15),
                adaptive_height=True
            ),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=[0.5, 0.5, 0.5, 1],
                ),
                MDRaisedButton(
                    text="Save",
                    md_bg_color=[0.2, 0.6, 0.8, 1],
                ),
            ],
        )
        
        # Add settings controls to content
        # Would add API key inputs, theme settings, etc.
        
        settings_dialog.open()


class KrystalApp(MDApp):
    """Modern KivyMD application with enhanced UX"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
    
    def build(self):
        self.title = "Krystal - Power Structure Mapper"
        Window.clearcolor = (0.95, 0.95, 0.98, 1)  # Light background
        
        # Create screen manager
        sm = MDScreenManager()
        
        # Add screens
        welcome_screen = WelcomeScreen()
        analysis_screen = AnalysisScreen()
        
        sm.add_widget(welcome_screen)
        sm.add_widget(analysis_screen)
        
        return sm
    
    def on_start(self):
        """Called when the app starts"""
        print("🚀 Krystal app started with enhanced UI!")
    
    def show_snackbar(self, message):
        """Show snackbar notification"""
        # This would use KivyMD's Snackbar in a real implementation
        print(f"Notification: {message}")


def main():
    """Main entry point"""
    try:
        KrystalApp().run()
    except Exception as e:
        print(f"❌ App error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()