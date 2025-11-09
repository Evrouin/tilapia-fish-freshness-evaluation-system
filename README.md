# Tilapia Fish Freshness Evaluation System

A computer vision system for evaluating tilapia fish freshness using YOLOv3 object detection, GrabCut segmentation, and advanced RGB color analysis.

## Features
- **Object Detection**: Custom YOLOv3 model for tilapia gill identification
- **Segmentation**: GrabCut algorithm for precise gill area extraction
- **Color Analysis**: Advanced RGB analysis with brightness, saturation, and color ratios
- **GUI Interface**: User-friendly Tkinter-based interface with progress indicators
- **Performance Optimizations**: Image caching, lazy loading, and memory-based processing
- **Structured Logging**: Industry-standard logging with separate analysis results
- **Modern Architecture**: Object-oriented design with proper separation of concerns

## Project Structure
```
├── src/tilapia_freshness/
│   ├── models/              # ML models (YOLO, GrabCut, Analyzer)
│   ├── gui/                 # GUI components
│   ├── utils/               # Utility functions (caching, progress, logging)
│   ├── enums/               # Enums and constants
│   ├── config/              # Configuration management
│   ├── exceptions/          # Custom exceptions
│   └── assets/              # Application resources (icon)
├── tests/                   # Unit tests
├── .github/workflows/       # CI/CD pipeline
├── images/                  # Sample images
├── inputs/                  # Standardized input files (auto-generated)
├── outputs/                 # Generated results and logs
├── main.py                  # Application entry point
├── pyproject.toml           # Modern Python packaging
└── requirements.txt         # Dependencies
```

## Prerequisites
- Python 3.11+
- Required packages listed in `requirements.txt`

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/Evrouin/tilapia-fish-freshness-evaluation-system.git
cd tilapia-fish-freshness-evaluation-system
```

### 2. Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -e .
# Or for development:
pip install -e ".[dev]"
```

### 4. Download Model Files
Download the required model files from [Google Drive](https://drive.google.com/drive/folders/10jHceX5oWSkUvNIrLch0MGXo0zh2iUJp?usp=sharing) and place them in the `data/` folder:
- `yolov3_tilapia.weights`
- `yolov3_tilapia.cfg`
- `obj.names`

## Usage

### Run Application
```bash
python main.py
# Or if installed:
tilapia-freshness
```

### Using the GUI
1. Click **"Select Image"** to choose a tilapia fish image
2. The system automatically detects gills using YOLOv3 with progress indication
3. Click **"Start Analysis"** to perform segmentation and freshness evaluation
4. Results display RGB values, confidence scores, and freshness classification

### Freshness Classifications
- **Fresh**: Good color quality, red dominance, appropriate saturation
- **Not Fresh**: Moderate degradation, unclear color characteristics
- **Old**: Blue/gray dominance, washed out colors, high brightness

## Development

### Development Setup
```bash
make install-dev    # Install with development dependencies
```

### Code Quality
```bash
make format         # Format code with Black and isort
make lint          # Run flake8 linter
make type-check    # Run mypy type checker
make test          # Run tests with coverage
make check-all     # Run all quality checks
```

### Running Tests
```bash
pytest tests/ -v --cov=src/tilapia_freshness
```

## Technical Details

### Key Components
- **YOLODetector**: Handles gill detection with lazy loading
- **GillSegmenter**: Performs GrabCut segmentation
- **ColorAnalyzer**: Analyzes RGB values and classifies freshness
- **InputFileManager**: Standardized file processing with timestamp naming
- **ProgressDialog**: User feedback for long operations

### Color Analysis Algorithm
The system uses multiple metrics for accurate freshness evaluation:
- Distance from fresh reference point (32, 19, 17)
- Color brightness and saturation analysis
- RGB ratios and dominance patterns
- Weighted mean/median filtering for noise reduction
- Configurable thresholds for different freshness levels

## Authors
- [@John Elway Cortez](https://github.com/Evrouin) - Lead Developer
- [@Dustin Uriel Obispo]() - Co-Developer
- [@King Red Sanchez](https://github.com/haringpula) - Co-Developer
- [@Briel Aldous Viola]() - Co-Developer

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.