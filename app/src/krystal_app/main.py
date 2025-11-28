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
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.uix.widget import Widget
import math
import re




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
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
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


class NetworkGraphWidget(Widget):
    """Interactive network graph visualization"""
    
    def __init__(self, entities, relationships, **kwargs):
        super().__init__(**kwargs)
        self.entities = entities
        self.relationships = relationships
        self.node_positions = {}
        self.selected_node = None
        self.bind(size=self._update_graph, pos=self._update_graph)
        
    def _update_graph(self, *args):
        """Update graph layout when widget size changes"""
        self.canvas.clear()
        self._draw_network()
    
    def _draw_network(self):
        """Draw the network graph"""
        if not self.entities or not self.relationships:
            return
            
        # Calculate node positions in a circle
        center_x = self.center_x
        center_y = self.center_y
        radius = min(self.width, self.height) * 0.35
        num_nodes = len(self.entities)
        
        with self.canvas:
            # Draw relationships (edges)
            for rel in self.relationships:
                source_id = rel.get('source')
                target_id = rel.get('target')
                
                if source_id in self.node_positions and target_id in self.node_positions:
                    src_x, src_y = self.node_positions[source_id]
                    tgt_x, tgt_y = self.node_positions[target_id]
                    
                    # Color based on relationship strength
                    strength = rel.get('strength', 0.5)
                    Color(0.3, 0.3, 0.8, strength)
                    
                    Line(points=[src_x, src_y, tgt_x, tgt_y], width=1.5)
            
            # Draw entities (nodes)
            for i, entity in enumerate(self.entities):
                entity_id = entity.get('id')
                angle = 2 * math.pi * i / num_nodes
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                self.node_positions[entity_id] = (x, y)
                
                # Color based on entity type
                entity_type = entity.get('type', 'organization')
                colors = {
                    'person': (0.2, 0.8, 0.2),      # Green
                    'corporation': (0.8, 0.2, 0.2), # Red
                    'government': (0.2, 0.2, 0.8),  # Blue
                    'organization': (0.8, 0.8, 0.2) # Yellow
                }
                color = colors.get(entity_type, (0.5, 0.5, 0.5))
                
                Color(*color)
                Ellipse(pos=(x-15, y-15), size=(30, 30))
                
                # Node label
                Color(0, 0, 0, 1)
                name = entity.get('name', 'Unknown')
                if len(name) > 12:
                    name = name[:12] + "..."
    
    def on_touch_down(self, touch):
        """Handle node clicks"""
        for entity_id, (x, y) in self.node_positions.items():
            if abs(touch.x - x) < 20 and abs(touch.y - y) < 20:
                entity = next((e for e in self.entities if e.get('id') == entity_id), None)
                if entity:
                    self.show_node_info(entity, touch)
                return True
        return super().on_touch_down(touch)
    
    def show_node_info(self, entity, touch):
        """Show entity information when node is clicked"""
        # Create a popup with entity details
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        
        content = BoxLayout(orientation='vertical', padding=10)
        
        name_label = Label(
            text=f"🏢 {entity.get('name', 'Unknown')}",
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height=40
        )
        
        type_label = Label(
            text=f"Type: {entity.get('type', 'Unknown').title()}",
            font_size='14sp'
        )
        
        influence_label = Label(
            text=f"Influence Score: {entity.get('influence_score', 0):.1f}",
            font_size='14sp'
        )
        
        content.add_widget(name_label)
        content.add_widget(type_label)
        content.add_widget(influence_label)
        
        popup = Popup(
            title='Entity Details',
            content=content,
            size_hint=(0.6, 0.4),
            auto_dismiss=True
        )
        popup.open()


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
        
        # App icon
        self.icon_label = MDLabel(
            text="🔍",
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
    
    def start_analysis(self, instance):
        """Navigate to analysis screen"""
        self.manager.current = 'analysis'
    
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
        self.current_analysis = None
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
                ["chart-box", lambda x: self.show_network_visualization()],
                ["help", lambda x: self.show_help()],
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
        
        # Analysis type buttons
        analysis_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), adaptive_height=True)
        analysis_types = [
            ("News", "newspaper"),
            ("Organization", "office-building"),
            ("Person", "account"),
            ("Topic", "tag")
        ]
        
        self.analysis_buttons = []
        for text, icon in analysis_types:
            btn = MDRoundFlatButton(
                text=text,
                icon=icon,
                size_hint_x=None,
                width=dp(120),
                theme_text_color="Custom",
                text_color=[0.5, 0.5, 0.5, 1],
                line_color=[0.8, 0.8, 0.8, 1]
            )
            btn.bind(on_release=lambda x, t=text: self.set_analysis_type(x, t))
            analysis_layout.add_widget(btn)
            self.analysis_buttons.append(btn)
        
        # Set first button as active
        if self.analysis_buttons:
            self.set_analysis_type(self.analysis_buttons[0], "News")
        
        # News category selection
        category_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), adaptive_height=True)
        category_label = MDLabel(
            text="Category:",
            font_style="Body2",
            theme_text_color="Secondary",
            size_hint_x=0.3
        )
        
        # News categories dropdown (simplified as buttons for now)
        self.category_buttons = []
        categories = ["All", "Technology", "Business", "Politics", "General"]
        
        category_buttons_layout = MDBoxLayout(orientation="horizontal", spacing=dp(5), adaptive_height=True)
        for category in categories:
            btn = MDRoundFlatButton(
                text=category,
                size_hint_x=None,
                width=dp(80),
                theme_text_color="Custom",
                text_color=[0.5, 0.5, 0.5, 1],
                line_color=[0.8, 0.8, 0.8, 1]
            )
            btn.bind(on_release=lambda x, c=category: self.set_news_category(x, c))
            category_buttons_layout.add_widget(btn)
            self.category_buttons.append(btn)
        
        # Set "All" as default category
        self.set_news_category(self.category_buttons[0], "All")
        
        category_layout.add_widget(category_label)
        category_layout.add_widget(category_buttons_layout)
        
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
        input_card.add_widget(analysis_layout)
        input_card.add_widget(category_layout)
        input_card.add_widget(button_layout)
        content_layout.add_widget(input_card)
        
        # Progress Card
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
    
    def extract_keywords_from_url(self, url: str) -> str:
        """Extract meaningful keywords from a URL for news search - ENHANCED VERSION"""
        try:
            print(f"🔗 Processing URL: {url}")
            
            # Remove protocol and domain
            if '://' in url:
                url = url.split('://', 1)[1]
            
            # Remove www and domain
            if url.startswith('www.'):
                url = url[4:]
            
            # Extract path (remove domain)
            if '/' in url:
                domain, path = url.split('/', 1)
            else:
                domain, path = url, ""
            
            # Common news domains to ignore in search
            news_domains = ['cnn.com', 'bbc.com', 'reuters.com', 'apnews.com', 'theguardian.com', 
                           'nytimes.com', 'washingtonpost.com', 'foxnews.com', 'nbcnews.com',
                           'wsj.com', 'bloomberg.com', 'latimes.com', 'usatoday.com']
            
            # If it's a known news domain, focus on the path
            if any(domain in nd or nd in domain for nd in news_domains):
                keywords_source = path
            else:
                keywords_source = url
            
            # Clean up the path
            import re
            
            # Remove date patterns (YYYY/MM/DD or YYYY-MM-DD)
            keywords_source = re.sub(r'\d{4}[-/]\d{2}[-/]\d{2}', '', keywords_source)
            
            # Remove common URL suffixes and technical parts
            remove_patterns = [
                r'-\w+$',  # trailing slugs like -intl, -hnk
                r'\.(html|php|aspx)$',  # file extensions
                r'/index$',  # index pages
                r'/\d+$',  # trailing numbers
                r'[?&].*$',  # query parameters
            ]
            
            for pattern in remove_patterns:
                keywords_source = re.sub(pattern, '', keywords_source)
            
            # Replace separators with spaces and clean up
            keywords = keywords_source.replace('-', ' ').replace('/', ' ').replace('_', ' ')
            keywords = ' '.join(keywords.split()).strip()  # Remove extra spaces
            
            # Convert to title case for better display
            keywords = keywords.title()
            
            # If we have no meaningful keywords, use domain-based fallback
            if not keywords or len(keywords) < 3:
                domain_keywords = domain.replace('.com', '').replace('.org', '').replace('.net', '')
                if domain_keywords and domain_keywords not in ['www', 'news']:
                    keywords = domain_keywords.title() + " News"
                else:
                    keywords = "Current Events"
            
            # Final cleanup: remove any remaining numbers and short words
            keywords = re.sub(r'\b\d+\b', '', keywords)  # Remove standalone numbers
            keywords = ' '.join([word for word in keywords.split() if len(word) > 2])  # Remove short words
            keywords = keywords.strip()
            
            if not keywords:
                keywords = "Breaking News"
            
            print(f"🔍 Extracted topic: {keywords}")
            return keywords
            
        except Exception as e:
            print(f"Error extracting keywords from URL: {e}")
            return "Breaking News"
    
    def analyze_article(self, instance):
        """Start analysis with enhanced UX - URL AWARE VERSION"""
        query = self.url_input.text.strip()
        if not query:
            self.show_message("Please enter a URL or search terms")
            return
        
        # Check if input is a URL and extract keywords
        is_url = False
        original_query = query
        
        if query.startswith(('http://', 'https://', 'www.')):
            is_url = True
            query = self.extract_keywords_from_url(query)
            print(f"🔗 URL detected: {original_query}")
            print(f"🔍 Searching for topic: {query}")
            
            # Show user what we're actually searching for
            self.show_message(f"Analyzing topic: {query}")
            
            # Optional: Update the input field to show the extracted keywords
            # This helps users understand what we're searching for
            self.url_input.text = query
        
        # Use category if specified
        category = getattr(self, 'active_news_category', None)
        
        if self.is_analyzing:
            return
        
        self.is_analyzing = True
        self.analyze_btn.disabled = True
        self.analyze_btn.text = "Analyzing..."
        
        # Show progress card
        self.progress_card.opacity = 1
        
        # Clear previous results
        self.results_layout.clear_widgets()
        
        # Add initial status item with context about what we're analyzing
        if is_url:
            status_text = f"Analyzing: {query}"
            secondary_text = f"From URL: {original_query[:50]}..." if len(original_query) > 50 else f"From URL: {original_query}"
        else:
            category_text = f" (Category: {category})" if category and category != "all" else ""
            status_text = f"Starting {self.active_analysis_type} analysis{category_text}"
            secondary_text = f"Search: {query}"
        
        initial_item = TwoLineListItem(
            text=status_text,
            secondary_text=secondary_text
        )
        self.results_layout.add_widget(initial_item)
        
        # Start analysis process with category
        Clock.schedule_once(lambda dt: self._perform_analysis(query, category), 0.5)
    
    def _perform_analysis(self, query, category=None):
        """Perform analysis with detailed progress updates - URL AWARE"""
        try:
            steps = [
                (20, f"Searching {category if category else 'all'} news..." if not query.startswith('http') else "Analyzing news topic..."),
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
        """Handle analysis completion with category - WITH URL DETECTION & DISPLAY"""
        try:
            # URL detection at the start
            original_query = query
            extracted_topic = None
            is_url = False
            
            if query.startswith(('http://', 'https://', 'www.')):
                is_url = True
                extracted_topic = self.extract_keywords_from_url(query)
                query = extracted_topic
                print(f"🔗 URL detected: {original_query}")
                print(f"🔍 Extracted topic: {extracted_topic}")
            
            # Get real news data with category
            articles = []
            if self.active_analysis_type == "News":
                if category and category != "all":
                    # Use category for top headlines
                    articles = self.news_client.get_top_headlines(
                        category=category, 
                        max_results=5
                    )
                else:
                    # Use search for general queries
                    articles = self.news_client.search_news(query, max_results=5)
            else:
                # For other analysis types, use search
                articles = self.news_client.search_news(query, max_results=5)
            
            if not articles:
                if is_url:
                    self._analysis_error(f"No news found for topic: '{extracted_topic}'. Try different search terms.")
                else:
                    self._analysis_error("No articles found for your search. Try different terms or category.")
                return
            
            # Show API status with URL context if applicable
            api_status = "🔴 Mock Data" if not self.news_client.is_api_available() else "🟢 Real News API"
            
            if is_url:
                self.show_message(f"Using {api_status} | Topic: {extracted_topic}")
            else:
                self.show_message(f"Using {api_status}")
            
            # Extract entities from articles (ONLY ONCE - no duplicates)
            entities = []
            for article in articles:
                # Combine title and content for entity extraction
                text_content = f"{article.get('title', '')} {article.get('description', '')} {article.get('content', '')}"
                if text_content.strip():
                    # Extract entities from article content
                    article_entities = self.news_client.extract_entities(text_content, query)
                    entities.extend(article_entities)
                
                # ALSO include entities that were already extracted by NewsClient during article fetching
                if 'entities' in article and article['entities']:
                    entities.extend(article['entities'])
            
            # Remove duplicates based on entity name and ensure structure
            unique_entities = {}
            for entity in entities:
                name = entity.get('name', '')
                if name and name not in unique_entities:
                    # Ensure entity has basic structure
                    if 'id' not in entity:
                        entity['id'] = f"{name.lower().replace(' ', '_')}_{hash(name) % 10000}"
                    if 'type' not in entity:
                        entity['type'] = 'organization'
                    unique_entities[name] = entity
            
            entities = list(unique_entities.values())
            
            # If no entities found in articles, create some from the query
            if not entities:
                entities = self._create_entities_from_query(query)
            
            # Get LittleSis entities based on the discovered entity names
            entity_names = [entity['name'] for entity in entities if 'name' in entity]
            ls_entities = self.littlesis_client.search_entities(entity_names)
            
            # Ensure LittleSis entities have proper structure
            for entity in ls_entities:
                if 'id' not in entity:
                    name = entity.get('name', 'unknown')
                    entity['id'] = f"ls_{name.lower().replace(' ', '_')}_{hash(name) % 10000}"
            
            entities.extend(ls_entities)
            
            # Final cleanup - ensure all entities have IDs and remove duplicates
            final_entities = []
            seen_ids = set()
            for entity in entities:
                # Ensure ID exists
                if 'id' not in entity:
                    name = entity.get('name', 'unknown')
                    entity['id'] = f"final_{name.lower().replace(' ', '_')}_{hash(name) % 10000}"
                
                # Remove duplicates by ID
                if entity['id'] not in seen_ids:
                    final_entities.append(entity)
                    seen_ids.add(entity['id'])
            
            entities = final_entities
            
            # Get relationships (with better error handling)
            relationships = []
            for entity in entities[:5]:  # Limit to avoid too many API calls
                try:
                    entity_id = entity.get('id')
                    entity_name = entity.get('name', '')
                    if entity_id and entity_name:
                        # Ensure entity_id is properly formatted for LittleSis
                        if isinstance(entity_id, str) and not entity_id.isdigit():
                            # Convert string ID to numeric for consistency
                            entity_id = abs(hash(entity_id)) % 100000
                        
                        connections = self.littlesis_client.get_entity_connections(entity_id, entity_name, max_connections=3)
                        relationships.extend(connections)
                except Exception as e:
                    print(f"Failed to get connections for {entity.get('name', 'unknown')}: {e}")
                    continue
            
            # If no relationships found, create some sample ones
            if not relationships:
                relationships = self._create_sample_relationships(entities)
            
            print(f"DEBUG: Starting analysis with {len(entities)} entities and {len(relationships)} relationships")
            
            # Perform actual analysis with error handling
            try:
                analysis = self.mapper.analyze_network(entities, relationships)
                # Store relationships in analysis for visualization
                analysis['relationships'] = relationships
            except Exception as e:
                print(f"PowerMapper analysis error: {e}")
                # Create a basic analysis result
                analysis = {
                    "summary": {
                        "entity_count": len(entities),
                        "relationship_count": len(relationships),
                        "network_density": 0.0,
                        "connected_components": 1
                    },
                    "centrality": {},
                    "communities": {"communities": [], "modularity": 0.0},
                    "influence_rankings": sorted(entities, key=lambda x: x.get('influence_score', 0), reverse=True),
                    "structural_analysis": {},
                    "key_findings": ["Basic analysis completed", f"Found {len(entities)} entities with {len(relationships)} relationships"],
                    "relationships": relationships
                }
            
            # Store current analysis for visualization
            self.current_analysis = analysis
            
            # Clear loading item and display results with URL context
            self.results_layout.clear_widgets()
            self.display_analysis_results(analysis, articles[0], api_status, 
                                        original_url=original_query if is_url else None,
                                        extracted_topic=extracted_topic if is_url else None)
            
            # Reset UI state
            self.is_analyzing = False
            self.analyze_btn.disabled = False
            self.analyze_btn.text = "Start Analysis"
            
            # Hide progress card after delay
            Clock.schedule_once(lambda dt: setattr(self.progress_card, 'opacity', 0), 2)
            
        except Exception as e:
            print(f"Analysis complete error: {e}")
            import traceback
            traceback.print_exc()
            self._analysis_error(f"Analysis failed: {str(e)}")
    
    def display_analysis_results(self, analysis, article, api_status="🔴 Mock Data", 
                               original_url=None, extracted_topic=None):
        """Display beautiful analysis results with visualizations"""
        
        # Safely extract source information
        source_name = "Unknown"
        try:
            source_data = article.get('source', {})
            if isinstance(source_data, dict):
                source_name = source_data.get('name', 'Unknown')
            else:
                source_name = str(source_data)
        except:
            source_name = "Unknown"
        
        # Show URL context if this was a URL analysis
        if original_url and extracted_topic:
            url_info_item = TwoLineListItem(
                text="🔗 URL Analysis",
                secondary_text=f"From: {original_url[:60]}...",
                bg_color=[0.9, 0.95, 1.0, 1]
            )
            self.results_layout.add_widget(url_info_item)
            
            topic_item = TwoLineListItem(
                text="📋 Extracted Topic",
                secondary_text=extracted_topic,
                bg_color=[0.95, 0.98, 1.0, 1]
            )
            self.results_layout.add_widget(topic_item)
        
        # Article header with API status
        article_item = TwoLineListItem(
            text=article.get('title', 'Analysis Results'),
            secondary_text=f"Source: {source_name} | {api_status}",
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
        
        # Network Visualization Section
        if analysis.get('summary', {}).get('entity_count', 0) > 0:
            viz_header = OneLineListItem(
                text="🌐 Network Visualization",
                bg_color=[0.9, 0.95, 1.0, 1]
            )
            self.results_layout.add_widget(viz_header)
            
            # Create network graph
            entities = analysis.get('influence_rankings', [])
            relationships = analysis.get('relationships', [])
            
            # Entity type distribution
            type_counts = {}
            for entity in entities:
                entity_type = entity.get('type', 'unknown')
                type_counts[entity_type] = type_counts.get(entity_type, 0) + 1
            
            viz_card = MDCard(
                orientation="vertical",
                padding=dp(15),
                size_hint_y=None,
                height=dp(120),
                elevation=2
            )
            
            viz_layout = MDBoxLayout(orientation="horizontal", adaptive_height=True)
            
            for entity_type, count in type_counts.items():
                type_item = MDBoxLayout(
                    orientation="vertical",
                    size_hint_x=None,
                    width=dp(80),
                    spacing=dp(5)
                )
                
                # Color dot for entity type
                colors = {
                    'person': [0.2, 0.8, 0.2, 1],
                    'corporation': [0.8, 0.2, 0.2, 1],
                    'government': [0.2, 0.2, 0.8, 1],
                    'organization': [0.8, 0.8, 0.2, 1]
                }
                color = colors.get(entity_type, [0.5, 0.5, 0.5, 1])
                
                dot = MDLabel(
                    text="●",
                    font_size='20sp',
                    theme_text_color="Custom",
                    text_color=color,
                    halign="center"
                )
                
                count_label = MDLabel(
                    text=f"{count} {entity_type.title()}",
                    font_style="Caption",
                    halign="center",
                    theme_text_color="Secondary"
                )
                
                type_item.add_widget(dot)
                type_item.add_widget(count_label)
                viz_layout.add_widget(type_item)
            
            viz_card.add_widget(viz_layout)
            self.results_layout.add_widget(viz_card)
        
        # Influence Rankings with Visual Indicators
        if analysis['influence_rankings']:
            influencers_header = OneLineListItem(
                text="🏆 Most Influential Entities",
                bg_color=[0.95, 0.98, 0.95, 1]
            )
            self.results_layout.add_widget(influencers_header)
            
            for i, entity in enumerate(analysis['influence_rankings'][:5]):
                score = entity.get('influence_score', 0)
                entity_type = entity.get('type', 'Entity').title()
                
                # Create a visual bar for influence score
                influence_item = MDBoxLayout(
                    orientation="horizontal",
                    adaptive_height=True,
                    padding=dp(10)
                )
                
                # Rank and name
                text_layout = MDBoxLayout(
                    orientation="vertical",
                    size_hint_x=0.6
                )
                
                rank_label = MDLabel(
                    text=f"{i+1}. {entity['name']}",
                    font_style="Body1",
                    theme_text_color="Primary"
                )
                
                type_label = MDLabel(
                    text=entity_type,
                    font_style="Caption",
                    theme_text_color="Secondary"
                )
                
                text_layout.add_widget(rank_label)
                text_layout.add_widget(type_label)
                
                # Influence bar
                bar_layout = MDBoxLayout(
                    orientation="vertical",
                    size_hint_x=0.4,
                    spacing=dp(5)
                )
                
                score_label = MDLabel(
                    text=f"{score:.1f}",
                    font_style="Body2",
                    halign="right",
                    theme_text_color="Primary"
                )
                
                # Visual progress bar
                progress_bg = MDBoxLayout(
                    size_hint_y=None,
                    height=dp(8),
                    md_bg_color=[0.8, 0.8, 0.8, 1],
                    radius=[dp(4), dp(4), dp(4), dp(4)]
                )
                
                progress_fill = MDBoxLayout(
                    size_hint_x=score/100,
                    size_hint_y=1,
                    md_bg_color=[0.2, 0.6, 0.8, 1],
                    radius=[dp(4), dp(4), dp(4), dp(4)]
                )
                
                progress_bg.add_widget(progress_fill)
                bar_layout.add_widget(score_label)
                bar_layout.add_widget(progress_bg)
                
                influence_item.add_widget(text_layout)
                influence_item.add_widget(bar_layout)
                
                # Wrap in a card
                entity_card = MDCard(
                    orientation="vertical",
                    padding=dp(5),
                    size_hint_y=None,
                    height=dp(70),
                    elevation=1
                )
                entity_card.add_widget(influence_item)
                self.results_layout.add_widget(entity_card)
        
        # Network Statistics
        summary = analysis.get('summary', {})
        if summary:
            stats_header = OneLineListItem(text="📊 Network Statistics")
            self.results_layout.add_widget(stats_header)
            
            stats_card = MDCard(
                orientation="horizontal",
                padding=dp(15),
                spacing=dp(20),
                size_hint_y=None,
                height=dp(80),
                elevation=1
            )
            
            stats = [
                (f"👥 {summary.get('entity_count', 0)}", "Entities"),
                (f"🔗 {summary.get('relationship_count', 0)}", "Relationships"),
                (f"🌐 {summary.get('connected_components', 1)}", "Components"),
                (f"📈 {summary.get('network_density', 0):.3f}", "Density")
            ]
            
            for value, label in stats:
                stat_item = MDBoxLayout(orientation="vertical")
                value_label = MDLabel(
                    text=value,
                    font_style="H6",
                    halign="center",
                    theme_text_color="Primary"
                )
                label_label = MDLabel(
                    text=label,
                    font_style="Caption",
                    halign="center",
                    theme_text_color="Secondary"
                )
                stat_item.add_widget(value_label)
                stat_item.add_widget(label_label)
                stats_card.add_widget(stat_item)
            
            self.results_layout.add_widget(stats_card)

        # Key findings
        if analysis.get('key_findings'):
            findings_header = OneLineListItem(text="🔍 Key Findings")
            self.results_layout.add_widget(findings_header)
            
            for finding in analysis['key_findings'][:3]:
                finding_item = OneLineListItem(
                    text=f"✓ {finding}"
                )
                self.results_layout.add_widget(finding_item)

def show_network_visualization(self, instance=None):
        """Show interactive network visualization"""
        if not hasattr(self, 'current_analysis') or not self.current_analysis:
            self.show_message("Run an analysis first to see the network")
            return
        
        # Create visualization dialog
        content = MDBoxLayout(orientation='vertical', size_hint_y=None)
        content.height = 500
        
        # Create network graph
        entities = self.current_analysis.get('influence_rankings', [])
        relationships = self.current_analysis.get('relationships', [])
        
        if entities and relationships:
            network_widget = NetworkGraphWidget(entities, relationships)
            network_widget.size_hint = (1, 0.8)
            content.add_widget(network_widget)
        else:
            # Fallback: show entity distribution
            viz_label = MDLabel(
                text="🌐 Power Network Structure",
                font_style="H6",
                halign="center",
                size_hint_y=None,
                height=40
            )
            content.add_widget(viz_label)
            
            # Show entity type distribution
            type_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, padding=20)
            
            type_counts = {}
            for entity in entities:
                entity_type = entity.get('type', 'unknown')
                type_counts[entity_type] = type_counts.get(entity_type, 0) + 1
            
            for entity_type, count in type_counts.items():
                type_card = MDCard(
                    orientation='vertical',
                    padding=15,
                    size_hint_x=None,
                    width=100,
                    elevation=2
                )
                
                type_label = MDLabel(
                    text=entity_type.title(),
                    font_style="Body2",
                    halign="center"
                )
                count_label = MDLabel(
                    text=str(count),
                    font_style="H5", 
                    halign="center",
                    theme_text_color="Primary"
                )
                
                type_card.add_widget(count_label)
                type_card.add_widget(type_label)
                type_layout.add_widget(type_card)
            
            content.add_widget(type_layout)
        
        viz_dialog = MDDialog(
            title="Network Visualization",
            type="custom",
            content_cls=content,
            size_hint=(0.9, 0.8),
            buttons=[
                MDFlatButton(
                    text="Close",
                    theme_text_color="Custom",
                    text_color=[0.5, 0.5, 0.5, 1],
                    on_release=lambda x: viz_dialog.dismiss()
                ),
            ],
        )
        viz_dialog.open()
    
    def set_analysis_type(self, button, analysis_type):
        """Set the active analysis type"""
        # Reset all buttons
        for btn in self.analysis_buttons:
            btn.md_bg_color = [1, 1, 1, 0]  # Transparent background
            btn.text_color = [0.5, 0.5, 0.5, 1]
            btn.line_color = [0.8, 0.8, 0.8, 1]
        
        # Set active button
        button.md_bg_color = [0.2, 0.6, 0.8, 1]
        button.text_color = [1, 1, 1, 1]
        button.line_color = [0.2, 0.6, 0.8, 1]
        self.active_analysis_type = analysis_type
        self.top_bar.title = f"{analysis_type} Analysis"
    
    def set_news_category(self, button, category):
        """Set the active news category"""
        # Reset all category buttons
        for btn in self.category_buttons:
            btn.text_color = [0.5, 0.5, 0.5, 1]
            btn.line_color = [0.8, 0.8, 0.8, 1]
        
        # Set active category button
        button.text_color = [0.2, 0.6, 0.8, 1]
        button.line_color = [0.2, 0.6, 0.8, 1]
        self.active_news_category = category.lower() if category != "All" else None
    
    def update_progress(self, value, status):
        """Update progress with animation"""
        self.progress_value = value
        self.status_text = status
        self.status_label.text = status
    
    def load_sample_data(self, instance=None):
        """Load sample data with enhanced UX"""
        self.url_input.text = "technology sector influence"
        self.analyze_article(None)
    
    def _create_entities_from_query(self, query):
        """Create basic entities from search query when no entities are found"""
        entities = []
        # Simple entity extraction from query words
        important_words = [word for word in query.split() if len(word) > 3]
        for word in important_words[:5]:  # Limit to 5 entities
            entities.append({
                'name': word.title(),
                'type': 'Organization',  # Default type
                'id': f"query_{word.lower()}",
                'description': f"Entity mentioned in search: {query}"
            })
        return entities
    
    def _create_sample_relationships(self, entities):
        """Create sample relationships when no real ones are found - FIXED VERSION"""
        relationships = []
        
        if len(entities) < 2:
            return relationships
        
        # Create a small network with the most relevant entities
        for i in range(min(5, len(entities))):
            for j in range(i + 1, min(i + 3, len(entities))):
                if i == j:
                    continue
                    
                # Ensure both entities have IDs, generate if missing
                entity1 = entities[i]
                entity2 = entities[j]
                
                # Get or generate IDs for both entities
                entity1_id = entity1.get('id')
                if not entity1_id:
                    entity1_id = f"entity_{i}_{hash(entity1.get('name', str(i)))}"
                    entity1['id'] = entity1_id
                
                entity2_id = entity2.get('id') 
                if not entity2_id:
                    entity2_id = f"entity_{j}_{hash(entity2.get('name', str(j)))}"
                    entity2['id'] = entity2_id
                
                # Determine relationship type based on entity types
                type1 = entity1.get('type', 'organization')
                type2 = entity2.get('type', 'organization')
                
                # Create appropriate relationship based on entity types
                if type1 == 'person' and type2 == 'corporation':
                    rel_type = 'board_member'
                    strength = 0.8
                    description = f"{entity1['name']} serves on board of {entity2['name']}"
                elif type1 == 'corporation' and type2 == 'corporation':
                    rel_type = 'partnership'
                    strength = 0.6
                    description = f"{entity1['name']} partners with {entity2['name']}"
                elif type1 == 'government' and type2 == 'corporation':
                    rel_type = 'regulation'
                    strength = 0.7
                    description = f"{entity1['name']} regulates {entity2['name']}"
                elif type1 == 'person' and type2 == 'person':
                    rel_type = 'colleague'
                    strength = 0.5
                    description = f"{entity1['name']} works with {entity2['name']}"
                else:
                    rel_type = 'connected_to'
                    strength = 0.5
                    description = f"{entity1['name']} connected to {entity2['name']}"
                    
                relationships.append({
                    'source': str(entity1_id),
                    'target': str(entity2_id),
                    'type': rel_type,
                    'relationship': rel_type,
                    'description': description,
                    'strength': strength
                })
        
        return relationships
    
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
        
        self.show_message("Analysis failed - please try again")
    
    def show_message(self, message):
        """Show a message to the user"""
        # Simple message display
        print(f"Message: {message}")
    
    def go_back(self):
        """Return to welcome screen"""
        self.manager.current = 'welcome'
    
    def show_help(self):
        """Show help dialog"""
        help_dialog = MDDialog(
            title="How to Use Krystal",
            text="1. Enter a news URL or search terms\n2. Select analysis type\n3. Choose news category (optional)\n4. View power structure mapping\n5. Explore connections and influence scores\n\nKrystal helps you uncover hidden relationships between powerful entities in news media.",
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
        # Check API status
        api_status = "🔴 Not configured" 
        if self.news_client.is_api_available():
            api_status = "🟢 Connected"
        
        settings_dialog = MDDialog(
            title="Settings & API Status",
            text=f"News API: {api_status}\n\nTo use real news data:\n1. Get API key from newsapi.org\n2. Set NEWS_API_KEY environment variable\n3. Restart the application",
            buttons=[
                MDFlatButton(
                    text="Close",
                    theme_text_color="Custom",
                    text_color=[0.2, 0.6, 0.8, 1],
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
        print("🚀 Krystal app started with News API integration!")
        
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