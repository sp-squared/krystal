"""
Krystal Mobile Application - Modern Power Structure Mapping Interface
GPL v3
"""

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import math

# KivyMD Components
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.dialog import MDDialog

# Core functionality
from krystal.power_mapper import PowerMapper
from krystal.data_sources import LittleSisClient, NewsClient


class NetworkGraphWidget(Widget):
    """Interactive network graph visualization"""
    
    def __init__(self, entities, relationships, **kwargs):
        super().__init__(**kwargs)
        self.entities = entities
        self.relationships = relationships
        self.node_positions = {}
        self.bind(size=self._update_graph, pos=self._update_graph)
        
    def _update_graph(self, *args):
        self.canvas.clear()
        self._draw_network()
        
    def _draw_network(self):
        if not self.entities or not self.relationships:
            # Only draw background if there's no content
            with self.canvas:
                Color(1, 1, 1, 1)  # White background
                Rectangle(pos=self.pos, size=self.size)
            return
            
        center_x = self.center_x
        center_y = self.center_y
        radius = min(self.width, self.height) * 0.35
        num_nodes = len(self.entities)
        
        with self.canvas:
            # Draw white background first
            Color(1, 1, 1, 1)  # White background
            Rectangle(pos=self.pos, size=self.size)
            
            # Draw relationships (lines)
            for rel in self.relationships:
                source_id = rel.get('source')
                target_id = rel.get('target')
                
                if source_id in self.node_positions and target_id in self.node_positions:
                    src_x, src_y = self.node_positions[source_id]
                    tgt_x, tgt_y = self.node_positions[target_id]
                    
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
                
                entity_type = entity.get('type', 'organization')
                colors = {
                    'person': (0.2, 0.8, 0.2),
                    'corporation': (0.8, 0.2, 0.2),
                    'government': (0.2, 0.2, 0.8),
                    'organization': (0.8, 0.8, 0.2)
                }
                color = colors.get(entity_type, (0.5, 0.5, 0.5))
                
                Color(*color)
                Ellipse(pos=(x-15, y-15), size=(30, 30))
    
    def _draw_network(self):
        if not self.entities or not self.relationships:
            return
            
        center_x = self.center_x
        center_y = self.center_y
        radius = min(self.width, self.height) * 0.35
        num_nodes = len(self.entities)
        
        with self.canvas:
            # Draw relationships first (lines)
            for rel in self.relationships:
                source_id = rel.get('source')
                target_id = rel.get('target')
                
                if source_id in self.node_positions and target_id in self.node_positions:
                    src_x, src_y = self.node_positions[source_id]
                    tgt_x, tgt_y = self.node_positions[target_id]
                    
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
                
                entity_type = entity.get('type', 'organization')
                colors = {
                    'person': (0.2, 0.8, 0.2),
                    'corporation': (0.8, 0.2, 0.2),
                    'government': (0.2, 0.2, 0.8),
                    'organization': (0.8, 0.8, 0.2)
                }
                color = colors.get(entity_type, (0.5, 0.5, 0.5))
                
                Color(*color)
                Ellipse(pos=(x-15, y-15), size=(30, 30))


class WelcomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'welcome'
        self.build_ui()
    
    def build_ui(self):
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding="20dp",
            spacing="20dp"
        )
        
        header_layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp"
        )
        
        self.icon_label = MDIconButton(
            icon="magnify",
            disabled=True,
            size_hint=(None, None),
            size=("64dp", "64dp")
        )
        
        title_layout = MDBoxLayout(
            orientation="vertical",
            spacing="5dp"
        )
        title_label = MDLabel(
            text="KRYSTAL",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height="40dp"
        )
        subtitle_label = MDLabel(
            text="Power Structure Mapper",
            font_style="Subtitle1",
            halign="center",
            size_hint_y=None,
            height="30dp"
        )
        
        title_layout.add_widget(title_label)
        title_layout.add_widget(subtitle_label)
        
        header_layout.add_widget(self.icon_label)
        header_layout.add_widget(title_layout)
    
        features_layout = MDBoxLayout(
            orientation="vertical",
            spacing="15dp"
        )
        
        features_title = MDLabel(
            text="Discover Hidden Connections",
            font_style="H6",
            halign="center",
            size_hint_y=None,
            height="35dp"
        )
        
        features_list = MDBoxLayout(
            orientation="vertical",
            spacing="10dp"
        )
        
        features = [
            ("magnify", "Analyze news articles for power structures"),
            ("chart-box", "Visualize relationship networks"),
            ("office-building", "Track corporate and government ties"),
            ("lock", "Privacy-first, no data collection")
        ]
        
        for icon, text in features:
            feature_item = MDBoxLayout(
                orientation="horizontal",
                spacing="10dp",
                size_hint_y=None,
                height="40dp"
            )
            icon_widget = MDIconButton(
                icon=icon,
                disabled=True,
                size_hint=(None, None),
                size=("40dp", "40dp")
            )
            text_label = MDLabel(
                text=text,
                font_style="Body2"
            )

            feature_item.add_widget(icon_widget)
            feature_item.add_widget(text_label)
            features_list.add_widget(feature_item)
        
        features_layout.add_widget(features_title)
        features_layout.add_widget(features_list)

        action_layout = MDBoxLayout(
            orientation="vertical",
            padding="20dp",
            spacing="15dp"
        )
        
        self.start_button = MDRaisedButton(
            text="Start Analysis",
            size_hint=(1, None),
            height="48dp"
        )
        self.start_button.bind(on_press=self.start_analysis)
        
        sample_button = MDFlatButton(
            text="Try Sample Data",
            size_hint=(1, None),
            height="48dp"
        )
        sample_button.bind(on_press=self.show_sample)
        
        action_layout.add_widget(self.start_button)
        action_layout.add_widget(sample_button)
        
        main_layout.add_widget(header_layout)
        main_layout.add_widget(features_layout)
        main_layout.add_widget(action_layout)
        
        self.add_widget(main_layout)
    
    def start_analysis(self, instance):
        self.manager.current = 'analysis'
    
    def show_sample(self, instance):
        sample_dialog = MDDialog(
            title="Sample Analysis",
            text="This will load a demonstration with sample power structure data.",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda x: sample_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Load Sample",
                    on_release=lambda x: self.load_sample_data(sample_dialog)
                ),
            ],
        )
        sample_dialog.open()
    
    def load_sample_data(self, dialog):
        dialog.dismiss()
        self.manager.current = 'analysis'
        analysis_screen = self.manager.get_screen('analysis')
        Clock.schedule_once(lambda dt: analysis_screen.load_sample_data(), 0.5)


