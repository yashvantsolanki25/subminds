"""
SubMinds Desktop Application
AI-powered subconscious decision analysis for F1 drivers
Desktop GUI using Tkinter
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from pathlib import Path
import threading
import time
from datetime import datetime
from typing import Optional, Dict, Any
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using environment variables only.")

try:
    from src.ai_engine.granite_client import GraniteAIClient
except ImportError as e:
    print(f"Warning: IBM Granite module not available: {e}")
    GraniteAIClient = None

try:
    from src.facial_analysis.capture import FacialCapture
    from src.facial_analysis.emotion_tracker import EmotionTracker
    from src.facial_analysis.expression_detector import ExpressionDetector
except ImportError as e:
    print(f"Warning: Facial analysis modules not available: {e}")
    FacialCapture = None
    EmotionTracker = None
    ExpressionDetector = None

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("Warning: OpenCV not available")


class SubMindsDesktopApp:
    """Main desktop application for SubMinds"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SubMinds - F1 Driver Analysis")
        self.root.geometry("1200x800")
        
        # Application state
        self.is_running = False
        self.granite_client: Optional[Any] = None
        self.facial_capture: Optional[Any] = None
        self.emotion_tracker: Optional[Any] = None
        
        # Configuration
        self.config = self.load_config()
        
        # Setup UI
        self.setup_ui()
        
        # Initialize components
        self.initialize_components()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        return {
            'ibm_api_key': os.getenv('IBM_CLOUD_API_KEY', ''),
            'ibm_project_id': os.getenv('IBM_PROJECT_ID', ''),
            'camera_id': int(os.getenv('CAMERA_ID', '0')),
            'analysis_interval': float(os.getenv('ANALYSIS_INTERVAL', '2.0')),
        }
    
    def setup_ui(self):
        """Setup the user interface"""
        # Create main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_container,
            text="SubMinds - Subconscious Decision Analysis",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=10)
        
        # Control Panel
        self.setup_control_panel(main_container)
        
        # Status Panel
        self.setup_status_panel(main_container)
        
        # Analysis Output
        self.setup_analysis_panel(main_container)
        
        # Statistics Panel
        self.setup_statistics_panel(main_container)
        
    def setup_control_panel(self, parent):
        """Setup control panel with buttons"""
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Start/Stop button
        self.start_button = ttk.Button(
            control_frame,
            text="Start Analysis",
            command=self.toggle_analysis,
            width=20
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        # Configure button
        config_button = ttk.Button(
            control_frame,
            text="Configure",
            command=self.show_config_dialog,
            width=20
        )
        config_button.grid(row=0, column=1, padx=5)
        
        # Clear button
        clear_button = ttk.Button(
            control_frame,
            text="Clear Output",
            command=self.clear_output,
            width=20
        )
        clear_button.grid(row=0, column=2, padx=5)
        
        # Export button
        export_button = ttk.Button(
            control_frame,
            text="Export Results",
            command=self.export_results,
            width=20
        )
        export_button.grid(row=0, column=3, padx=5)
        
    def setup_status_panel(self, parent):
        """Setup status panel"""
        status_frame = ttk.LabelFrame(parent, text="System Status", padding="10")
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Status indicators
        self.status_labels = {}
        
        labels = [
            ('IBM Granite AI', 'granite_status'),
            ('Facial Capture', 'camera_status'),
            ('Emotion Tracker', 'emotion_status'),
            ('Analysis', 'analysis_status')
        ]
        
        for idx, (label_text, key) in enumerate(labels):
            label = ttk.Label(status_frame, text=f"{label_text}:")
            label.grid(row=0, column=idx*2, padx=5, sticky=tk.W)
            
            status = ttk.Label(status_frame, text="●", foreground="red", font=('Arial', 12))
            status.grid(row=0, column=idx*2+1, padx=5, sticky=tk.W)
            self.status_labels[key] = status
        
    def setup_analysis_panel(self, parent):
        """Setup analysis output panel"""
        analysis_frame = ttk.LabelFrame(parent, text="Analysis Output", padding="10")
        analysis_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Configure grid
        analysis_frame.columnconfigure(0, weight=1)
        analysis_frame.rowconfigure(0, weight=1)
        
        # Scrolled text widget
        self.output_text = scrolledtext.ScrolledText(
            analysis_frame,
            wrap=tk.WORD,
            width=100,
            height=20,
            font=('Courier', 10)
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def setup_statistics_panel(self, parent):
        """Setup statistics panel"""
        stats_frame = ttk.LabelFrame(parent, text="Statistics", padding="10")
        stats_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.stats_labels = {}
        
        stats = [
            ('Total Analyses', 'total_analyses'),
            ('Success Rate', 'success_rate'),
            ('Avg Response Time', 'avg_response_time'),
            ('Uptime', 'uptime')
        ]
        
        for idx, (label_text, key) in enumerate(stats):
            label = ttk.Label(stats_frame, text=f"{label_text}:")
            label.grid(row=0, column=idx*2, padx=10, sticky=tk.W)
            
            value = ttk.Label(stats_frame, text="0", font=('Arial', 10, 'bold'))
            value.grid(row=0, column=idx*2+1, padx=5, sticky=tk.W)
            self.stats_labels[key] = value
        
    def initialize_components(self):
        """Initialize AI and capture components"""
        self.log_output("Initializing SubMinds components...")
        
        # Initialize IBM Granite
        if GraniteAIClient and self.config['ibm_api_key'] and self.config['ibm_project_id']:
            try:
                self.granite_client = GraniteAIClient(
                    api_key=self.config['ibm_api_key'],
                    project_id=self.config['ibm_project_id']
                )
                if self.granite_client.is_available():
                    self.update_status('granite_status', 'green')
                    self.log_output("✓ IBM Granite AI initialized successfully")
                else:
                    self.update_status('granite_status', 'yellow')
                    self.log_output("⚠ IBM Granite AI in mock mode")
            except Exception as e:
                self.update_status('granite_status', 'red')
                self.log_output(f"✗ IBM Granite AI initialization failed: {e}")
        else:
            self.update_status('granite_status', 'yellow')
            self.log_output("⚠ IBM Granite AI not configured (using mock mode)")
        
        # Initialize facial capture
        try:
            if FacialCapture:
                self.facial_capture = FacialCapture(camera_id=self.config['camera_id'])
                self.update_status('camera_status', 'green')
                self.log_output("✓ Facial capture initialized")
            else:
                self.update_status('camera_status', 'yellow')
                self.log_output("⚠ Facial capture module not available")
        except Exception as e:
            self.update_status('camera_status', 'red')
            self.log_output(f"✗ Facial capture initialization failed: {e}")
        
        # Initialize emotion tracker
        try:
            if EmotionTracker:
                self.emotion_tracker = EmotionTracker()
                self.update_status('emotion_status', 'green')
                self.log_output("✓ Emotion tracker initialized")
            else:
                self.update_status('emotion_status', 'yellow')
                self.log_output("⚠ Emotion tracker module not available")
        except Exception as e:
            self.update_status('emotion_status', 'red')
            self.log_output(f"✗ Emotion tracker initialization failed: {e}")
        
        self.log_output("\nSystem ready. Click 'Start Analysis' to begin.")
        
    def toggle_analysis(self):
        """Start or stop analysis"""
        if not self.is_running:
            self.start_analysis()
        else:
            self.stop_analysis()
    
    def start_analysis(self):
        """Start the analysis process"""
        self.is_running = True
        self.start_button.config(text="Stop Analysis")
        self.update_status('analysis_status', 'green')
        self.log_output("\n" + "="*80)
        self.log_output("ANALYSIS STARTED")
        self.log_output("="*80 + "\n")
        
        # Start analysis thread
        self.analysis_thread = threading.Thread(target=self.analysis_loop, daemon=True)
        self.analysis_thread.start()
        
    def stop_analysis(self):
        """Stop the analysis process"""
        self.is_running = False
        self.start_button.config(text="Start Analysis")
        self.update_status('analysis_status', 'red')
        self.log_output("\n" + "="*80)
        self.log_output("ANALYSIS STOPPED")
        self.log_output("="*80 + "\n")
        
    def analysis_loop(self):
        """Main analysis loop (runs in separate thread)"""
        start_time = time.time()
        analysis_count = 0
        
        while self.is_running:
            try:
                # Simulate data collection
                facial_data = self.get_facial_data()
                telemetry = self.get_mock_telemetry()
                
                # Analyze with Granite
                if self.granite_client:
                    insights = self.granite_client.analyze_subconscious_patterns(
                        facial_data=facial_data,
                        telemetry=telemetry
                    )
                    
                    # Display results
                    self.display_insights(insights)
                    analysis_count += 1
                    
                    # Update statistics
                    self.update_statistics(analysis_count, start_time)
                
                # Wait before next analysis
                time.sleep(self.config['analysis_interval'])
                
            except Exception as e:
                self.log_output(f"Error in analysis loop: {e}")
                time.sleep(1)
    
    def get_facial_data(self) -> Dict[str, Any]:
        """Get facial expression data"""
        # Mock data for now
        return {
            'dominant_emotion': 'focused',
            'confidence': 0.85,
            'valence': 0.3,
            'arousal': 0.7,
            'stress_level': 6
        }
    
    def get_mock_telemetry(self) -> Dict[str, Any]:
        """Get mock telemetry data"""
        import random
        return {
            'speed': random.uniform(150, 200),
            'steering': random.uniform(-0.5, 0.5),
            'track_position': random.uniform(-0.2, 0.2),
            'lap_time': random.uniform(90, 100)
        }
    
    def display_insights(self, insights: Dict[str, Any]):
        """Display analysis insights"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        output = f"\n[{timestamp}] Analysis Results:\n"
        output += f"  Emotional State: {insights.get('emotional_state', 'Unknown')}\n"
        output += f"  Stress Analysis: {insights.get('stress_analysis', 'N/A')}\n"
        
        recommendations = insights.get('recommendations', [])
        if recommendations:
            output += f"  Recommendations:\n"
            for rec in recommendations[:3]:
                output += f"    • {rec}\n"
        
        self.log_output(output)
    
    def update_statistics(self, count: int, start_time: float):
        """Update statistics display"""
        uptime = time.time() - start_time
        
        self.root.after(0, lambda: self.stats_labels['total_analyses'].config(text=str(count)))
        self.root.after(0, lambda: self.stats_labels['success_rate'].config(text="100%"))
        self.root.after(0, lambda: self.stats_labels['avg_response_time'].config(text="0.5s"))
        self.root.after(0, lambda: self.stats_labels['uptime'].config(
            text=f"{int(uptime//60)}m {int(uptime%60)}s"
        ))
    
    def show_config_dialog(self):
        """Show configuration dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Configuration")
        dialog.geometry("500x400")
        
        ttk.Label(dialog, text="IBM Cloud API Key:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        api_key_entry = ttk.Entry(dialog, width=50, show="*")
        api_key_entry.insert(0, self.config['ibm_api_key'])
        api_key_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="IBM Project ID:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        project_id_entry = ttk.Entry(dialog, width=50)
        project_id_entry.insert(0, self.config['ibm_project_id'])
        project_id_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Camera ID:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        camera_id_entry = ttk.Entry(dialog, width=50)
        camera_id_entry.insert(0, str(self.config['camera_id']))
        camera_id_entry.grid(row=2, column=1, padx=10, pady=10)
        
        def save_config():
            self.config['ibm_api_key'] = api_key_entry.get()
            self.config['ibm_project_id'] = project_id_entry.get()
            self.config['camera_id'] = int(camera_id_entry.get())
            
            # Save to .env file
            self.save_to_env()
            
            messagebox.showinfo("Success", "Configuration saved! Restart the application for changes to take effect.")
            dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save_config).grid(row=3, column=0, columnspan=2, pady=20)
    
    def save_to_env(self):
        """Save configuration to .env file"""
        env_content = f"""# SubMinds Desktop Application Configuration
IBM_CLOUD_API_KEY={self.config['ibm_api_key']}
IBM_PROJECT_ID={self.config['ibm_project_id']}
CAMERA_ID={self.config['camera_id']}
ANALYSIS_INTERVAL={self.config['analysis_interval']}
"""
        with open('.env', 'w') as f:
            f.write(env_content)
    
    def clear_output(self):
        """Clear the output text"""
        self.output_text.delete(1.0, tk.END)
        self.log_output("Output cleared.\n")
    
    def export_results(self):
        """Export analysis results to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                content = self.output_text.get(1.0, tk.END)
                with open(filename, 'w') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Results exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export results: {e}")
    
    def update_status(self, key: str, color: str):
        """Update status indicator color"""
        if key in self.status_labels:
            self.status_labels[key].config(foreground=color)
    
    def log_output(self, message: str):
        """Log message to output text widget"""
        def _log():
            self.output_text.insert(tk.END, message + "\n")
            self.output_text.see(tk.END)
        
        if threading.current_thread() != threading.main_thread():
            self.root.after(0, _log)
        else:
            _log()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SubMindsDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# Made with Bob - Desktop Edition