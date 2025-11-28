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
from kivy.uix.image import Image

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
from kivymd.uix.list import MDList, OneLineListItem, OneLineIconListItem, TwoLineListItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.slider import MDSlider

# Core functionality
from krystal.power_mapper import PowerMapper, create_sample_network
from krystal.data_sources import LittleSisClient, NewsClient


class IconButton(MDRaisedButton):
    """Enhanced button with icon support and better animations"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.animation = None
    
    def on_press(self):
        """Add press animation"""
        if self.animation:
            self.animation.cancel(self)
        
        self.animation = Animation(
            md_bg_color=[c * 0.8 for c in self.md_bg_color[:3]] + [1],
            duration=0.1
        )
        self.animation.start(self)
        
        # Call original press handler
        super().on_press()
    
    def on_release(self):
        """Add release animation"""
        if self.animation:
            self.animation.cancel(self)
        
        self.animation = Animation(
            md_bg_color=self.theme_cls.primary_color,
            duration=0.2
        )
        self.animation.start(self)
        
        # Call original release handler
        super().on_release()


class CategoryButton(MDRoundFlatButton):
    """Specialized button for category selection with better visual feedback"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_active = False
    
    def set_active(self, active):
        """Toggle active state with animation"""
        self.is_active = active
        if active:
            anim = Animation(
                md_bg_color=[0.2, 0.6, 0.8, 1],
                text_color=[1, 1, 1, 1],
                duration=0.3
            )
        else:
            anim = Animation(
                md_bg_color=[1, 1, 1, 0],
                text_color=[0.5, 0.5, 0.5, 1],
                duration=0.3
            )
        anim.start(self)


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
            md_bg_color=[0.95, 0.95, 0.98, 1]
        )
        
        # Header section
        header_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            size_hint_y=0.4
        )
        
        # App icon with better styling
        self.icon_label = MDLabel(
            text="🔍",  # Can be replaced with actual image
            font_style="H2",
            theme_text_color="Custom",
            text_color=[0.2, 0.5, 0.8, 1],
            halign="center",
            size_hint_y=0.6
        )
        
        # App title
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
        
        # Features section
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
        
        # Action buttons with enhanced functionality
        action_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            size_hint_y=0.2
        )
        
        self.start_button = IconButton(
            text="Start Analysis",
            icon="rocket-launch",  # Material Design icon
            size_hint_y=None,
            height=dp(50),
            md_bg_color=[0.2, 0.6, 0.8, 1],
            elevation=4
        )
        self.start_button.bind(on_press=self.start_analysis)
        
        sample_button = MDFlatButton(
            text="Try Sample Data",
            icon="test-tube",  # Material Design icon
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
    
    def start_analysis(self, instance):
        """Navigate to analysis screen with button animation completion"""
        # Complete button animation before transition
        anim = Animation(
            md_bg_color=[0.1, 0.4, 0.6, 1],
            duration=0.2
        )
        anim.bind(on_complete=lambda *args: setattr(self.manager, 'current', 'analysis'))
        anim.start(instance)
    
    def show_sample(self, instance):
        """Show sample data preview with enhanced dialog"""
        sample_dialog = MDDialog(
            title="Sample Analysis",
            type="custom",
            content_cls=MDBoxLayout(
                MDLabel(
                    text="This will load a demonstration with sample power structure data showing how Krystal analyzes relationships between corporations, government entities, and influential organizations.",
                    size_hint_y=None,
                    height=dp(80)
                ),
                orientation="vertical",
                spacing=dp(10),
                adaptive_height=True
            ),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    icon="close-circle",
                    theme_text_color="Custom",
                    text_color=[0.5, 0.5, 0.5, 1],
                    on_release=lambda x: sample_dialog.dismiss()
                ),
                IconButton(
                    text="Load Sample",
                    icon="download",
                    md_bg_color=[0.2, 0.6, 0.8, 1],
                    on_release=lambda x: self.load_sample_data(sample_dialog)
                ),
            ],
        )
        sample_dialog.open()
    
    def load_sample_data(self, dialog):
        """Load sample data and navigate to analysis with smooth transition"""
        dialog.dismiss()
        
        # Show loading state
        self.start_button.disabled = True
        self.start_button.text = "Loading Sample..."
        
        Clock.schedule_once(lambda dt: self._complete_sample_load(), 1.0)
    
    def _complete_sample_load(self):
        """Complete sample data loading"""
        self.manager.current = 'analysis'
        analysis_screen = self.manager.get_screen('analysis')
        Clock.schedule_once(lambda dt: analysis_screen.load_sample_data(), 0.5)
        
        # Reset button state
        self.start_button.disabled = False
        self.start_button.text = "Start Analysis"


