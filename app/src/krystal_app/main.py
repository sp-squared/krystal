"""
Krystal Mobile Application - Power Structure Mapping Interface
GPL v3
"""

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, ListProperty

# Import our core functionality
from krystal.power_mapper import PowerMapper, create_sample_network
from krystal.data_sources import LittleSisClient, NewsClient


class WelcomeScreen(Screen):
    """Welcome screen with app introduction"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # App logo/icon
        icon = Label(
            text='🔍',
            font_size='64sp',
            size_hint=(1, 0.3)
        )
        layout.add_widget(icon)
        
        # App title
        title = Label(
            text='Krystal',
            font_size='32sp',
            bold=True,
            size_hint=(1, 0.2)
        )
        layout.add_widget(title)
        
        # App description
        description = Label(
            text='Map power structures in news media\n\nReveal connections between corporations,\ngovernment officials, and influential entities',
            font_size='16sp',
            text_size=(Window.width - dp(40), None),
            halign='center',
            valign='middle'
        )
        description.bind(size=description.setter('text_size'))
        layout.add_widget(description)
        
        # Start button
        start_btn = Button(
            text='Start Analysis',
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal='',
            font_size='18sp'
        )
        start_btn.bind(on_press=self.start_analysis)
        layout.add_widget(start_btn)
        
        self.add_widget(layout)
    
    def start_analysis(self, instance):
        """Navigate to analysis screen"""
        self.manager.current = 'analysis'


class AnalysisScreen(Screen):
    """Main analysis screen"""
    
    analysis_result = StringProperty("")
    progress_value = NumericProperty(0)
    status_text = StringProperty("Ready to analyze...")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize core components
        self.mapper = PowerMapper()
        self.news_client = NewsClient()
        self.littlesis_client = LittleSisClient()
        
        self.build_ui()
    
    def build_ui(self):
        """Build the user interface"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        back_btn = Button(
            text='←',
            size_hint=(0.2, 1),
            font_size='20sp'
        )
        back_btn.bind(on_press=self.go_back)
        
        title = Label(
            text='Power Structure Analysis',
            font_size='20sp',
            bold=True,
            size_hint=(0.6, 1)
        )
        
        settings_btn = Button(
            text='⚙️',
            size_hint=(0.2, 1),
            font_size='20sp'
        )
        settings_btn.bind(on_press=self.show_settings)
        
        header.add_widget(back_btn)
        header.add_widget(title)
        header.add_widget(settings_btn)
        main_layout.add_widget(header)
        
        # Input section
        input_section = BoxLayout(orientation='vertical', size_hint=(1, 0.2), spacing=dp(10))
        
        input_label = Label(
            text='Enter news article URL or search terms:',
            font_size='16sp',
            size_hint=(1, 0.3),
            halign='left'
        )
        
        self.url_input = TextInput(
            hint_text='https://example.com/news-article or "tech lobbying"',
            size_hint=(1, 0.4),
            multiline=False,
            padding=dp(10)
        )
        
        input_buttons = BoxLayout(orientation='horizontal', size_hint=(1, 0.3), spacing=dp(10))
        
        analyze_btn = Button(
            text='Analyze Power Structures',
            size_hint=(0.7, 1),
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal=''
        )
        analyze_btn.bind(on_press=self.analyze_article)
        
        sample_btn = Button(
            text='Load Sample',
            size_hint=(0.3, 1),
            background_color=(0.4, 0.4, 0.4, 1),
            background_normal=''
        )
        sample_btn.bind(on_press=self.load_sample_data)
        
        input_buttons.add_widget(analyze_btn)
        input_buttons.add_widget(sample_btn)
        
        input_section.add_widget(input_label)
        input_section.add_widget(self.url_input)
        input_section.add_widget(input_buttons)
        main_layout.add_widget(input_section)
        
        # Progress section
        progress_section = BoxLayout(orientation='vertical', size_hint=(1, 0.1), spacing=dp(5))
        
        self.status_label = Label(
            text=self.status_text,
            font_size='14sp',
            size_hint=(1, 0.5),
            halign='center'
        )
        
        self.progress_bar = ProgressBar(
            value=self.progress_value,
            size_hint=(1, 0.5)
        )
        
        progress_section.add_widget(self.status_label)
        progress_section.add_widget(self.progress_bar)
        main_layout.add_widget(progress_section)
        
        # Results section
        results_section = BoxLayout(orientation='vertical', size_hint=(1, 0.6))
        
        results_label = Label(
            text='Analysis Results:',
            font_size='16sp',
            bold=True,
            size_hint=(1, 0.1),
            halign='left'
        )
        
        # Scrollable results area
        scroll_view = ScrollView(size_hint=(1, 0.9))
        self.results_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(10),
            padding=dp(10)
        )
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        
        scroll_view.add_widget(self.results_layout)
        
        results_section.add_widget(results_label)
        results_section.add_widget(scroll_view)
        main_layout.add_widget(results_section)
        
        self.add_widget(main_layout)
    
    def update_progress(self, value, status):
        """Update progress bar and status"""
        self.progress_value = value
        self.status_text = status
        self.status_label.text = status
    
    def analyze_article(self, instance):
        """Analyze a news article for power structures"""
        query = self.url_input.text.strip()
        if not query:
            self.show_message("Please enter a URL or search terms")
            return
        
        # Clear previous results
        self.results_layout.clear_widgets()
        
        # Start analysis process
        self.update_progress(10, "Starting analysis...")
        
        # Schedule the analysis to run in background
        Clock.schedule_once(lambda dt: self._perform_analysis(query), 0.5)
    
    def _perform_analysis(self, query):
        """Perform the actual analysis (runs in background)"""
        try:
            self.update_progress(30, "Fetching news articles...")
            
            # Get news articles
            articles = self.news_client.search_news(query, max_results=5)
            if not articles:
                self.show_message("No articles found. Try different search terms.")
                self.update_progress(0, "Ready to analyze...")
                return
            
            article = articles[0]
            self.update_progress(50, f"Analyzing: {article['title'][:50]}...")
            
            # Extract entities and relationships
            entities = self.littlesis_client.search_entities(query)
            relationships = []
            
            for entity in entities:
                connections = self.littlesis_client.get_entity_connections(entity['id'])
                relationships.extend(connections)
            
            self.update_progress(80, "Mapping power structures...")
            
            # Analyze the network
            analysis = self.mapper.analyze_network(entities, relationships)
            
            self.update_progress(100, "Analysis complete!")
            
            # Display results
            self.display_analysis_results(analysis, article)
            
            # Reset progress after delay
            Clock.schedule_once(lambda dt: self.update_progress(0, "Ready to analyze..."), 2)
            
        except Exception as e:
            self.show_message(f"Analysis error: {str(e)}")
            self.update_progress(0, "Analysis failed")
    
    def load_sample_data(self, instance):
        """Load sample data for demonstration"""
        self.url_input.text = "technology corporate influence"
        self.update_progress(50, "Loading sample data...")
        
        Clock.schedule_once(lambda dt: self._load_sample_analysis(), 1)
    
    def _load_sample_analysis(self):
        """Perform sample analysis"""
        try:
            # Create sample network
            mapper = create_sample_network()
            analysis = mapper.analyze_network([], [])
            
            # Create mock article
            article = {
                "title": "Sample Analysis: Technology Sector Power Structures",
                "source": "Krystal Demo",
                "published_at": "2024-01-15"
            }
            
            self.update_progress(100, "Sample data loaded!")
            self.display_analysis_results(analysis, article)
            
            Clock.schedule_once(lambda dt: self.update_progress(0, "Ready to analyze..."), 2)
            
        except Exception as e:
            self.show_message(f"Sample data error: {str(e)}")
            self.update_progress(0, "Sample failed")
    
    def display_analysis_results(self, analysis, article):
        """Display analysis results in the UI"""
        # Clear previous results
        self.results_layout.clear_widgets()
        
        # Article info
        article_card = self.create_card()
        article_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80))
        
        article_title = Label(
            text=f"📰 {article['title']}",
            text_size=(Window.width - dp(40), None),
            halign='left',
            size_hint_y=0.6
        )
        
        article_meta = Label(
            text=f"Source: {article.get('source', 'Unknown')} | Published: {article.get('published_at', 'Unknown')}",
            font_size='12sp',
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=0.4
        )
        
        article_layout.add_widget(article_title)
        article_layout.add_widget(article_meta)
        article_card.add_widget(article_layout)
        self.results_layout.add_widget(article_card)
        
        # Summary
        summary_card = self.create_card()
        summary_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100))
        
        summary_title = Label(
            text="📊 Network Summary",
            bold=True,
            size_hint_y=0.3
        )
        
        summary_stats = Label(
            text=f"• {analysis['summary']['entity_count']} Entities\n"
                 f"• {analysis['summary']['relationship_count']} Relationships\n"
                 f"• {analysis['summary']['connected_components']} Network Components\n"
                 f"• Density: {analysis['summary']['network_density']:.3f}",
            text_size=(Window.width - dp(40), None),
            halign='left',
            size_hint_y=0.7
        )
        
        summary_layout.add_widget(summary_title)
        summary_layout.add_widget(summary_stats)
        summary_card.add_widget(summary_layout)
        self.results_layout.add_widget(summary_card)
        
        # Top influencers
        if analysis['influence_rankings']:
            influencers_card = self.create_card()
            influencers_layout = BoxLayout(orientation='vertical', size_hint_y=None)
            
            influencers_title = Label(
                text="🏆 Most Influential Entities",
                bold=True,
                size_hint_y=None,
                height=dp(30)
            )
            
            influencers_layout.add_widget(influencers_title)
            
            for i, entity in enumerate(analysis['influence_rankings'][:5]):
                influencer_item = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(40)
                )
                
                rank_label = Label(
                    text=f"{i+1}.",
                    size_hint=(0.1, 1),
                    bold=True
                )
                
                name_label = Label(
                    text=entity['name'],
                    text_size=(Window.width * 0.5, None),
                    halign='left',
                    size_hint=(0.6, 1)
                )
                
                score_label = Label(
                    text=f"{entity.get('influence_score', 0):.1f}",
                    size_hint=(0.3, 1),
                    halign='right'
                )
                
                influencer_item.add_widget(rank_label)
                influencer_item.add_widget(name_label)
                influencer_item.add_widget(score_label)
                influencers_layout.add_widget(influencer_item)
            
            influencers_layout.height = dp(30 + (40 * min(5, len(analysis['influence_rankings']))))
            influencers_card.add_widget(influencers_layout)
            self.results_layout.add_widget(influencers_card)
        
        # Key findings
        if analysis.get('key_findings'):
            findings_card = self.create_card()
            findings_layout = BoxLayout(orientation='vertical', size_hint_y=None)
            
            findings_title = Label(
                text="🔍 Key Findings",
                bold=True,
                size_hint_y=None,
                height=dp(30)
            )
            
            findings_layout.add_widget(findings_title)
            
            for finding in analysis['key_findings'][:3]:  # Show top 3 findings
                finding_label = Label(
                    text=f"• {finding}",
                    text_size=(Window.width - dp(40), None),
                    halign='left',
                    size_hint_y=None,
                    height=dp(40)
                )
                findings_layout.add_widget(finding_label)
            
            findings_layout.height = dp(30 + (40 * min(3, len(analysis['key_findings']))))
            findings_card.add_widget(findings_layout)
            self.results_layout.add_widget(findings_card)
    
    def create_card(self):
        """Create a card-like container for results"""
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(10),
            spacing=dp(5)
        )
        
        with card.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            card.rect = Rectangle(pos=card.pos, size=card.size)
        
        card.bind(pos=self.update_rect, size=self.update_rect)
        return card
    
    def update_rect(self, instance, value):
        """Update card background rectangle"""
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def show_message(self, message):
        """Show a message to the user"""
        self.results_layout.clear_widgets()
        message_label = Label(
            text=message,
            font_size='16sp',
            text_size=(Window.width - dp(40), None),
            halign='center',
            valign='middle'
        )
        self.results_layout.add_widget(message_label)
    
    def go_back(self, instance):
        """Return to welcome screen"""
        self.manager.current = 'welcome'
    
    def show_settings(self, instance):
        """Show settings screen (to be implemented)"""
        self.show_message("Settings screen coming soon!")


class KrystalApp(App):
    """Main Kivy application class"""
    
    def build(self):
        self.title = "Krystal - Power Structure Mapper"
        Window.clearcolor = (1, 1, 1, 1)  # White background
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        welcome_screen = WelcomeScreen(name='welcome')
        analysis_screen = AnalysisScreen(name='analysis')
        
        sm.add_widget(welcome_screen)
        sm.add_widget(analysis_screen)
        
        return sm
    
    def on_start(self):
        """Called when the app starts"""
        print("🚀 Krystal app started successfully!")
    
    def on_stop(self):
        """Called when the app stops"""
        print("🛑 Krystal app stopped.")


def main():
    """Main entry point for the application"""
    try:
        KrystalApp().run()
    except Exception as e:
        print(f"❌ App error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()