class AnalysisScreen(MDScreen):
    progress_value = NumericProperty(0)
    status_text = StringProperty("Ready to analyze power structures")
    is_analyzing = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "analysis"
        
        self.mapper = PowerMapper()
        self.news_client = NewsClient()
        self.littlesis_client = LittleSisClient()
        
        self.active_analysis_type = "News"
        self.active_news_category = None
        self.current_analysis = None
        Clock.schedule_once(lambda dt: self.build_ui(), 0.1)
    
    def build_ui(self):
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding="0dp",
            spacing="0dp"
        )
        
        self.top_bar = MDTopAppBar(
            title="Power Analysis",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[
                ["chart-box", lambda x: self.show_network_visualization()],
                ["help", lambda x: self.show_help()],
            ]
        )
        main_layout.add_widget(self.top_bar)
        
        # Static Content Section - Inputs, buttons, and progress
        static_content = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height="380dp",  # Fixed height for static content
            padding="16dp",
            spacing="16dp"
        )
        
        # Input Section
        input_layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            size_hint_y=None,
            height="260dp"
        )
        
        input_title = MDLabel(
            text="Analyze Power Structures",
            font_style="H6",
            size_hint_y=None,
            height="32dp"
        )
        
        self.url_input = MDTextField(
            hint_text="Enter news URL or search terms...",
            icon_left="magnify",
            size_hint_y=None,
            height="48dp"
        )
        
        analysis_layout = MDBoxLayout(
            orientation="horizontal",
            spacing="6dp",
            size_hint_y=None,
            height="40dp"
        )
        analysis_types = ["News", "Organization", "Person", "Topic"]
        
        self.analysis_buttons = []
        for text in analysis_types:
            btn = MDRaisedButton(
                text=text,
                size_hint_x=None,
                width="90dp"
            )
            btn.bind(on_release=lambda x, t=text: self.set_analysis_type(x, t))
            analysis_layout.add_widget(btn)
            self.analysis_buttons.append(btn)
        
        if self.analysis_buttons:
            self.set_analysis_type(self.analysis_buttons[0], "News")
        
        category_layout = MDBoxLayout(
            orientation="horizontal",
            spacing="6dp",
            size_hint_y=None,
            height="40dp"
        )
        category_label = MDLabel(
            text="Category:",
            size_hint_x=None,
            width="70dp"
        )
        category_layout.add_widget(category_label)
        
        self.category_buttons = []
        categories = ["All", "Technology", "Business", "Politics"]
        
        for category in categories:
            btn = MDRaisedButton(
                text=category,
                size_hint_x=None,
                width="90dp"
            )
            btn.bind(on_release=lambda x, c=category: self.set_news_category(x, c))
            category_layout.add_widget(btn)
            self.category_buttons.append(btn)
        
        if self.category_buttons:
            self.set_news_category(self.category_buttons[0], "All")
        
        button_layout = MDBoxLayout(
            orientation="horizontal",
            spacing="10dp",
            size_hint_y=None,
            height="48dp"
        )
        
        self.analyze_btn = MDRaisedButton(
            text="Start Analysis",
            on_release=self.analyze_article,
            size_hint_x=0.7
        )
        
        sample_btn = MDFlatButton(
            text="Quick Sample",
            on_release=lambda x: self.load_sample_data(),
            size_hint_x=0.3
        )
        
        button_layout.add_widget(self.analyze_btn)
        button_layout.add_widget(sample_btn)
        
        input_layout.add_widget(input_title)
        input_layout.add_widget(self.url_input)
        input_layout.add_widget(analysis_layout)
        input_layout.add_widget(category_layout)
        input_layout.add_widget(button_layout)
        static_content.add_widget(input_layout)
        
        # Progress Section - Also static
        self.progress_layout = MDBoxLayout(
            orientation="vertical",
            spacing="6dp",
            size_hint_y=None,
            height="80dp"
        )
        self.progress_layout.opacity = 0  # Initially hidden
        
        progress_title = MDLabel(
            text="Analysis Progress",
            font_style="H6",
            size_hint_y=None,
            height="24dp"
        )
        
        self.status_label = MDLabel(
            text=self.status_text,
            size_hint_y=None,
            height="24dp"
        )
        
        self.progress_bar = MDProgressBar(value=self.progress_value)
        
        self.progress_layout.add_widget(progress_title)
        self.progress_layout.add_widget(self.status_label)
        self.progress_layout.add_widget(self.progress_bar)
        static_content.add_widget(self.progress_layout)
        
        # Add static content to main layout
        main_layout.add_widget(static_content)
        
        # Scrollable Content Section - Only Analysis Results
        self.content_scroll = MDScrollView(
            size_hint=(1, 1)  # Take all remaining space
        )
        self.content_layout = MDBoxLayout(
            orientation="vertical", 
            size_hint_y=None,
            padding="16dp",
            spacing="16dp",
            height="800dp"  # Initial height
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        # Results Section Title (scrollable)
        results_title = MDLabel(
            text="Analysis Results",
            font_style="H6",
            size_hint_y=None,
            height="32dp"
        )
        self.content_layout.add_widget(results_title)
        
        self.results_container = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            height="200dp"  # Initial minimal height
        )
        self.content_layout.add_widget(self.results_container)
        
        self.content_scroll.add_widget(self.content_layout)
        main_layout.add_widget(self.content_scroll)
        
        self.add_widget(main_layout)
    
    def show_network_visualization(self, instance=None):
        if not hasattr(self, 'current_analysis') or not self.current_analysis:
            self.show_message("Run an analysis first to see the network")
            return
        
        content = BoxLayout(
            orientation='vertical',
            padding='10dp'
        )
        
        entities = self.current_analysis.get('influence_rankings', [])
        relationships = self.current_analysis.get('relationships', [])
        
        if entities and relationships:
            network_widget = NetworkGraphWidget(entities, relationships)
            content.add_widget(network_widget)
        else:
            viz_label = Label(text="Power Network Structure")
            content.add_widget(viz_label)
        
        popup = Popup(
            title='Network Visualization',
            content=content,
            size_hint=(0.9, 0.8),
            auto_dismiss=True
        )
        
        # Clean up when popup is dismissed
        popup.bind(on_dismiss=lambda x: self._cleanup_popup(content))
        popup.open()

    def _cleanup_popup(self, content):
        """Clean up popup content to prevent rendering artifacts"""
        content.clear_widgets()

    def extract_keywords_from_url(self, url: str) -> str:
        try:
            if '://' in url:
                url = url.split('://', 1)[1]
            
            if url.startswith('www.'):
                url = url[4:]
            
            if '/' in url:
                domain, path = url.split('/', 1)
            else:
                domain, path = url, ""
            
            import re
            keywords_source = re.sub(r'\d{4}[-/]\d{2}[-/]\d{2}', '', path)
            keywords = keywords_source.replace('-', ' ').replace('/', ' ').replace('_', ' ')
            keywords = ' '.join(keywords.split()).strip()
            keywords = keywords.title()
            
            if not keywords or len(keywords) < 3:
                domain_keywords = domain.replace('.com', '').replace('.org', '').replace('.net', '')
                if domain_keywords and domain_keywords not in ['www', 'news']:
                    keywords = domain_keywords.title() + " News"
                else:
                    keywords = "Current Events"
            
            keywords = re.sub(r'\b\d+\b', '', keywords)
            keywords = ' '.join([word for word in keywords.split() if len(word) > 2])
            keywords = keywords.strip()
            
            if not keywords:
                keywords = "Breaking News"
            
            return keywords
            
        except Exception as e:
            return "Breaking News"
    
    def analyze_article(self, instance):
        query = self.url_input.text.strip()
        if not query:
            self.show_message("Please enter a URL or search terms")
            return
        
        is_url = False
        original_query = query
        
        if query.startswith(('http://', 'https://', 'www.')):
            is_url = True
            query = self.extract_keywords_from_url(query)
            self.show_message(f"Analyzing topic: {query}")
            self.url_input.text = query
        
        category = getattr(self, 'active_news_category', None)
        
        if self.is_analyzing:
            return
        
        self.is_analyzing = True
        self.analyze_btn.disabled = True
        self.analyze_btn.text = "Analyzing..."
        
        # Show progress in static area
        self.progress_layout.opacity = 1
        
        self.results_container.clear_widgets()
        
        if is_url:
            status_text = f"Analyzing: {query}"
            secondary_text = f"From URL: {original_query}"
        else:
            status_text = f"Starting {self.active_analysis_type} analysis"
            secondary_text = f"Search: {query}"
        
        initial_item = TwoLineListItem(text=status_text, secondary_text=secondary_text)
        self.results_container.add_widget(initial_item)
        
        # Auto-scroll to show progress
        self.content_scroll.scroll_y = 1.0
        
        Clock.schedule_once(lambda dt: self._perform_analysis(query, category), 0.5)
    
    def _perform_analysis(self, query, category=None):
        try:
            steps = [
                (20, "Searching news..."),
                (40, "Extracting entities..."),
                (60, "Mapping relationships..."),
                (80, "Analyzing power structures..."),
                (95, "Finalizing results..."),
                (100, "Analysis complete!")
            ]
            
            def update_step(step_index):
                if step_index < len(steps):
                    progress, status = steps[step_index]
                    self.update_progress(progress, status)
                    
                    if step_index > 0:
                        self.results_container.children[0].text = status
                        self.results_container.children[0].secondary_text = f"Progress: {progress}%"
                    
                    Clock.schedule_once(lambda dt: update_step(step_index + 1), 1)
                else:
                    self._analysis_complete(query, category)
        
            update_step(0)
            
        except Exception as e:
            self._analysis_error(str(e))
    
    def _analysis_complete(self, query, category=None):
        try:
            original_query = query
            extracted_topic = None
            is_url = False
            
            if query.startswith(('http://', 'https://', 'www.')):
                is_url = True
                extracted_topic = self.extract_keywords_from_url(query)
                query = extracted_topic
            
            articles = []
            if self.active_analysis_type == "News":
                if category and category != "all":
                    articles = self.news_client.get_top_headlines(category=category, max_results=5)
                else:
                    articles = self.news_client.search_news(query, max_results=5)
            else:
                articles = self.news_client.search_news(query, max_results=5)
            
            if not articles:
                self._analysis_error("No articles found for your search.")
                return
            
            api_status = "[MOCK] Mock Data" if not self.news_client.is_api_available() else "[LIVE] Real News API"
            
            entities = []
            for article in articles:
                text_content = f"{article.get('title', '')} {article.get('description', '')} {article.get('content', '')}"
                if text_content.strip():
                    article_entities = self.news_client.extract_entities(text_content, query)
                    entities.extend(article_entities)
                
                if 'entities' in article and article['entities']:
                    entities.extend(article['entities'])
            
            unique_entities = {}
            for entity in entities:
                name = entity.get('name', '')
                if name and name not in unique_entities:
                    if 'id' not in entity:
                        entity['id'] = f"{name.lower().replace(' ', '_')}_{hash(name) % 10000}"
                    if 'type' not in entity:
                        entity['type'] = 'organization'
                    unique_entities[name] = entity
            
            entities = list(unique_entities.values())
            
            if not entities:
                entities = self._create_entities_from_query(query)
            
            entity_names = [entity['name'] for entity in entities if 'name' in entity]
            ls_entities = self.littlesis_client.search_entities(entity_names)
            
            for entity in ls_entities:
                if 'id' not in entity:
                    name = entity.get('name', 'unknown')
                    entity['id'] = f"ls_{name.lower().replace(' ', '_')}_{hash(name) % 10000}"
            
            entities.extend(ls_entities)
            
            final_entities = []
            seen_ids = set()
            for entity in entities:
                if 'id' not in entity:
                    name = entity.get('name', 'unknown')
                    entity['id'] = f"final_{name.lower().replace(' ', '_')}_{hash(name) % 10000}"
                
                if entity['id'] not in seen_ids:
                    final_entities.append(entity)
                    seen_ids.add(entity['id'])
            
            entities = final_entities
            
            relationships = []
            for entity in entities[:5]:
                try:
                    entity_id = entity.get('id')
                    entity_name = entity.get('name', '')
                    if entity_id and entity_name:
                        if isinstance(entity_id, str) and not entity_id.isdigit():
                            entity_id = abs(hash(entity_id)) % 100000
                        
                        connections = self.littlesis_client.get_entity_connections(entity_id, entity_name, max_connections=3)
                        relationships.extend(connections)
                except Exception as e:
                    continue
            
            if not relationships:
                relationships = self._create_sample_relationships(entities)
            
            try:
                analysis = self.mapper.analyze_network(entities, relationships)
                analysis['relationships'] = relationships
            except Exception as e:
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
            
            self.current_analysis = analysis
            
            self.results_container.clear_widgets()
            self.display_analysis_results(analysis, articles[0], api_status)
            
            self.is_analyzing = False
            self.analyze_btn.disabled = False
            self.analyze_btn.text = "Start Analysis"
            
            def remove_progress(dt):
                # Just hide the progress instead of removing from layout
                self.progress_layout.opacity = 0
                self.progress_value = 0
                self.status_text = "Ready to analyze power structures"
            
            Clock.schedule_once(remove_progress, 0.5)
            
        except Exception as e:
            self._analysis_error(f"Analysis failed: {str(e)}")
    
    def display_analysis_results(self, analysis, article, api_status="🔴 Mock Data"):
        self.results_container.clear_widgets()
        self.results_container.spacing = "12dp"
        self.results_container.padding = "8dp"
        
        # Auto-scroll to show results
        self.content_scroll.scroll_y = 1.0
        
        source_name = "Unknown"
        try:
            source_data = article.get('source', {})
            if isinstance(source_data, dict):
                source_name = source_data.get('name', 'Unknown')
            else:
                source_name = str(source_data)
        except:
            source_name = "Unknown"
        
        # Calculate total height for results container
        total_results_height = 0
        
        # Header Section - More compact
        header_height = 100
        header_layout = MDBoxLayout(
            orientation="vertical",
            spacing="8dp",
            size_hint_y=None,
            height=header_height
        )
        total_results_height += header_height
        
        title_text = article.get('title', 'Analysis Results')
        if len(title_text) > 60:
            title_text = title_text[:60] + "..."
            
        title_label = MDLabel(
            text=title_text,
            font_style="H6",
            halign="center",
            size_hint_y=None,
            height="50dp"
        )
        
        source_layout = MDBoxLayout(
            orientation="horizontal",
            spacing="8dp",
            size_hint_y=None,
            height="30dp"
        )
        source_label = MDLabel(
            text=f"Source: {source_name}",
            size_hint_x=0.7,
            font_style="Subtitle1"
        )
        api_label = MDLabel(
            text=api_status,
            size_hint_x=0.3,
            font_style="Caption",
            halign="right"
        )
        
        source_layout.add_widget(source_label)
        source_layout.add_widget(api_label)
        header_layout.add_widget(title_label)
        header_layout.add_widget(source_layout)
        
        self.results_container.add_widget(header_layout)
        
        # Add separator
        separator1 = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="1dp"
        )
        with separator1.canvas:
            Color(0.8, 0.8, 0.8, 1)
            Rectangle(pos=separator1.pos, size=separator1.size)
        self.results_container.add_widget(separator1)
        total_results_height += 1
        
        # Network Overview Section
        if analysis.get('summary', {}).get('entity_count', 0) > 0:
            overview_height = 100
            overview_layout = MDBoxLayout(
                orientation="vertical",
                spacing="8dp",
                size_hint_y=None,
                height=overview_height
            )
            total_results_height += overview_height
            
            overview_title = MDLabel(
                text="Network Overview",
                font_style="H6",
                size_hint_y=None,
                height="25dp"
            )
            overview_layout.add_widget(overview_title)
            
            stats_layout = MDBoxLayout(
                orientation="horizontal",
                spacing="12dp",
                size_hint_y=None,
                height="60dp"
            )
            
            summary = analysis.get('summary', {})
            stats_data = [
                ("Entities", f"{summary.get('entity_count', 0)}"),
                ("Relationships", f"{summary.get('relationship_count', 0)}"), 
                ("Components", f"{summary.get('connected_components', 1)}"),
                ("Density", f"{summary.get('network_density', 0):.3f}")
            ]
            
            for label, value in stats_data:
                stat_item = MDBoxLayout(
                    orientation="vertical",
                    spacing="4dp",
                    size_hint_x=0.25
                )
                value_label = MDLabel(
                    text=value,
                    font_style="H6",
                    halign="center"
                )
                label_label = MDLabel(
                    text=label,
                    font_style="Caption",
                    halign="center"
                )
                stat_item.add_widget(value_label)
                stat_item.add_widget(label_label)
                stats_layout.add_widget(stat_item)
            
            overview_layout.add_widget(stats_layout)
            self.results_container.add_widget(overview_layout)
            
            # Add separator
            separator2 = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="1dp"
            )
            with separator2.canvas:
                Color(0.8, 0.8, 0.8, 1)
                Rectangle(pos=separator2.pos, size=separator2.size)
            self.results_container.add_widget(separator2)
            total_results_height += 1
        
        # Entity Distribution Section
        entities = analysis.get('influence_rankings', [])
        if entities:
            distribution_height = 100
            distribution_layout = MDBoxLayout(
                orientation="vertical",
                spacing="8dp",
                size_hint_y=None,
                height=distribution_height
            )
            total_results_height += distribution_height
            
            distribution_title = MDLabel(
                text="Entity Distribution",
                font_style="H6",
                size_hint_y=None,
                height="25dp"
            )
            distribution_layout.add_widget(distribution_title)
            
            type_layout = MDBoxLayout(
                orientation="horizontal",
                spacing="12dp",
                size_hint_y=None,
                height="60dp"
            )
            
            type_counts = {}
            for entity in entities:
                entity_type = entity.get('type', 'unknown')
                type_counts[entity_type] = type_counts.get(entity_type, 0) + 1
            
            for entity_type, count in type_counts.items():
                type_item = MDBoxLayout(
                    orientation="vertical",
                    spacing="4dp",
                    size_hint_x=0.25
                )
                count_label = MDLabel(
                    text=str(count),
                    font_style="H6",
                    halign="center"
                )
                type_label = MDLabel(
                    text=entity_type.title(),
                    font_style="Caption",
                    halign="center"
                )
                type_item.add_widget(count_label)
                type_item.add_widget(type_label)
                type_layout.add_widget(type_item)
            
            distribution_layout.add_widget(type_layout)
            self.results_container.add_widget(distribution_layout)
            
            # Add separator
            separator3 = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="1dp"
            )
            with separator3.canvas:
                Color(0.8, 0.8, 0.8, 1)
                Rectangle(pos=separator3.pos, size=separator3.size)
            self.results_container.add_widget(separator3)
            total_results_height += 1
        
        # Most Influential Entities Section
        if analysis['influence_rankings']:
            influencers_height = 200
            influencers_layout = MDBoxLayout(
                orientation="vertical",
                spacing="8dp",
                size_hint_y=None,
                height=influencers_height
            )
            total_results_height += influencers_height
            
            influencers_title = MDLabel(
                text="Most Influential Entities",
                font_style="H6",
                size_hint_y=None,
                height="25dp"
            )
            influencers_layout.add_widget(influencers_title)
            
            for i, entity in enumerate(analysis['influence_rankings'][:4]):
                score = entity.get('influence_score', 0)
                
                influencer_item = MDBoxLayout(
                    orientation="horizontal",
                    spacing="8dp",
                    size_hint_y=None,
                    height="40dp"
                )
                
                rank_label = MDLabel(
                    text=str(i+1),
                    size_hint_x=0.1,
                    font_style="H6"
                )
                
                info_layout = MDBoxLayout(
                    orientation="vertical",
                    spacing="2dp",
                    size_hint_x=0.7
                )
                name_label = MDLabel(
                    text=entity['name'],
                    font_style="Subtitle1"
                )
                type_label = MDLabel(
                    text=entity.get('type', 'Entity').title(),
                    font_style="Caption"
                )
                info_layout.add_widget(name_label)
                info_layout.add_widget(type_label)
                
                score_layout = MDBoxLayout(
                    orientation="vertical",
                    size_hint_x=0.2
                )
                score_label = MDLabel(
                    text=f"{score:.1f}",
                    font_style="H6",
                    halign="right"
                )
                score_subtitle = MDLabel(
                    text="Score",
                    font_style="Caption",
                    halign="right"
                )
                score_layout.add_widget(score_label)
                score_layout.add_widget(score_subtitle)
                
                influencer_item.add_widget(rank_label)
                influencer_item.add_widget(info_layout)
                influencer_item.add_widget(score_layout)
                influencers_layout.add_widget(influencer_item)
                
                # Add subtle separator between influencer items (except last one)
                if i < min(3, len(analysis['influence_rankings'][:4]) - 1):
                    item_separator = MDBoxLayout(
                        orientation="horizontal",
                        size_hint_y=None,
                        height="1dp"
                    )
                    with item_separator.canvas:
                        Color(0.9, 0.9, 0.9, 1)
                        Rectangle(pos=item_separator.pos, size=item_separator.size)
                    influencers_layout.add_widget(item_separator)
            
            self.results_container.add_widget(influencers_layout)
            
            # Add separator
            separator4 = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="1dp"
            )
            with separator4.canvas:
                Color(0.8, 0.8, 0.8, 1)
                Rectangle(pos=separator4.pos, size=separator4.size)
            self.results_container.add_widget(separator4)
            total_results_height += 1
        
        # Key Insights Section
        if analysis.get('key_findings'):
            num_findings = len(analysis['key_findings'][:2])
            findings_height = 30 + (num_findings * 35) + 8
            findings_layout = MDBoxLayout(
                orientation="vertical",
                spacing="6dp",
                size_hint_y=None,
                height=findings_height
            )
            total_results_height += findings_height
            
            findings_title = MDLabel(
                text="Key Insights",
                font_style="H6",
                size_hint_y=None,
                height="25dp"
            )
            findings_layout.add_widget(findings_title)
            
            for finding in analysis['key_findings'][:2]:
                finding_item = MDBoxLayout(
                    orientation="horizontal",
                    spacing="6dp",
                    size_hint_y=None,
                    height="30dp"
                )
                # Add bullet point
                bullet = MDLabel(
                    text="•",
                    size_hint_x=0.1,
                    font_style="H6"
                )
                finding_label = MDLabel(
                    text=finding,
                    font_style="Body1"
                )
                finding_item.add_widget(bullet)
                finding_item.add_widget(finding_label)
                findings_layout.add_widget(finding_item)
            
            self.results_container.add_widget(findings_layout)
        
        # Update the results container height
        self.results_container.height = total_results_height
        
        # Update the main content layout height to ensure proper scrolling
        total_content_height = (
            32 +   # results title
            total_results_height +
            (5 * 16)  # spacing between sections
        )
        self.content_layout.height = max(800, total_content_height)
    
    def set_analysis_type(self, button, analysis_type):
        for btn in self.analysis_buttons:
            btn.md_bg_color = [1, 1, 1, 0]
        
        button.md_bg_color = [0.2, 0.6, 0.8, 1]
        self.active_analysis_type = analysis_type
        self.top_bar.title = f"{analysis_type} Analysis"
    
    def set_news_category(self, button, category):
        for btn in self.category_buttons:
            btn.md_bg_color = [1, 1, 1, 0]
        
        button.md_bg_color = [0.2, 0.6, 0.8, 1]
        self.active_news_category = category.lower() if category != "All" else None
    
    def update_progress(self, value, status):
        self.progress_value = value
        self.status_text = status
        self.status_label.text = status
    
    def load_sample_data(self, instance=None):
        self.url_input.text = "technology sector influence"
        self.analyze_article(None)
    
    def _create_entities_from_query(self, query):
        entities = []
        important_words = [word for word in query.split() if len(word) > 3]
        for word in important_words[:5]:
            entities.append({
                'name': word.title(),
                'type': 'Organization',
                'id': f"query_{word.lower()}",
                'description': f"Entity mentioned in search: {query}"
            })
        return entities
    
    def _create_sample_relationships(self, entities):
        relationships = []
        
        if len(entities) < 2:
            return relationships
        
        for i in range(min(5, len(entities))):
            for j in range(i + 1, min(i + 3, len(entities))):
                if i == j:
                    continue
                    
                entity1 = entities[i]
                entity2 = entities[j]
                
                entity1_id = entity1.get('id')
                if not entity1_id:
                    entity1_id = f"entity_{i}_{hash(entity1.get('name', str(i)))}"
                    entity1['id'] = entity1_id
                
                entity2_id = entity2.get('id') 
                if not entity2_id:
                    entity2_id = f"entity_{j}_{hash(entity2.get('name', str(j)))}"
                    entity2['id'] = entity2_id
                
                type1 = entity1.get('type', 'organization')
                type2 = entity2.get('type', 'organization')
                
                if type1 == 'person' and type2 == 'corporation':
                    rel_type = 'board_member'
                elif type1 == 'corporation' and type2 == 'corporation':
                    rel_type = 'partnership'
                elif type1 == 'government' and type2 == 'corporation':
                    rel_type = 'regulation'
                elif type1 == 'person' and type2 == 'person':
                    rel_type = 'colleague'
                else:
                    rel_type = 'connected_to'
                    
                relationships.append({
                    'source': str(entity1_id),
                    'target': str(entity2_id),
                    'type': rel_type,
                    'relationship': rel_type,
                    'description': f"{entity1['name']} connected to {entity2['name']}",
                    'strength': 0.5
                })
        
        return relationships
    
    def _analysis_error(self, error_msg):
        self.is_analyzing = False
        self.analyze_btn.disabled = False
        self.analyze_btn.text = "Start Analysis"
        
        # Hide progress
        self.progress_layout.opacity = 0
        self.progress_value = 0
        self.status_text = "Ready to analyze power structures"
        
        self.results_container.clear_widgets()
        error_item = TwoLineListItem(text="Analysis Failed", secondary_text=error_msg)
        self.results_container.add_widget(error_item)
    
    def show_message(self, message):
        print(f"Message: {message}")
    
    def go_back(self):
        self.manager.current = 'welcome'
    
    def show_help(self):
        help_dialog = MDDialog(
            title="How to Use Krystal",
            text="1. Enter a news URL or search terms\n2. Select analysis type\n3. Choose news category (optional)\n4. View power structure mapping\n5. Explore connections and influence scores",
            buttons=[
                MDFlatButton(text="Got it", on_release=lambda x: help_dialog.dismiss()),
            ],
        )
        help_dialog.open()


class KrystalApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
        
        # Fix for button shadow issues
        from kivy.config import Config
        Config.set('graphics', 'multisamples', '0')  # Disable multisampling

    def build(self):
        self.title = "Krystal - Power Structure Mapper"
        Window.clearcolor = (1, 1, 1, 1)
        
        sm = MDScreenManager()
        
        welcome_screen = WelcomeScreen()
        analysis_screen = AnalysisScreen()
        
        sm.add_widget(welcome_screen)
        sm.add_widget(analysis_screen)
        
        return sm
    
    def on_start(self):
        print("Krystal app started!")
        from krystal.data_sources import NewsClient
        news_client = NewsClient()
        if news_client.is_api_available():
            print("News API is available!")
        else:
            print("Using mock news data.")


def main():
    try:
        KrystalApp().run()
    except Exception as e:
        print(f"App error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()