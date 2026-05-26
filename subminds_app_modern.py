"""
SubMinds Desktop Application - Modern UI Version
AI-powered subconscious decision analysis with enhanced UX
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk, ImageDraw, ImageFont
import threading
import time
from datetime import datetime
from typing import Optional, Dict, Any

# Try to import required modules
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("WARNING: OpenCV not installed")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("WARNING: python-dotenv not installed")

# Add src to path
sys.path.insert(0, str(os.path.join(os.path.dirname(__file__), 'src')))

try:
    from src.ai_engine.granite_client import GraniteAIClient
    GRANITE_AVAILABLE = True
except ImportError:
    GRANITE_AVAILABLE = False

try:
    from src.facial_analysis.expression_detector import ExpressionDetector
    FACE_DETECTION_AVAILABLE = True
except ImportError:
    FACE_DETECTION_AVAILABLE = False


class ModernSubMindsApp:
    """Modern desktop application with enhanced UI/UX"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SubMinds AI - Emotion Analysis System")
        self.root.geometry("1600x950")
        self.root.configure(bg='#1a1a2e')
        
        # Application state
        self.is_running = False
        self.camera = None
        self.granite_client = None
        self.face_detector = None
        self.analysis_count = 0
        self.start_time = None
        self.current_frame = None
        self.camera_canvas = None
        
        # Create captures directory
        self.captures_dir = os.path.join(os.path.dirname(__file__), 'captures')
        os.makedirs(self.captures_dir, exist_ok=True)
        
        # Configuration
        self.config = {
            'ibm_api_key': os.getenv('IBM_CLOUD_API_KEY', ''),
            'ibm_project_id': os.getenv('IBM_PROJECT_ID', ''),
            'camera_id': int(os.getenv('CAMERA_ID', '0')),
            'analysis_interval': float(os.getenv('ANALYSIS_INTERVAL', '2.0')),
        }
        
        # Colors
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent': '#e94560',
            'accent_light': '#ff6b81',
            'success': '#00d9ff',
            'text': '#ffffff',
            'text_dim': '#a0a0a0'
        }
        
        # Setup modern UI
        self.setup_modern_ui()
        
        # Initialize components
        self.initialize_components()
        
    def setup_modern_ui(self):
        """Setup modern user interface"""
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Modern.TFrame', background=self.colors['bg_dark'])
        style.configure('Card.TFrame', background=self.colors['bg_medium'], relief='flat')
        style.configure('Modern.TLabel', background=self.colors['bg_dark'], 
                       foreground=self.colors['text'], font=('Segoe UI', 10))
        style.configure('Title.TLabel', background=self.colors['bg_dark'],
                       foreground=self.colors['text'], font=('Segoe UI', 24, 'bold'))
        style.configure('Subtitle.TLabel', background=self.colors['bg_dark'],
                       foreground=self.colors['text_dim'], font=('Segoe UI', 12))
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        title = tk.Label(header_frame, text="SubMinds AI", 
                        bg=self.colors['bg_dark'], fg=self.colors['accent'],
                        font=('Segoe UI', 28, 'bold'))
        title.pack(side='left')
        
        subtitle = tk.Label(header_frame, text="Real-time Emotion Analysis System",
                           bg=self.colors['bg_dark'], fg=self.colors['text_dim'],
                           font=('Segoe UI', 12))
        subtitle.pack(side='left', padx=20)
        
        # Status indicators
        status_frame = tk.Frame(header_frame, bg=self.colors['bg_dark'])
        status_frame.pack(side='right')
        
        self.status_indicators = {}
        statuses = [('Camera', 'camera'), ('AI Engine', 'ai'), ('Analysis', 'analysis')]
        
        for label, key in statuses:
            indicator_frame = tk.Frame(status_frame, bg=self.colors['bg_medium'], 
                                      relief='flat', bd=1)
            indicator_frame.pack(side='left', padx=5)
            
            tk.Label(indicator_frame, text=label, bg=self.colors['bg_medium'],
                    fg=self.colors['text_dim'], font=('Segoe UI', 9)).pack(side='left', padx=5)
            
            status_dot = tk.Label(indicator_frame, text="●", bg=self.colors['bg_medium'],
                                 fg='#ff4444', font=('Segoe UI', 14))
            status_dot.pack(side='left', padx=5)
            self.status_indicators[key] = status_dot
        
        # Content area
        content_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        content_frame.pack(fill='both', expand=True)
        
        # Left panel - Camera
        left_panel = tk.Frame(content_frame, bg=self.colors['bg_medium'], 
                             relief='flat', bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Camera header
        camera_header = tk.Frame(left_panel, bg=self.colors['bg_light'], height=50)
        camera_header.pack(fill='x')
        camera_header.pack_propagate(False)
        
        tk.Label(camera_header, text="📹 Live Camera Feed", 
                bg=self.colors['bg_light'], fg=self.colors['text'],
                font=('Segoe UI', 14, 'bold')).pack(side='left', padx=15, pady=10)
        
        # Camera canvas with overlay controls
        camera_container = tk.Frame(left_panel, bg='black')
        camera_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.camera_canvas = tk.Canvas(camera_container, bg='black',
                                       highlightthickness=0, width=800, height=600)
        self.camera_canvas.pack(fill='both', expand=True)
        
        # Show placeholder text
        self.camera_canvas.create_text(400, 300, text="Camera will appear here\nClick START ANALYSIS",
                                       fill='white', font=('Segoe UI', 16), tags="placeholder")
        
        # Overlay control buttons on canvas (will be positioned after window renders)
        self.root.after(100, self.create_overlay_controls)
        
        # Right panel - Analysis
        right_panel = tk.Frame(content_frame, bg=self.colors['bg_medium'],
                              relief='flat', bd=2, width=500)
        right_panel.pack(side='right', fill='both', padx=(10, 0))
        right_panel.pack_propagate(False)
        
        # Analysis header
        analysis_header = tk.Frame(right_panel, bg=self.colors['bg_light'], height=50)
        analysis_header.pack(fill='x')
        analysis_header.pack_propagate(False)
        
        tk.Label(analysis_header, text="🧠 AI Analysis Results",
                bg=self.colors['bg_light'], fg=self.colors['text'],
                font=('Segoe UI', 14, 'bold')).pack(side='left', padx=15, pady=10)
        
        # Analysis output
        output_container = tk.Frame(right_panel, bg=self.colors['bg_medium'])
        output_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.output_text = scrolledtext.ScrolledText(
            output_container,
            wrap=tk.WORD,
            bg=self.colors['bg_dark'],
            fg=self.colors['text'],
            font=('Consolas', 10),
            relief='flat',
            padx=10,
            pady=10
        )
        self.output_text.pack(fill='both', expand=True)
        
        # Bottom stats bar
        stats_bar = tk.Frame(main_container, bg=self.colors['bg_light'], height=60)
        stats_bar.pack(fill='x', pady=(10, 0))
        stats_bar.pack_propagate(False)
        
        self.stats_labels = {}
        stats = [
            ('Analyses', 'analyses', '0'),
            ('Uptime', 'uptime', '0:00'),
            ('FPS', 'fps', '0'),
            ('Last Image', 'image', 'None')
        ]
        
        for idx, (label, key, default) in enumerate(stats):
            stat_frame = tk.Frame(stats_bar, bg=self.colors['bg_light'])
            stat_frame.pack(side='left', expand=True, fill='both')
            
            tk.Label(stat_frame, text=label, bg=self.colors['bg_light'],
                    fg=self.colors['text_dim'], font=('Segoe UI', 9)).pack()
            
            value_label = tk.Label(stat_frame, text=default, bg=self.colors['bg_light'],
                                  fg=self.colors['success'], font=('Segoe UI', 16, 'bold'))
            value_label.pack()
            self.stats_labels[key] = value_label
    
    def create_overlay_controls(self):
        """Create modern overlay controls on camera canvas"""
        # Start button
        self.start_btn = tk.Button(
            self.camera_canvas,
            text="▶ START ANALYSIS",
            command=self.start_analysis,
            bg=self.colors['success'],
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            padx=30,
            pady=15,
            cursor='hand2',
            activebackground=self.colors['accent_light']
        )
        
        # Stop button
        self.stop_btn = tk.Button(
            self.camera_canvas,
            text="⏹ STOP ANALYSIS",
            command=self.stop_analysis,
            bg=self.colors['accent'],
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            padx=30,
            pady=15,
            cursor='hand2',
            state='disabled',
            activebackground='#d63447'
        )
        
        # Snapshot button
        self.snapshot_btn = tk.Button(
            self.camera_canvas,
            text="📷",
            command=self.save_snapshot,
            bg=self.colors['bg_light'],
            fg='white',
            font=('Segoe UI', 16),
            relief='flat',
            width=3,
            height=1,
            cursor='hand2'
        )
        
        # Position buttons (will be updated in camera loop)
        self.update_button_positions()
    
    def update_button_positions(self):
        """Update overlay button positions"""
        try:
            if not self.camera_canvas:
                return
                
            canvas_width = self.camera_canvas.winfo_width()
            canvas_height = self.camera_canvas.winfo_height()
            
            if canvas_width > 100 and canvas_height > 100:
                # Center buttons at bottom
                center_x = canvas_width // 2
                bottom_y = canvas_height - 80
                
                # Delete old button windows if they exist
                self.camera_canvas.delete("start_btn_window")
                self.camera_canvas.delete("stop_btn_window")
                self.camera_canvas.delete("snapshot_btn_window")
                
                # Create new button windows
                self.camera_canvas.create_window(center_x - 120, bottom_y,
                                                 window=self.start_btn, tags="start_btn_window")
                self.camera_canvas.create_window(center_x + 120, bottom_y,
                                                 window=self.stop_btn, tags="stop_btn_window")
                self.camera_canvas.create_window(canvas_width - 50, 50,
                                                 window=self.snapshot_btn, tags="snapshot_btn_window")
        except Exception as e:
            print(f"Button position error: {e}")
    
    def initialize_components(self):
        """Initialize camera and AI components"""
        self.log_output("🚀 Initializing SubMinds AI System...\n")
        
        # Initialize camera
        if CV2_AVAILABLE:
            try:
                self.camera = cv2.VideoCapture(self.config['camera_id'])
                if self.camera.isOpened():
                    self.update_status('camera', True)
                    self.log_output("✓ Camera initialized successfully")
                else:
                    self.update_status('camera', False)
                    self.log_output("✗ Camera not accessible")
            except Exception as e:
                self.update_status('camera', False)
                self.log_output(f"✗ Camera error: {e}")
        
        # Initialize face detector
        if FACE_DETECTION_AVAILABLE:
            try:
                self.face_detector = ExpressionDetector()
                if self.face_detector.is_available():
                    self.log_output("✓ Face detection initialized")
            except Exception as e:
                self.log_output(f"⚠ Face detection error: {e}")
        
        # Initialize IBM Granite
        if GRANITE_AVAILABLE and self.config['ibm_api_key'] and self.config['ibm_project_id']:
            try:
                self.granite_client = GraniteAIClient(
                    api_key=self.config['ibm_api_key'],
                    project_id=self.config['ibm_project_id']
                )
                if self.granite_client.is_available():
                    self.update_status('ai', True)
                    self.log_output("✓ IBM Granite AI connected")
                else:
                    self.update_status('ai', False)
                    self.log_output("⚠ IBM Granite in mock mode")
            except Exception as e:
                self.update_status('ai', False)
                self.log_output(f"⚠ IBM Granite error: {e}")
        else:
            self.update_status('ai', False)
            self.log_output("⚠ IBM Granite not configured")
            if GRANITE_AVAILABLE:
                try:
                    self.granite_client = GraniteAIClient()
                except:
                    pass
        
        self.log_output("\n✨ System ready! Click START ANALYSIS to begin.\n")
    
    def start_analysis(self):
        """Start analysis"""
        if not CV2_AVAILABLE or not self.camera or not self.camera.isOpened():
            messagebox.showerror("Error", "Camera not available")
            return
        
        self.is_running = True
        self.start_time = time.time()
        self.analysis_count = 0
        
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.update_status('analysis', True)
        
        self.log_output("\n" + "="*50)
        self.log_output("🎬 ANALYSIS STARTED")
        self.log_output("="*50 + "\n")
        
        # Start threads
        threading.Thread(target=self.camera_loop, daemon=True).start()
        threading.Thread(target=self.analysis_loop, daemon=True).start()
    
    def stop_analysis(self):
        """Stop analysis"""
        self.is_running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.update_status('analysis', False)
        
        self.log_output("\n" + "="*50)
        self.log_output(f"⏹ ANALYSIS STOPPED - Total: {self.analysis_count}")
        self.log_output("="*50 + "\n")
    
    def camera_loop(self):
        """Camera feed loop"""
        frame_count = 0
        fps_start = time.time()
        
        # Remove placeholder
        self.camera_canvas.delete("placeholder")
        
        while self.is_running:
            try:
                if not self.camera or not self.camera.isOpened():
                    self.log_output("Camera not available")
                    break
                    
                ret, frame = self.camera.read()
                if not ret:
                    continue
                
                self.current_frame = frame.copy()
                
                # Detect face and annotate
                if self.face_detector and self.face_detector.is_available():
                    analysis = self.face_detector.analyze_expression(frame)
                    if analysis.get('face_detected', False):
                        frame = self.face_detector.draw_annotations(frame, analysis)
                
                # Resize for display
                canvas_width = self.camera_canvas.winfo_width()
                canvas_height = self.camera_canvas.winfo_height()
                
                if canvas_width > 100 and canvas_height > 100:
                    display_frame = cv2.resize(frame, (canvas_width, canvas_height))
                else:
                    display_frame = cv2.resize(frame, (800, 600))
                    
                frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
                
                # Convert to PIL Image
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update canvas
                self.camera_canvas.delete("camera_image")
                center_x = canvas_width // 2 if canvas_width > 100 else 400
                center_y = canvas_height // 2 if canvas_height > 100 else 300
                self.camera_canvas.create_image(center_x, center_y, image=imgtk, tags="camera_image")
                self.camera_canvas.imgtk = imgtk
                
                # Keep buttons on top
                self.camera_canvas.tag_raise("start_btn_window")
                self.camera_canvas.tag_raise("stop_btn_window")
                self.camera_canvas.tag_raise("snapshot_btn_window")
                
                # Calculate FPS
                frame_count += 1
                if frame_count % 30 == 0:
                    fps = 30 / (time.time() - fps_start)
                    self.root.after(0, lambda: self.stats_labels['fps'].config(text=f"{fps:.1f}"))
                    fps_start = time.time()
                
                time.sleep(0.03)
                
            except Exception as e:
                print(f"Camera error: {e}")
                time.sleep(0.1)
    
    def analysis_loop(self):
        """Analysis loop"""
        while self.is_running:
            try:
                if self.current_frame is None:
                    time.sleep(0.1)
                    continue
                
                frame = self.current_frame.copy()
                
                # Save frame
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                image_filename = f"analysis_{timestamp}.jpg"
                image_path = os.path.join(self.captures_dir, image_filename)
                
                if CV2_AVAILABLE:
                    cv2.imwrite(image_path, frame)
                    self.stats_labels['image'].config(text=image_filename[:20] + "...")
                
                # Analyze
                if self.face_detector and self.face_detector.is_available():
                    facial_data = self.face_detector.analyze_expression(frame)
                else:
                    facial_data = {'face_detected': True, 'dominant_emotion': 'focused'}
                
                # Telemetry
                import random
                telemetry = {
                    'speed': random.uniform(150, 200),
                    'steering': random.uniform(-0.5, 0.5),
                    'track_position': random.uniform(-0.2, 0.2),
                }
                
                # AI Analysis
                if self.granite_client:
                    insights = self.granite_client.analyze_subconscious_patterns(
                        facial_data=facial_data,
                        telemetry=telemetry
                    )
                    self.display_insights(insights, image_filename)
                    self.analysis_count += 1
                    self.update_statistics()
                
                time.sleep(self.config['analysis_interval'])
                
            except Exception as e:
                self.log_output(f"Analysis error: {e}")
                time.sleep(1)
    
    def display_insights(self, insights: Dict[str, Any], image_filename: str):
        """Display insights"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        output = f"\n{'='*50}\n"
        output += f"[{timestamp}] Analysis #{self.analysis_count + 1}\n"
        output += f"{'='*50}\n"
        output += f"📷 {image_filename}\n\n"
        output += f"😊 {insights.get('emotional_state', 'Unknown')}\n"
        output += f"💪 {insights.get('stress_analysis', 'N/A')}\n\n"
        
        for rec in insights.get('recommendations', [])[:2]:
            output += f"💡 {rec}\n"
        
        output += f"{'='*50}\n"
        
        self.log_output(output)
    
    def update_statistics(self):
        """Update stats"""
        if self.start_time:
            uptime = int(time.time() - self.start_time)
            mins, secs = divmod(uptime, 60)
            self.stats_labels['analyses'].config(text=str(self.analysis_count))
            self.stats_labels['uptime'].config(text=f"{mins}:{secs:02d}")
    
    def save_snapshot(self):
        """Save snapshot"""
        if self.current_frame is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snapshot_{timestamp}.jpg"
            filepath = os.path.join(self.captures_dir, filename)
            
            if CV2_AVAILABLE:
                cv2.imwrite(filepath, self.current_frame)
                self.log_output(f"📷 Snapshot saved: {filename}\n")
    
    def update_status(self, key: str, active: bool):
        """Update status indicator"""
        if key in self.status_indicators:
            color = '#00ff00' if active else '#ff4444'
            self.status_indicators[key].config(fg=color)
    
    def log_output(self, message: str):
        """Log to output"""
        def _log():
            self.output_text.insert(tk.END, message + "\n")
            self.output_text.see(tk.END)
        
        if threading.current_thread() != threading.main_thread():
            self.root.after(0, _log)
        else:
            _log()
    
    def on_closing(self):
        """Handle closing"""
        self.is_running = False
        if self.camera:
            self.camera.release()
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ModernSubMindsApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()

# Made with Bob - Modern UI Edition