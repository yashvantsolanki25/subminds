# Run SubMinds Modern UI

## Quick Start

### Run the Modern Version
```bash
python subminds_app_modern.py
```

### Or Run the Original Version
```bash
python subminds_app.py
```

## What's New in Modern UI

### 🎨 Enhanced Visual Design
- **Dark theme** with modern color scheme
- **Card-based layout** for better organization
- **Smooth animations** and transitions
- **Professional typography** (Segoe UI)

### 🎮 Overlay Controls on Camera
- **START/STOP buttons** directly on camera feed
- **Snapshot button** (📷) in top-right corner
- **No separate control panel** - cleaner interface
- **Buttons appear over video** for modern look

### 📊 Real-time Status Indicators
- **Color-coded status dots** in header
  - 🟢 Green = Active/Connected
  - 🔴 Red = Inactive/Disconnected
- **Camera status** - Shows if camera is working
- **AI Engine status** - Shows IBM Watson connection
- **Analysis status** - Shows if analysis is running

### 📈 Enhanced Stats Bar
- **Analyses count** - Total analyses performed
- **Uptime** - How long analysis has been running
- **FPS** - Camera frame rate
- **Last Image** - Most recent captured image name

### 🎯 Better UX
- **Larger camera view** (800x600)
- **Cleaner analysis panel** on the right
- **Better text formatting** with emojis
- **Responsive layout** that adapts to window size

## Features

### Camera Controls (Overlay)
1. **▶ START ANALYSIS** - Green button, starts everything
2. **⏹ STOP ANALYSIS** - Red button, stops analysis
3. **📷 Snapshot** - Top-right, saves current frame

### Analysis Display
- Shows real-time AI insights
- Displays which image is being analyzed
- Color-coded text for better readability
- Scrollable output for history

### Status Monitoring
- Live camera feed with face detection
- Real-time emotion annotations
- Performance metrics
- Connection status

## Color Scheme

- **Background**: Dark navy (#1a1a2e)
- **Cards**: Medium dark (#16213e)
- **Accent**: Vibrant pink (#e94560)
- **Success**: Cyan (#00d9ff)
- **Text**: White/Gray for contrast

## Keyboard Shortcuts

- **ESC** - Close application
- **Space** - Take snapshot (when focused)

## Tips

1. **Better Lighting** - Ensure good lighting for face detection
2. **Camera Position** - Face the camera directly
3. **Distance** - Stay 2-3 feet from camera
4. **Background** - Plain background works best

## Comparison

### Original App (subminds_app.py)
- Traditional layout
- Separate control buttons below camera
- Standard tkinter styling
- Good for detailed control

### Modern App (subminds_app_modern.py)
- Modern dark theme
- Overlay controls on camera
- Professional appearance
- Better for presentations

## Both Apps Include

✅ Real-time face detection
✅ 7 advanced emotion types
✅ IBM Watson AI integration
✅ Automatic image capture
✅ Image tracking in analysis
✅ Manual snapshot feature
✅ Captures folder management
✅ Full API connectivity

## Choose Your Version

**Use Modern App if you want:**
- Better visual appearance
- Overlay controls
- Professional look
- Dark theme

**Use Original App if you want:**
- Traditional interface
- More control options
- Familiar layout
- Light theme

Both work identically - just different UI/UX!