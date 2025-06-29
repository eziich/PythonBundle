import tkinter as tk
from tkinter import ttk, messagebox
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import threading
import json
import random
import warnings
warnings.filterwarnings('ignore')

class CryptoAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Value Analyzer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Data storage
        self.crypto_data = []
        self.predictions = []
        
        # API endpoints
        self.coingecko_api = "https://api.coingecko.com/api/v3"
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="🚀 Crypto Value Analyzer", 
                              font=("Arial", 24, "bold"), 
                              fg='#00ff88', bg='#2b2b2b')
        title_label.pack(pady=(0, 20))
        
        # Control frame
        control_frame = tk.Frame(main_frame, bg='#2b2b2b')
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Fetch button
        self.fetch_btn = tk.Button(control_frame, text="📊 Fetch Top 3 Cryptocurrencies", 
                                  command=self.fetch_data,
                                  font=("Arial", 12, "bold"),
                                  bg='#00ff88', fg='#2b2b2b',
                                  relief=tk.RAISED, bd=3)
        self.fetch_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Demo data button
        self.demo_btn = tk.Button(control_frame, text="🎮 Load Demo Data", 
                                 command=self.load_demo_data,
                                 font=("Arial", 12, "bold"),
                                 bg='#ff8800', fg='#2b2b2b',
                                 relief=tk.RAISED, bd=3)
        self.demo_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Rate limit warning
        warning_label = tk.Label(control_frame, text="⚠️ If you get error 429, wait 2 minutes between fetch requests", 
                                font=("Arial", 9), 
                                fg='#ffaa00', bg='#2b2b2b')
        warning_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(control_frame, mode='indeterminate')
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Status label
        self.status_label = tk.Label(control_frame, text="Ready to fetch data...", 
                                    font=("Arial", 10), 
                                    fg='#ffffff', bg='#2b2b2b')
        self.status_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_overview_tab()
        self.create_charts_tab()
        self.create_predictions_tab()
        self.create_details_tab()
        
    def create_overview_tab(self):
        overview_frame = tk.Frame(self.notebook, bg='#2b2b2b')
        self.notebook.add(overview_frame, text="📈 Overview")
        
        # Treeview for crypto data
        columns = ('Rank', 'Name', 'Symbol', 'Price (USD)', '24h Change', 'Market Cap', 'Volume')
        self.tree = ttk.Treeview(overview_frame, columns=columns, show='headings', height=10)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(overview_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
    def create_charts_tab(self):
        charts_frame = tk.Frame(self.notebook, bg='#2b2b2b')
        self.notebook.add(charts_frame, text="📊 Charts")
        
        # Charts container
        self.charts_container = tk.Frame(charts_frame, bg='#2b2b2b')
        self.charts_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_predictions_tab(self):
        predictions_frame = tk.Frame(self.notebook, bg='#2b2b2b')
        self.notebook.add(predictions_frame, text="🔮 Predictions")
        
        # Predictions container
        self.predictions_container = tk.Frame(predictions_frame, bg='#2b2b2b')
        self.predictions_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_details_tab(self):
        details_frame = tk.Frame(self.notebook, bg='#2b2b2b')
        self.notebook.add(details_frame, text="📋 Details")
        
        # Details text area
        self.details_text = tk.Text(details_frame, bg='#3b3b3b', fg='#ffffff', 
                                   font=("Consolas", 10), wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=scrollbar.set)
        
        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
    def load_demo_data(self):
        """Load demo data for testing when API is not available"""
        self.status_label.config(text="Loading demo data...")
        
        # Demo cryptocurrency data
        demo_cryptos = [
            {
                'id': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'BTC',
                'current_price': 45000, 'market_cap': 850000000000,
                'volume': 25000000000, 'price_change_24h': 2.5,
                'market_cap_rank': 1
            },
            {
                'id': 'ethereum', 'name': 'Ethereum', 'symbol': 'ETH',
                'current_price': 3200, 'market_cap': 380000000000,
                'volume': 18000000000, 'price_change_24h': 1.8,
                'market_cap_rank': 2
            },
            {
                'id': 'binancecoin', 'name': 'BNB', 'symbol': 'BNB',
                'current_price': 320, 'market_cap': 48000000000,
                'volume': 1200000000, 'price_change_24h': -0.5,
                'market_cap_rank': 3
            },
            {
                'id': 'cardano', 'name': 'Cardano', 'symbol': 'ADA',
                'current_price': 0.45, 'market_cap': 16000000000,
                'volume': 800000000, 'price_change_24h': 3.2,
                'market_cap_rank': 4
            },
            {
                'id': 'solana', 'name': 'Solana', 'symbol': 'SOL',
                'current_price': 95, 'market_cap': 41000000000,
                'volume': 2500000000, 'price_change_24h': 4.1,
                'market_cap_rank': 5
            },
            {
                'id': 'ripple', 'name': 'XRP', 'symbol': 'XRP',
                'current_price': 0.52, 'market_cap': 28000000000,
                'volume': 1500000000, 'price_change_24h': -1.2,
                'market_cap_rank': 6
            },
            {
                'id': 'polkadot', 'name': 'Polkadot', 'symbol': 'DOT',
                'current_price': 7.2, 'market_cap': 9000000000,
                'volume': 400000000, 'price_change_24h': 2.8,
                'market_cap_rank': 7
            },
            {
                'id': 'dogecoin', 'name': 'Dogecoin', 'symbol': 'DOGE',
                'current_price': 0.08, 'market_cap': 11000000000,
                'volume': 600000000, 'price_change_24h': 1.5,
                'market_cap_rank': 8
            },
            {
                'id': 'avalanche', 'name': 'Avalanche', 'symbol': 'AVAX',
                'current_price': 35, 'market_cap': 12000000000,
                'volume': 800000000, 'price_change_24h': 5.2,
                'market_cap_rank': 9
            },
            {
                'id': 'chainlink', 'name': 'Chainlink', 'symbol': 'LINK',
                'current_price': 15, 'market_cap': 8500000000,
                'volume': 500000000, 'price_change_24h': -0.8,
                'market_cap_rank': 10
            }
        ]
        
        # Generate demo historical data
        self.crypto_data = []
        for crypto in demo_cryptos:
            # Generate 30 days of price data
            base_price = crypto['current_price']
            dates = [datetime.now() - timedelta(days=30-i) for i in range(30)]
            prices = []
            
            for i in range(30):
                # Add some realistic price variation
                variation = random.gauss(0, 0.05)  # 5% daily variation
                price = base_price * (1 + variation)
                prices.append(max(price * 0.5, price))  # Ensure price doesn't go too low
            
            crypto_info = {
                'id': crypto['id'],
                'name': crypto['name'],
                'symbol': crypto['symbol'],
                'current_price': crypto['current_price'],
                'market_cap': crypto['market_cap'],
                'volume': crypto['volume'],
                'price_change_24h': crypto['price_change_24h'],
                'market_cap_rank': crypto['market_cap_rank'],
                'dates': dates,
                'prices': prices
            }
            
            self.crypto_data.append(crypto_info)
        
        # Generate predictions
        self.generate_predictions()
        
        # Update UI
        self.update_ui()
        self.status_label.config(text="Demo data loaded successfully!")
        
    def fetch_data(self):
        """Fetch cryptocurrency data in a separate thread"""
        self.fetch_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.status_label.config(text="Fetching data...")
        
        thread = threading.Thread(target=self._fetch_data_thread)
        thread.daemon = True
        thread.start()
        
    def _fetch_data_thread(self):
        """Thread function to fetch data"""
        try:
            # Test API connection first
            self.root.after(0, lambda: self.status_label.config(text="Testing API connection..."))
            
            test_url = f"{self.coingecko_api}/ping"
            test_response = requests.get(test_url, timeout=10)
            
            if test_response.status_code != 200:
                raise Exception(f"API test failed with status code: {test_response.status_code}")
            
            # Fetch top 3 cryptocurrencies (reduced from 10 to avoid rate limiting)
            self.root.after(0, lambda: self.status_label.config(text="Fetching top 3 cryptocurrencies..."))
            
            url = f"{self.coingecko_api}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 3,  # Reduced from 10 to 3
                'page': 1,
                'sparkline': False
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            crypto_list = response.json()
            
            if not crypto_list:
                raise Exception("No cryptocurrency data received from API")
            
            # Fetch historical data for each crypto
            self.crypto_data = []
            for i, crypto in enumerate(crypto_list):
                self.root.after(0, lambda i=i, name=crypto['name']: self.status_label.config(
                    text=f"Fetching data for {name}... ({i+1}/3)"))
                
                try:
                    # Get historical data (1 month)
                    historical_url = f"{self.coingecko_api}/coins/{crypto['id']}/market_chart"
                    hist_params = {
                        'vs_currency': 'usd',
                        'days': 30
                    }
                    
                    hist_response = requests.get(historical_url, params=hist_params, timeout=30)
                    hist_response.raise_for_status()
                    hist_data = hist_response.json()
                    
                    # Process historical data
                    prices = hist_data['prices']
                    dates = [datetime.fromtimestamp(price[0]/1000) for price in prices]
                    prices_usd = [price[1] for price in prices]
                    
                    crypto_info = {
                        'id': crypto['id'],
                        'name': crypto['name'],
                        'symbol': crypto['symbol'].upper(),
                        'current_price': crypto['current_price'],
                        'market_cap': crypto['market_cap'],
                        'volume': crypto['total_volume'],
                        'price_change_24h': crypto['price_change_percentage_24h'],
                        'market_cap_rank': crypto['market_cap_rank'],
                        'dates': dates,
                        'prices': prices_usd
                    }
                    
                    self.crypto_data.append(crypto_info)
                    
                    # Add delay to avoid rate limiting
                    import time
                    time.sleep(1.5)  # Increased from 0.5 to 1.5 seconds
                    
                except Exception as e:
                    if "429" in str(e) or "Too Many Requests" in str(e):
                        error_msg = f"API Rate Limit Exceeded (Status 429)\n\nThis happens when you make too many requests too quickly.\n\nSolutions:\n• Wait 1-2 minutes before trying again\n• Use the 'Load Demo Data' button to see the app\n• Get a free API key from CoinGecko for higher limits"
                    else:
                        error_msg = f"Failed to fetch data: {str(e)}\n\nTry using the 'Load Demo Data' button to see the app in action."
                    self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                    # Continue with other cryptocurrencies
                    continue
            
            if not self.crypto_data:
                raise Exception("Failed to fetch data for any cryptocurrencies")
            
            # Generate predictions
            self.generate_predictions()
            
            # Update UI
            self.root.after(0, self.update_ui)
            
        except Exception as e:
            error_msg = f"Failed to fetch data: {str(e)}\n\nTry using the 'Load Demo Data' button to see the app in action."
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        finally:
            self.root.after(0, self.fetch_complete)
            
    def fetch_complete(self):
        """Called when data fetching is complete"""
        self.fetch_btn.config(state=tk.NORMAL)
        self.progress.stop()
        if self.crypto_data:
            self.status_label.config(text=f"Data fetched successfully! ({len(self.crypto_data)} cryptocurrencies)")
        else:
            self.status_label.config(text="Ready to fetch data...")
        
    def generate_predictions(self):
        """Generate price predictions for each cryptocurrency using simple linear regression"""
        self.predictions = []
        
        for crypto in self.crypto_data:
            try:
                # Simple linear regression implementation
                prices = crypto['prices']
                n = len(prices)
                
                if n < 2:
                    continue
                
                # Calculate linear regression manually
                x = np.arange(n)
                y = np.array(prices)
                
                # Calculate means
                x_mean = np.mean(x)
                y_mean = np.mean(y)
                
                # Calculate slope and intercept
                numerator = np.sum((x - x_mean) * (y - y_mean))
                denominator = np.sum((x - x_mean) ** 2)
                
                if denominator == 0:
                    continue
                    
                slope = numerator / denominator
                intercept = y_mean - slope * x_mean
                
                # Predict next 7 days
                future_x = n + 6  # 7 days ahead
                predicted_7d = slope * future_x + intercept
                
                # Calculate prediction metrics
                current_price = crypto['current_price']
                price_change_7d = ((predicted_7d - current_price) / current_price) * 100
                
                prediction_info = {
                    'crypto_id': crypto['id'],
                    'current_price': current_price,
                    'predicted_7d': predicted_7d,
                    'price_change_7d': price_change_7d,
                    'confidence': min(85, max(50, 100 - abs(price_change_7d) * 2)),  # Simple confidence metric
                    'trend': 'Bullish' if price_change_7d > 0 else 'Bearish'
                }
                
                self.predictions.append(prediction_info)
                
            except Exception as e:
                print(f"Error generating prediction for {crypto['name']}: {e}")
                
    def update_ui(self):
        """Update all UI components with fetched data"""
        self.update_overview_table()
        self.update_charts()
        self.update_predictions()
        self.update_details()
        
    def update_overview_table(self):
        """Update the overview table with crypto data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new data
        for crypto in self.crypto_data:
            self.tree.insert('', tk.END, values=(
                crypto['market_cap_rank'],
                crypto['name'],
                crypto['symbol'],
                f"${crypto['current_price']:,.2f}",
                f"{crypto['price_change_24h']:+.2f}%",
                f"${crypto['market_cap']:,.0f}",
                f"${crypto['volume']:,.0f}"
            ))
            
    def update_charts(self):
        """Update charts with new data"""
        # Clear existing charts
        for widget in self.charts_container.winfo_children():
            widget.destroy()
        
        if not self.crypto_data:
            return
            
        # Create figure with subplots
        fig = Figure(figsize=(15, 10), facecolor='#2b2b2b')
        
        # Price trends subplot
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.set_facecolor('#3b3b3b')
        
        for crypto in self.crypto_data[:3]:  # Show top 3
            ax1.plot(crypto['dates'], crypto['prices'], label=crypto['symbol'], linewidth=2)
        
        ax1.set_title('Price Trends (Last 30 Days)', color='white', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Date', color='white')
        ax1.set_ylabel('Price (USD)', color='white')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(colors='white')
        
        # Market cap pie chart
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.set_facecolor('#3b3b3b')
        
        labels = [crypto['symbol'] for crypto in self.crypto_data]
        sizes = [crypto['market_cap'] for crypto in self.crypto_data]
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
        
        wedges, texts, autotexts = ax2.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                          colors=colors, startangle=90)
        ax2.set_title('Market Cap Distribution', color='white', fontsize=12, fontweight='bold')
        
        # 24h price change bar chart
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.set_facecolor('#3b3b3b')
        
        symbols = [crypto['symbol'] for crypto in self.crypto_data]
        changes = [crypto['price_change_24h'] for crypto in self.crypto_data]
        colors = ['green' if change > 0 else 'red' for change in changes]
        
        bars = ax3.bar(symbols, changes, color=colors, alpha=0.7)
        ax3.set_title('24h Price Change (%)', color='white', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Change (%)', color='white')
        ax3.tick_params(colors='white')
        ax3.grid(True, alpha=0.3)
        
        # Volume comparison
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.set_facecolor('#3b3b3b')
        
        volumes = [crypto['volume'] / 1e9 for crypto in self.crypto_data]  # Convert to billions
        
        bars = ax4.bar(symbols, volumes, color='skyblue', alpha=0.7)
        ax4.set_title('24h Trading Volume (Billions USD)', color='white', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Volume (B USD)', color='white')
        ax4.tick_params(colors='white')
        ax4.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, volume in zip(bars, volumes):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{volume:.1f}B', ha='center', va='bottom', color='white')
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, self.charts_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_predictions(self):
        """Update predictions tab"""
        # Clear existing content
        for widget in self.predictions_container.winfo_children():
            widget.destroy()
        
        if not self.predictions:
            return
            
        # Create predictions figure
        fig = Figure(figsize=(15, 10), facecolor='#2b2b2b')
        
        # Prediction chart
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.set_facecolor('#3b3b3b')
        
        symbols = [pred['crypto_id'].upper() for pred in self.predictions]
        changes = [pred['price_change_7d'] for pred in self.predictions]
        colors = ['green' if change > 0 else 'red' for change in changes]
        
        bars = ax1.bar(symbols, changes, color=colors, alpha=0.7)
        ax1.set_title('7-Day Price Prediction (%)', color='white', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Predicted Change (%)', color='white')
        ax1.tick_params(colors='white')
        ax1.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, change in zip(bars, changes):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + (0.5 if height > 0 else -1),
                    f'{change:+.1f}%', ha='center', va='bottom' if height > 0 else 'top', 
                    color='white', fontweight='bold')
        
        # Confidence levels
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.set_facecolor('#3b3b3b')
        
        confidences = [pred['confidence'] for pred in self.predictions]
        colors = ['green' if conf > 70 else 'orange' if conf > 60 else 'red' for conf in confidences]
        
        bars = ax2.bar(symbols, confidences, color=colors, alpha=0.7)
        ax2.set_title('Prediction Confidence (%)', color='white', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Confidence (%)', color='white')
        ax2.tick_params(colors='white')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 100)
        
        # Add value labels
        for bar, conf in zip(bars, confidences):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{conf:.0f}%', ha='center', va='bottom', color='white', fontweight='bold')
        
        # Current vs Predicted prices
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.set_facecolor('#3b3b3b')
        
        current_prices = [pred['current_price'] for pred in self.predictions]
        predicted_prices = [pred['predicted_7d'] for pred in self.predictions]
        
        x = np.arange(len(symbols))
        width = 0.35
        
        bars1 = ax3.bar(x - width/2, current_prices, width, label='Current Price', color='blue', alpha=0.7)
        bars2 = ax3.bar(x + width/2, predicted_prices, width, label='Predicted Price (7d)', color='orange', alpha=0.7)
        
        ax3.set_title('Current vs Predicted Prices', color='white', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Price (USD)', color='white')
        ax3.set_xticks(x)
        ax3.set_xticklabels(symbols)
        ax3.legend()
        ax3.tick_params(colors='white')
        ax3.grid(True, alpha=0.3)
        
        # Trend distribution pie chart
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.set_facecolor('#3b3b3b')
        
        bullish_count = sum(1 for pred in self.predictions if pred['trend'] == 'Bullish')
        bearish_count = len(self.predictions) - bullish_count
        
        trend_labels = ['Bullish', 'Bearish']
        trend_sizes = [bullish_count, bearish_count]
        trend_colors = ['green', 'red']
        
        wedges, texts, autotexts = ax4.pie(trend_sizes, labels=trend_labels, autopct='%1.1f%%', 
                                          colors=trend_colors, startangle=90)
        ax4.set_title('Prediction Trends Distribution', color='white', fontsize=12, fontweight='bold')
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, self.predictions_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_details(self):
        """Update details tab with comprehensive information"""
        self.details_text.delete(1.0, tk.END)
        
        if not self.crypto_data:
            self.details_text.insert(tk.END, "No data available. Please fetch cryptocurrency data first.")
            return
            
        # Generate detailed report
        report = "🚀 CRYPTO VALUE ANALYZER - DETAILED REPORT\n"
        report += "=" * 60 + "\n\n"
        report += f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Total Cryptocurrencies Analyzed: {len(self.crypto_data)}\n\n"
        
        # Market summary
        total_market_cap = sum(crypto['market_cap'] for crypto in self.crypto_data)
        total_volume = sum(crypto['volume'] for crypto in self.crypto_data)
        
        report += "📊 MARKET SUMMARY\n"
        report += "-" * 30 + "\n"
        report += f"Total Market Cap: ${total_market_cap:,.0f}\n"
        report += f"Total 24h Volume: ${total_volume:,.0f}\n"
        report += f"Average 24h Change: {np.mean([crypto['price_change_24h'] for crypto in self.crypto_data]):+.2f}%\n\n"
        
        # Individual crypto details
        report += "💰 INDIVIDUAL CRYPTOCURRENCY ANALYSIS\n"
        report += "-" * 50 + "\n\n"
        
        for i, crypto in enumerate(self.crypto_data, 1):
            report += f"{i}. {crypto['name']} ({crypto['symbol']})\n"
            report += f"   Rank: #{crypto['market_cap_rank']}\n"
            report += f"   Current Price: ${crypto['current_price']:,.2f}\n"
            report += f"   Market Cap: ${crypto['market_cap']:,.0f}\n"
            report += f"   24h Volume: ${crypto['volume']:,.0f}\n"
            report += f"   24h Change: {crypto['price_change_24h']:+.2f}%\n"
            
            # Price statistics
            prices = crypto['prices']
            min_price = min(prices)
            max_price = max(prices)
            avg_price = np.mean(prices)
            
            report += f"   30-Day Low: ${min_price:,.2f}\n"
            report += f"   30-Day High: ${max_price:,.2f}\n"
            report += f"   30-Day Average: ${avg_price:,.2f}\n"
            report += f"   Volatility: {((max_price - min_price) / avg_price * 100):.1f}%\n\n"
        
        # Predictions summary
        if self.predictions:
            report += "🔮 PREDICTION SUMMARY\n"
            report += "-" * 30 + "\n"
            
            bullish_predictions = [pred for pred in self.predictions if pred['trend'] == 'Bullish']
            bearish_predictions = [pred for pred in self.predictions if pred['trend'] == 'Bearish']
            
            report += f"Bullish Predictions: {len(bullish_predictions)}/{len(self.predictions)}\n"
            report += f"Bearish Predictions: {len(bearish_predictions)}/{len(self.predictions)}\n"
            report += f"Average Confidence: {np.mean([pred['confidence'] for pred in self.predictions]):.1f}%\n\n"
            
            report += "📈 TOP PREDICTIONS\n"
            report += "-" * 20 + "\n"
            
            # Sort by predicted change
            sorted_predictions = sorted(self.predictions, key=lambda x: abs(x['price_change_7d']), reverse=True)
            
            for pred in sorted_predictions[:5]:
                crypto_name = next(crypto['name'] for crypto in self.crypto_data if crypto['id'] == pred['crypto_id'])
                report += f"• {crypto_name}: {pred['price_change_7d']:+.1f}% (Confidence: {pred['confidence']:.0f}%)\n"
        
        # Risk assessment
        report += "\n⚠️ RISK ASSESSMENT\n"
        report += "-" * 20 + "\n"
        
        high_volatility = [crypto for crypto in self.crypto_data 
                          if abs(crypto['price_change_24h']) > 10]
        
        if high_volatility:
            report += f"High Volatility Assets ({len(high_volatility)}):\n"
            for crypto in high_volatility:
                report += f"  - {crypto['name']}: {crypto['price_change_24h']:+.2f}%\n"
        else:
            report += "No extremely volatile assets detected.\n"
        
        report += "\n💡 RECOMMENDATIONS\n"
        report += "-" * 20 + "\n"
        report += "• This analysis is for informational purposes only\n"
        report += "• Always do your own research before investing\n"
        report += "• Consider diversifying your portfolio\n"
        report += "• Monitor market conditions regularly\n"
        report += "• Past performance doesn't guarantee future results\n"
        
        self.details_text.insert(tk.END, report)

def main():
    root = tk.Tk()
    app = CryptoAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main() 