class AnalysisScreen(MDScreen):
    """Modern analysis screen with enhanced UX and News API integration"""
    
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
        self.active_analysis_type = "News"
        self.active_news_category = None
        self.analysis_buttons = []
        self.category_buttons = []
        
        self.build_ui()
    
    def build_ui(self):
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Top App Bar with enhanced navigation
        self.top_bar = MDTopAppBar(
            title="Power Analysis",
            elevation=4,
            md_bg_color=[0.2, 0.6, 0.8, 1],
            specific_text_color=[1, 1, 1, 1],
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[
                ["help-circle", lambda x: self.show_help()],
                ["cog", lambda x: self.show_settings()],
            ]
        )
        main_layout.add_widget(self.top_bar)
        
        # Content area
        content_layout = MDBoxLayout(orientation="vertical", padding=dp(20), spacing=dp(20))
        
        # Input Card with enhanced styling
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
        
        # Analysis type buttons with enhanced functionality
        analysis_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), adaptive_height=True)
        analysis_types = [
            ("News", "newspaper-variant"),
            ("Organization", "office-building"),
            ("Person", "account"),
            ("Topic", "tag")
        ]
        
        for text, icon in analysis_types:
            btn = IconButton(
                text=text,
                icon=icon,
                size_hint_x=None,
                width=dp(130),
                theme_text_color="Custom",
                text_color=[1, 1, 1, 1] if text == "News" else [0.5, 0.5, 0.5, 1],
                md_bg_color=[0.2, 0.6, 0.8, 1] if text == "News" else [0.8, 0.8, 0.8, 1]
            )
            btn.bind(on_release=lambda x, t=text: self.set_analysis_type(x, t))
            analysis_layout.add_widget(btn)
            self.analysis_buttons.append(btn)
        
        # News category selection with enhanced buttons
        category_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), adaptive_height=True)
        category_label = MDLabel(
            text="Category:",
            font_style="Body2",
            theme_text_color="Secondary",
            size_hint_x=0.3
        )
        
        # News categories with specialized buttons
        category_buttons_layout = MDBoxLayout(orientation="horizontal", spacing=dp(5), adaptive_height=True)
        categories = [
            ("All", "asterisk"),
            ("Technology", "laptop"),
            ("Business", "briefcase"),
            ("Politics", "gavel"),
            ("General", "earth")
        ]
        
        for category, icon in categories:
            btn = CategoryButton(
                text=category,
                icon=icon,
                size_hint_x=None,
                width=dp(90),
                theme_text_color="Custom",
                text_color=[0.2, 0.6, 0.8, 1] if category == "All" else [0.5, 0.5, 0.5, 1],
                line_color=[0.2, 0.6, 0.8, 1] if category == "All" else [0.8, 0.8, 0.8, 1]
            )
            btn.set_active(category == "All")
            btn.bind(on_release=lambda x, c=category: self.set_news_category(x, c))
            category_buttons_layout.add_widget(btn)
            self.category_buttons.append(btn)
        
        category_layout.add_widget(category_label)
        category_layout.add_widget(category_buttons_layout)
        
        # Action buttons with enhanced functionality
        button_layout = MDBoxLayout(orientation="horizontal", spacing=dp(15), adaptive_height=True)
        
        self.analyze_btn = IconButton(
            text="Start Analysis",
            icon="magnify",
            size_hint_x=0.7,
            md_bg_color=[0.2, 0.6, 0.8, 1],
            on_release=self.analyze_article
        )
        
        sample_btn = MDFlatButton(
            text="Quick Sample",
            icon="lightning-bolt",
            size_hint_x=0.3,
            theme_text_color="Custom",
            text_color=[0.5, 0.5, 0.5, 1],
            on_release=lambda x: self.load_sample_data()
        )
        
        button_layout.add_widget(self.analyze_btn)
        button_layout.add_widget(sample_btn)
        
        input_card.add_widget(input_title)
        input_card.add_widget(self.url_input)
        input_card.add_widget(analysis_layout)
        input_card.add_widget(category_layout)
        input_card.add_widget(button_layout)
        content_layout.add_widget(input_card)
        
        # Progress Card with enhanced animations
        self.progress_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            elevation=2,
            radius=[dp(15), dp(15), dp(15), dp(15)],
            opacity=0
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
    
    def set_analysis_type(self, button, analysis_type):
        """Set the active analysis type with smooth transitions"""
        # Animate all buttons to inactive state
        for btn in self.analysis_buttons:
            if btn != button:
                anim = Animation(
                    md_bg_color=[0.8, 0.8, 0.8, 1],
                    text_color=[0.5, 0.5, 0.5, 1],
                    duration=0.3
                )
                anim.start(btn)
        
        # Animate active button
        active_anim = Animation(
            md_bg_color=[0.2, 0.6, 0.8, 1],
            text_color=[1, 1, 1, 1],
            duration=0.3
        )
        active_anim.start(button)
        
        self.active_analysis_type = analysis_type
        self.top_bar.title = f"{analysis_type} Analysis"
    
    def set_news_category(self, button, category):
        """Set the active news category with visual feedback"""
        # Update all category buttons
        for btn in self.category_buttons:
            if btn == button:
                btn.set_active(True)
            else:
                btn.set_active(False)
        
        self.active_news_category = category.lower() if category != "All" else None
    
    def analyze_article(self, instance):
        """Start analysis with enhanced UX and animations"""
        query = self.url_input.text.strip()
        if not query:
            self.show_message("Please enter a URL or search terms")
            return
        
        if self.is_analyzing:
            return
        
        self.is_analyzing = True
        self.analyze_btn.disabled = True
        self.analyze_btn.text = "Analyzing..."
        
        # Show progress card with animation
        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.progress_card)
        
        # Clear previous results
        self.results_layout.clear_widgets()
        
        # Add initial status item
        category_text = f" (Category: {self.active_news_category})" if self.active_news_category else ""
        initial_item = TwoLineListItem(
            text=f"Starting analysis{category_text}...",
            secondary_text="Preparing to map power structures"
        )
        self.results_layout.add_widget(initial_item)
        
        # Start analysis process with category
        Clock.schedule_once(lambda dt: self._perform_analysis(query, self.active_news_category), 0.5)
    
    def _perform_analysis(self, query, category=None):
        """Perform analysis with detailed progress updates and animations"""
        try:
            steps = [
                (20, f"Searching {category if category else 'all'} news..."),
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
                    self._analysis_complete(query, category)
            
            # Start the step-by-step progress
            update_step(0)
            
        except Exception as e:
            self._analysis_error(str(e))
    
    def _analysis_complete(self, query, category=None):
        """Handle analysis completion with enhanced results display"""
        try:
            # Get real news data with category
            if category and category != "all":
                articles = self.news_client.get_top_headlines(category=category, max_results=5)
            else:
                articles = self.news_client.search_news(query, max_results=5)
            
            if not articles:
                self._analysis_error("No articles found for your search")
                return
            
            # Show API status
            api_status = "🔴 Mock Data" if not self.news_client.is_api_available() else "🟢 Real News API"
            self.show_message(f"Using {api_status}")
            
            # Extract entities from articles
            entities = []
            for article in articles:
                article_entities = self.news_client.extract_entities(
                    article.get('content', '') + ' ' + article.get('title', '')
                )
                entities.extend(article_entities)
            
            # Get additional entities from LittleSis based on search query
            ls_entities = self.littlesis_client.search_entities(query)
            entities.extend(ls_entities)
            
            # Remove duplicates based on entity name
            unique_entities = {}
            for entity in entities:
                name = entity.get('name', '')
                if name and name not in unique_entities:
                    unique_entities[name] = entity
            
            entities = list(unique_entities.values())
            
            # Get relationships
            relationships = []
            for entity in entities[:10]:  # Limit to avoid too many API calls
                if 'id' in entity:
                    connections = self.littlesis_client.get_entity_connections(entity['id'])
                    relationships.extend(connections)
            
            # Perform actual analysis
            analysis = self.mapper.analyze_network(entities, relationships)
            
            # Clear loading item and display results
            self.results_layout.clear_widgets()
            self.display_analysis_results(analysis, articles[0], api_status)
            
            # Reset UI state with animations
            self.is_analyzing = False
            self.analyze_btn.disabled = False
            self.analyze_btn.text = "Start Analysis"
            
            # Hide progress card after delay with animation
            Clock.schedule_once(
                lambda dt: Animation(opacity=0, duration=0.5).start(self.progress_card), 
                2
            )
            
        except Exception as e:
            self._analysis_error(str(e))
    
    def _analysis_error(self, error_msg):
        """Handle analysis errors with user-friendly messaging"""
        self.is_analyzing = False
        self.analyze_btn.disabled = False
        self.analyze_btn.text = "Start Analysis"
        
        self.results_layout.clear_widgets()
        error_item = TwoLineListItem(
            text="Analysis Failed",
            secondary_text=error_msg
        )
        self.results_layout.add_widget(error_item)
        
        self.show_message("Analysis failed - please try again")
    
    def update_progress(self, value, status):
        """Update progress with smooth animation"""
        anim = Animation(value=value, duration=0.5)
        anim.start(self.progress_bar)
        
        self.progress_value = value
        self.status_text = status
        self.status_label.text = status
    
    def load_sample_data(self, instance=None):
        """Load sample data with enhanced UX"""
        self.url_input.text = "technology sector influence"
        
        # Add a small delay to show the text change
        Clock.schedule_once(lambda dt: self.analyze_article(None), 0.3)
    
    def display_analysis_results(self, analysis, article, api_status="🔴 Mock Data"):
        """Display beautiful analysis results with enhanced visuals"""
        # Article header with API status
        article_item = TwoLineListItem(
            text=article.get('title', 'Analysis Results'),
            secondary_text=f"Source: {article.get('source', 'Unknown')} | {api_status}",
            bg_color=[0.95, 0.95, 0.98, 1]
        )
        self.results_layout.add_widget(article_item)
        
        # Show how to get real data if using mock
        if "Mock" in api_status:
            help_item = OneLineListItem(
                text="💡 Set NEWS_API_KEY environment variable for real news data",
                bg_color=[1, 0.9, 0.9, 1]
            )
            self.results_layout.add_widget(help_item)
        
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
    
    def show_message(self, message):
        """Show a message to the user"""
        # Simple message display - could be enhanced with toast notifications
        print(f"Message: {message}")
    
    def go_back(self):
        """Return to welcome screen with smooth transition"""
        self.manager.transition.direction = 'right'
        self.manager.current = 'welcome'
    
    def show_help(self):
        """Show enhanced help dialog"""
        help_dialog = MDDialog(
            title="How to Use Krystal",
            type="custom",
            content_cls=MDBoxLayout(
                MDLabel(
                    text="1. Enter a news URL or search terms\n2. Select analysis type\n3. Choose news category (optional)\n4. View power structure mapping\n5. Explore connections and influence scores\n\nKrystal helps you uncover hidden relationships between powerful entities in news media.",
                    size_hint_y=None,
                    height=dp(150)
                ),
                orientation="vertical",
                spacing=dp(10),
                adaptive_height=True
            ),
            buttons=[
                IconButton(
                    text="Got it",
                    icon="check",
                    md_bg_color=[0.2, 0.6, 0.8, 1],
                    on_release=lambda x: help_dialog.dismiss()
                ),
            ],
        )
        help_dialog.open()
    
    def show_settings(self):
        """Show enhanced settings dialog"""
        # Check API status
        api_status = "🔴 Not configured" 
        if self.news_client.is_api_available():
            api_status = "🟢 Connected"
        
        settings_dialog = MDDialog(
            title="Settings & API Status",
            type="custom",
            content_cls=MDBoxLayout(
                MDLabel(
                    text=f"News API: {api_status}\n\nTo use real news data:\n1. Get API key from newsapi.org\n2. Set NEWS_API_KEY environment variable\n3. Restart the application",
                    size_hint_y=None,
                    height=dp(120)
                ),
                orientation="vertical",
                spacing=dp(10),
                adaptive_height=True
            ),
            buttons=[
                IconButton(
                    text="Close",
                    icon="close",
                    md_bg_color=[0.5, 0.5, 0.5, 1],
                    on_release=lambda x: settings_dialog.dismiss()
                ),
            ],
        )
        settings_dialog.open()


class KrystalApp(MDApp):
    """Modern KivyMD application with enhanced UX"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"  # Use Material Design 3
    
    def build(self):
        self.title = "Krystal - Power Structure Mapper"
        Window.clearcolor = (0.95, 0.95, 0.98, 1)
        
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
        print("🚀 Krystal app started with enhanced button functionality!")
        
        # Check API status on startup
        from krystal.data_sources import NewsClient
        news_client = NewsClient()
        if news_client.is_api_available():
            print("✅ News API is available and ready!")
        else:
            print("ℹ️  Using mock news data. Set NEWS_API_KEY for real news.")


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