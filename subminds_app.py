"""
SubMinds Desktop Application - Complete Version with Camera View
AI-powered subconscious decision analysis for F1 drivers
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime
from typing import Optional, Dict, Any
import json
import csv

# Try to import required modules
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("WARNING: OpenCV not installed. Run: pip install opencv-python numpy")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("WARNING: python-dotenv not installed. Run: pip install python-dotenv")

# Add src to path
sys.path.insert(0, str(os.path.join(os.path.dirname(__file__), 'src')))

try:
    from src.ai_engine.granite_client import GraniteAIClient
    GRANITE_AVAILABLE = True
except ImportError:
    GRANITE_AVAILABLE = False
    print("WARNING: IBM Granite client not available")

try:
    from src.facial_analysis.expression_detector import ExpressionDetector
    FACE_DETECTION_AVAILABLE = True
except ImportError:
    FACE_DETECTION_AVAILABLE = False
    print("WARNING: Face detection not available")


class SubMindsApp:
    """Main desktop application with camera view"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SubMinds - F1 Driver Analysis")
        self.root.geometry("1400x900")
        
        # Application state
        self.is_running = False
        self.camera = None
        self.granite_client = None
        self.face_detector = None
        self.analysis_count = 0
        self.start_time = None
        self.current_frame = None
        self.last_saved_image = None

        # Session records for CSV export
        self.session_records = []
        
        # Create captures directory
        self.captures_dir = os.path.join(os.path.dirname(__file__), 'captures')
        os.makedirs(self.captures_dir, exist_ok=True)
        
        # Configuration
        self.config = {
            'ibm_api_key': os.getenv('IBM_CLOUD_API_KEY', ''),
            'ibm_space_id': os.getenv('IBM_SPACE_ID', ''),
            'ibm_watson_url': os.getenv('IBM_WATSON_URL', 'https://us-south.ml.cloud.ibm.com'),
            'camera_id': int(os.getenv('CAMERA_ID', '0')),
            'analysis_interval': float(os.getenv('ANALYSIS_INTERVAL', '2.0')),
        }
        
        # Setup UI
        self.setup_ui()
        
        # Initialize components
        self.initialize_components()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container with two columns
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_container,
            text="SubMinds - Subconscious Decision Analysis",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Left Column - Camera only
        left_frame = ttk.Frame(main_container)
        left_frame.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=5)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)

        # Camera View
        camera_frame = ttk.LabelFrame(left_frame, text="Camera Feed", padding="10")
        camera_frame.grid(row=0, column=0, sticky="nsew", pady=5)
        camera_frame.columnconfigure(0, weight=1)
        camera_frame.rowconfigure(0, weight=1)

        self.camera_label = ttk.Label(camera_frame, text="Camera not started", background="black", foreground="white")
        self.camera_label.grid(row=0, column=0, sticky="nsew")

        # Right Column - Controls → Status → Analysis Output
        right_frame = ttk.Frame(main_container)
        right_frame.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=5)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(2, weight=1)

        # ── Row 0: Control Panel ──────────────────────────────────────
        control_frame = ttk.LabelFrame(right_frame, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, sticky="ew", pady=5)

        self.start_button = ttk.Button(
            control_frame,
            text="Start Analysis",
            command=self.start_analysis,
            width=18
        )
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = ttk.Button(
            control_frame,
            text="Stop Analysis",
            command=self.stop_analysis,
            width=18,
            state='disabled'
        )
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)

        config_button = ttk.Button(
            control_frame,
            text="Configure",
            command=self.show_config_dialog,
            width=18
        )
        config_button.grid(row=0, column=2, padx=5, pady=5)

        save_button = ttk.Button(
            control_frame,
            text="Save Snapshot",
            command=self.save_snapshot,
            width=18
        )
        save_button.grid(row=1, column=0, padx=5, pady=5)

        open_folder_button = ttk.Button(
            control_frame,
            text="Open Captures",
            command=self.open_captures_folder,
            width=18
        )
        open_folder_button.grid(row=1, column=1, padx=5, pady=5)

        export_button = ttk.Button(
            control_frame,
            text="Export CSV",
            command=self.export_csv,
            width=18
        )
        export_button.grid(row=1, column=2, padx=5, pady=5)

        # ── Row 1: Status Panel ───────────────────────────────────────
        status_frame = ttk.LabelFrame(right_frame, text="System Status", padding="10")
        status_frame.grid(row=1, column=0, sticky="ew", pady=5)

        self.status_labels = {}
        labels = [
            ('Camera', 'camera_status'),
            ('Dual AI', 'granite_status'),
            ('Analysis', 'analysis_status')
        ]

        for idx, (label_text, key) in enumerate(labels):
            label = ttk.Label(status_frame, text=f"{label_text}:")
            label.grid(row=0, column=idx*2, padx=5, sticky="w")

            status = ttk.Label(status_frame, text="●", foreground="red", font=('Arial', 12))
            status.grid(row=0, column=idx*2+1, padx=5, sticky="w")
            self.status_labels[key] = status

        # ── Row 2: Analysis Output ────────────────────────────────────
        output_frame = ttk.LabelFrame(right_frame, text="Analysis Output", padding="10")
        output_frame.grid(row=2, column=0, sticky="nsew", pady=5)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            width=60,
            height=25,
            font=('Courier', 9)
        )
        self.output_text.grid(row=0, column=0, sticky="nsew")
        
        # Statistics Panel
        stats_frame = ttk.LabelFrame(main_container, text="Statistics", padding="10")
        stats_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.stats_labels = {}
        stats = [
            ('Analyses', 'total_analyses'),
            ('Uptime', 'uptime'),
            ('FPS', 'fps')
        ]
        
        for idx, (label_text, key) in enumerate(stats):
            label = ttk.Label(stats_frame, text=f"{label_text}:")
            label.grid(row=0, column=idx*2, padx=10, sticky="w")
            
            value = ttk.Label(stats_frame, text="0", font=('Arial', 10, 'bold'))
            value.grid(row=0, column=idx*2+1, padx=5, sticky="w")
            self.stats_labels[key] = value
        
    def initialize_components(self):
        """Initialize camera and AI components"""
        self.log_output("Initializing SubMinds components...")
        
        # Initialize camera
        if CV2_AVAILABLE:
            try:
                self.camera = cv2.VideoCapture(self.config['camera_id'])
                if self.camera.isOpened():
                    self.update_status('camera_status', 'green')
                    self.log_output("✓ Camera initialized successfully")
                else:
                    self.update_status('camera_status', 'red')
                    self.log_output("✗ Camera not accessible")
            except Exception as e:
                self.update_status('camera_status', 'red')
                self.log_output(f"✗ Camera initialization failed: {e}")
        else:
            self.update_status('camera_status', 'red')
            self.log_output("✗ OpenCV not installed")
        
        # Initialize face detector
        if FACE_DETECTION_AVAILABLE:
            try:
                self.face_detector = ExpressionDetector()
                if self.face_detector.is_available():
                    self.log_output("✓ Face detection initialized")
                else:
                    self.log_output("⚠ Face detection not available")
            except Exception as e:
                self.log_output(f"⚠ Face detection error: {e}")
        else:
            self.log_output("⚠ Face detection module not available")
        
        # Initialize Dual AI (SubMindsAI + Llama 4 Maverick)
        if GRANITE_AVAILABLE:
            try:
                self.granite_client = GraniteAIClient(
                    config_path='config/ibm_granite_config.yaml',
                    api_key=self.config['ibm_api_key'] or None,
                    space_id=self.config['ibm_space_id'] or None,
                    url=self.config['ibm_watson_url']
                )
                stats = self.granite_client.get_statistics()
                if stats['subminds_available'] and stats['llama_available']:
                    self.update_status('granite_status', 'green')
                    self.log_output("✓ SubMindsAI custom model  — ONLINE 🤖")
                    self.log_output("✓ Llama 4 Maverick model   — ONLINE 🦙")
                elif stats['subminds_available'] or stats['llama_available']:
                    self.update_status('granite_status', 'yellow')
                    self.log_output("⚠ One AI model online, one in mock mode")
                else:
                    self.update_status('granite_status', 'yellow')
                    self.log_output("⚠ Both AI models in mock mode (check credentials)")
            except Exception as e:
                self.update_status('granite_status', 'yellow')
                self.log_output(f"⚠ AI init error (mock mode): {e}")
                try:
                    self.granite_client = GraniteAIClient()
                except Exception:
                    pass
        
        self.log_output("\nSystem ready. Click 'Start Analysis' to begin.")
        
    def start_analysis(self):
        """Start the analysis process"""
        if not CV2_AVAILABLE or not self.camera or not self.camera.isOpened():
            messagebox.showerror("Error", "Camera not available. Please check your camera connection.")
            return
        
        self.is_running = True
        self.start_time = time.time()
        self.analysis_count = 0
        self.session_records = []  # Reset records for new session
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.update_status('analysis_status', 'green')
        self.log_output("\n" + "="*60)
        self.log_output("ANALYSIS STARTED")
        self.log_output("="*60 + "\n")
        
        # Start camera and analysis threads
        self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.camera_thread.start()
        
        self.analysis_thread = threading.Thread(target=self.analysis_loop, daemon=True)
        self.analysis_thread.start()
        
    def stop_analysis(self):
        """Stop the analysis process and prompt to export CSV"""
        self.is_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.update_status('analysis_status', 'red')
        self.log_output("\n" + "="*60)
        self.log_output("ANALYSIS STOPPED")
        self.log_output(f"Total analyses performed: {self.analysis_count}")
        self.log_output("="*60 + "\n")

        # Auto-prompt CSV export if there is data
        if self.session_records:
            if messagebox.askyesno(
                "Export Report",
                f"Session complete — {self.analysis_count} analyses recorded.\n\nExport results as CSV?"
            ):
                self.export_csv()
    
    def save_snapshot(self):
        """Save current frame as snapshot"""
        if self.current_frame is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snapshot_{timestamp}.jpg"
            filepath = os.path.join(self.captures_dir, filename)
            
            if CV2_AVAILABLE:
                cv2.imwrite(filepath, self.current_frame)
                self.log_output(f"Snapshot saved: {filename}")
                messagebox.showinfo("Success", f"Snapshot saved to:\n{filepath}")
        else:
            messagebox.showwarning("Warning", "No frame available to save")
    
    def open_captures_folder(self):
        """Open the captures folder"""
        if os.path.exists(self.captures_dir):
            os.startfile(self.captures_dir)
        else:
            messagebox.showinfo("Info", "No captures folder yet")

    def export_csv(self):
        """Export session analysis records to a CSV file chosen by the user"""
        if not self.session_records:
            messagebox.showwarning("No Data", "No analysis data to export yet.\nRun an analysis session first.")
            return

        # Ask user where to save
        default_name = f"subminds_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = filedialog.asksaveasfilename(
            title="Save Analysis Report",
            initialfile=default_name,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not filepath:
            return  # User cancelled

        try:
            fieldnames = [
                'analysis_number',
                'timestamp',
                'image_file',
                'dominant_emotion',
                'emotion_emoji',
                'confidence',
                'valence',
                'arousal',
                'stress_level',
                'face_detected',
                'speed_kmh',
                'steering',
                'track_position',
                'emotional_state',
                'stress_analysis',
                'decision_patterns',
                'recommendations',
                'predictions',
            ]

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for record in self.session_records:
                    writer.writerow(record)

            self.log_output(f"✓ Report exported: {os.path.basename(filepath)}")
            messagebox.showinfo("Export Successful", f"Report saved to:\n{filepath}")

        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not save CSV:\n{e}")
            self.log_output(f"✗ Export failed: {e}")
        
    def camera_loop(self):
        """Camera feed loop (runs in separate thread)"""
        frame_count = 0
        fps_start = time.time()
        
        while self.is_running:
            try:
                ret, frame = self.camera.read()
                if not ret:
                    continue
                
                # Store current frame
                self.current_frame = frame.copy()
                
                # Resize frame for display
                display_frame = cv2.resize(frame, (640, 480))
                
                # Detect and annotate face if detector available
                if self.face_detector and self.face_detector.is_available():
                    analysis = self.face_detector.analyze_expression(frame)
                    if analysis.get('face_detected', False):
                        display_frame = self.face_detector.draw_annotations(
                            cv2.resize(frame, (640, 480)),
                            analysis
                        )
                
                # Add timestamp and info
                timestamp = datetime.now().strftime("%H:%M:%S")
                cv2.putText(display_frame, f"Time: {timestamp}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(display_frame, f"Analyses: {self.analysis_count}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Convert to RGB for tkinter
                frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update camera label
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk)
                
                # Calculate FPS
                frame_count += 1
                if frame_count % 30 == 0:
                    fps = 30 / (time.time() - fps_start)
                    self.root.after(0, lambda: self.stats_labels['fps'].config(text=f"{fps:.1f}"))
                    fps_start = time.time()
                
                time.sleep(0.03)  # ~30 FPS
                
            except Exception as e:
                print(f"Camera loop error: {e}")
                time.sleep(0.1)
    
    def analysis_loop(self):
        """Analysis loop (runs in separate thread)"""
        while self.is_running:
            try:
                # Get current frame
                if self.current_frame is None:
                    time.sleep(0.1)
                    continue
                
                frame = self.current_frame.copy()
                
                # Save frame with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                image_filename = f"analysis_{timestamp}.jpg"
                image_path = os.path.join(self.captures_dir, image_filename)
                
                if CV2_AVAILABLE:
                    cv2.imwrite(image_path, frame)
                    self.last_saved_image = image_filename
                
                # Analyze facial expression
                if self.face_detector and self.face_detector.is_available():
                    facial_data = self.face_detector.analyze_expression(frame)
                else:
                    # Fallback to simulated data
                    facial_data = {
                        'face_detected': True,
                        'dominant_emotion': 'focused',
                        'confidence': 0.85,
                        'valence': 0.3,
                        'arousal': 0.7,
                        'stress_level': 6
                    }
                
                # Simulate telemetry
                import random
                telemetry = {
                    'speed': random.uniform(150, 200),
                    'steering': random.uniform(-0.5, 0.5),
                    'track_position': random.uniform(-0.2, 0.2),
                }
                
                # Analyze with Granite AI
                if self.granite_client:
                    # Analyze facial data and telemetry
                    insights = self.granite_client.analyze_subconscious_patterns(
                        facial_data=facial_data,
                        telemetry=telemetry
                    )
                    
                    # Also analyze the captured image directly
                    image_analysis = None
                    if CV2_AVAILABLE and os.path.exists(image_path):
                        try:
                            image_analysis = self.granite_client.analyze_image(
                                image_path=image_path,
                                analysis_type="facial_expression",
                                additional_context="F1 driver performance analysis"
                            )
                            self.log_output(f"✓ Image sent to AI for analysis: {image_filename}")
                        except Exception as e:
                            self.log_output(f"⚠ Image analysis error: {e}")
                    
                    self.display_insights(insights, image_filename, facial_data, telemetry, image_analysis)
                    self.analysis_count += 1
                    
                    # Update statistics
                    self.update_statistics()
                
                # Wait before next analysis
                time.sleep(self.config['analysis_interval'])
                
            except Exception as e:
                self.log_output(f"Analysis error: {e}")
                time.sleep(1)
    
    def display_insights(self, insights: Dict[str, Any], image_filename: str = None,
                         facial_data: Dict[str, Any] = None, telemetry: Dict[str, Any] = None,
                         image_analysis: Dict[str, Any] = None):
        """Display dual-model analysis insights with emoji emotions."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        facial_data = facial_data or {}
        telemetry   = telemetry   or {}

        # ── Emotion emoji ─────────────────────────────────────────────
        from src.ai_engine.granite_client import get_emotion_emoji
        emotion       = facial_data.get('dominant_emotion', 'neutral')
        emotion_emoji = insights.get('emotion_emoji', get_emotion_emoji(emotion))

        # ── CSV record ────────────────────────────────────────────────
        self.session_records.append({
            'analysis_number':  self.analysis_count + 1,
            'timestamp':        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'image_file':       image_filename or '',
            'dominant_emotion': emotion,
            'emotion_emoji':    emotion_emoji,
            'confidence':       round(facial_data.get('confidence', 0.0), 3),
            'valence':          round(facial_data.get('valence', 0.0), 3),
            'arousal':          round(facial_data.get('arousal', 0.0), 3),
            'stress_level':     facial_data.get('stress_level', ''),
            'face_detected':    facial_data.get('face_detected', False),
            'speed_kmh':        round(telemetry.get('speed', 0.0), 1),
            'steering':         round(telemetry.get('steering', 0.0), 3),
            'track_position':   round(telemetry.get('track_position', 0.0), 3),
            'emotional_state':  insights.get('emotional_state', ''),
            'stress_analysis':  insights.get('stress_analysis', ''),
            'decision_patterns': ' | '.join(insights.get('decision_patterns', [])),
            'recommendations':  ' | '.join(insights.get('recommendations', [])),
            'predictions':      ' | '.join(insights.get('predictions', [])),
        })

        # ── Build display output ──────────────────────────────────────
        sep = "═" * 62
        output  = f"\n{sep}\n"
        output += f"  {emotion_emoji}  Analysis #{self.analysis_count + 1}  [{timestamp}]\n"
        output += f"{sep}\n"

        if image_filename:
            output += f"📷  {image_filename}\n\n"

        # Emotion badge
        output += f"{'─'*62}\n"
        output += f"  EMOTION  {emotion_emoji}  {emotion.replace('_', ' ').upper()}\n"
        output += f"  Stress {facial_data.get('stress_level', '?')}/10  |  "
        output += f"Valence {facial_data.get('valence', 0):+.2f}  |  "
        output += f"Arousal {facial_data.get('arousal', 0):.2f}\n"
        output += f"{'─'*62}\n\n"

        # ── SubMindsAI output ─────────────────────────────────────────
        subminds = insights.get('subminds_insight', {})
        output += f"🤖  SubMindsAI (Custom Model)\n"
        output += f"    {subminds.get('emotional_state', insights.get('emotional_state', '—'))}\n"
        s_stress = subminds.get('stress_analysis', '')
        if s_stress:
            output += f"    💢 {s_stress}\n"
        s_recs = subminds.get('recommendations', [])
        if s_recs:
            output += f"    💡 " + " | ".join(s_recs[:2]) + "\n"
        output += "\n"

        # ── Llama 4 Maverick output ───────────────────────────────────
        llama = insights.get('llama_insight', {})
        output += f"🦙  Llama 4 Maverick (Foundation Model)\n"
        output += f"    {llama.get('emotional_state', insights.get('emotional_state', '—'))}\n"
        l_stress = llama.get('stress_analysis', '')
        if l_stress:
            output += f"    💢 {l_stress}\n"
        l_recs = llama.get('recommendations', [])
        if l_recs:
            output += f"    💡 " + " | ".join(l_recs[:2]) + "\n"
        output += "\n"

        # ── Deep image analysis (if available) ───────────────────────
        if image_analysis:
            merged = image_analysis.get('merged', {})
            if merged:
                output += f"{'─'*62}\n"
                output += f"🔬  DEEP IMAGE ANALYSIS\n"
                primary = merged.get('primary_emotion', {})
                if isinstance(primary, dict):
                    pname  = primary.get('name', '?')
                    pintens = primary.get('intensity', 0)
                    pemoji = get_emotion_emoji(pname)
                    output += f"    Primary: {pemoji} {pname.title()} ({pintens:.0%})\n"
                sec = merged.get('secondary_emotions', [])
                if sec:
                    sec_str = "  ".join(
                        f"{get_emotion_emoji(e.get('name','?'))} {e.get('name','?').title()}"
                        for e in sec[:3]
                    )
                    output += f"    Secondary: {sec_str}\n"
                cog = merged.get('cognitive_state', '')
                if cog:
                    output += f"    🧠 {cog}\n"
                perf = merged.get('performance_impact', '')
                if perf:
                    output += f"    🏎️  {perf}\n"
                deep_recs = merged.get('recommendations', [])
                if deep_recs:
                    output += f"    ✅ " + "\n    ✅ ".join(deep_recs[:3]) + "\n"
                output += "\n"

        # ── Merged predictions ────────────────────────────────────────
        preds = insights.get('predictions', [])
        if preds:
            output += f"🔮  Predictions\n"
            for p in preds[:2]:
                output += f"    → {p}\n"
            output += "\n"

        output += f"{sep}\n"
        self.log_output(output)
    
    def update_statistics(self):
        """Update statistics display"""
        if self.start_time:
            uptime = time.time() - self.start_time
            self.root.after(0, lambda: self.stats_labels['total_analyses'].config(text=str(self.analysis_count)))
            self.root.after(0, lambda: self.stats_labels['uptime'].config(
                text=f"{int(uptime//60)}m {int(uptime%60)}s"
            ))
    
    def show_config_dialog(self):
        """Show configuration dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Configuration")
        dialog.geometry("550x400")
        
        ttk.Label(dialog, text="IBM Cloud API Key:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        api_key_entry = ttk.Entry(dialog, width=50, show="*")
        api_key_entry.insert(0, self.config['ibm_api_key'])
        api_key_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="IBM Space ID:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        space_id_entry = ttk.Entry(dialog, width=50)
        space_id_entry.insert(0, self.config['ibm_space_id'])
        space_id_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Watson URL:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        watson_url_entry = ttk.Entry(dialog, width=50)
        watson_url_entry.insert(0, self.config['ibm_watson_url'])
        watson_url_entry.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Camera ID:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        camera_id_entry = ttk.Entry(dialog, width=50)
        camera_id_entry.insert(0, str(self.config['camera_id']))
        camera_id_entry.grid(row=3, column=1, padx=10, pady=10)
        
        def save_config():
            self.config['ibm_api_key'] = api_key_entry.get()
            self.config['ibm_space_id'] = space_id_entry.get()
            self.config['ibm_watson_url'] = watson_url_entry.get()
            self.config['camera_id'] = int(camera_id_entry.get())
            
            # Save to .env
            with open('.env', 'w') as f:
                f.write(f"IBM_CLOUD_API_KEY={self.config['ibm_api_key']}\n")
                f.write(f"IBM_SPACE_ID={self.config['ibm_space_id']}\n")
                f.write(f"IBM_WATSON_URL={self.config['ibm_watson_url']}\n")
                f.write(f"CAMERA_ID={self.config['camera_id']}\n")
                f.write(f"ANALYSIS_INTERVAL={self.config['analysis_interval']}\n")
                f.write(f"MODEL_ID=meta-llama/llama-4-maverick-17b-128e-instruct-fp8\n")
                f.write(f"TEMPERATURE=0.7\n")
                f.write(f"TOP_P=0.9\n")
                f.write(f"MAX_TOKENS=2000\n")
            
            messagebox.showinfo("Success", "Configuration saved! Restart for changes to take effect.")
            dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save_config).grid(row=4, column=0, columnspan=2, pady=20)
    
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
    
    def on_closing(self):
        """Handle window closing"""
        self.is_running = False
        if self.camera:
            self.camera.release()
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SubMindsApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()

# Made with Bob - Desktop Edition with Camera View