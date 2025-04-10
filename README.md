# Video Broadcaster

Video Broadcaster is a real-time video streaming application that utilizes AI-powered segmentation to apply various background effects. This project is designed to work with virtual camera software, allowing users to broadcast video with customized backgrounds.

## Features

- **Real-time Person Segmentation**: Uses YOLOv8 for accurate person detection and segmentation.
- **Background Effects**: Choose from custom image backgrounds, blurred backgrounds, or black backgrounds.
- **Adjustable Settings**: Modify FPS and blur strength to suit your streaming needs.
- **Virtual Camera Output**: Stream processed video to virtual camera software for broadcasting.
- **Web-based Control Interface**: Manage streaming settings through a user-friendly web interface.

## Prerequisites

- **Python**: Version 3.8 or higher.
- **Virtual Camera Software**: OBS Virtual Camera or similar.
- **CUDA-capable GPU**: Recommended for optimal performance with YOLOv8.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/video_broadcaster.git
   cd video_broadcaster

   pip install requirements.txt

   python main.py

## API Endpoints

- **GET /api/settings**: Get current streaming settings.
- **GET /devices**: Update streaming settings.
- **GET /start:** Starts streaming with params
- **GET /stop:** Stops streaming



This README provides comprehensive information about your project, including setup, usage, and troubleshooting. Let me know if you need any additional sections or modifications!
