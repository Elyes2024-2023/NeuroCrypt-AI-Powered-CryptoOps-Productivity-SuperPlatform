# NeuroCrypt: AI-Powered CryptoOps & Productivity SuperPlatform

## Author
ELYES (2024-2025)

## Overview
NeuroCrypt is a modular, AI-driven super app that combines crypto operations, productivity tools, IoT monitoring, and system security into a unified platform.

## Core Features
- 🧠 AI-Enhanced Productivity Tools
- 📊 Crypto Wallet & DeFi Asset Tracking
- 📡 IoT Workspace Monitoring
- 🔐 System Health & Security
- 💼 SaaS Development Toolkit
- 📲 Mobile Companion App
- 📈 Executive Dashboards

## Tech Stack
- **Backend**: Python (FastAPI), C# (.NET Core)
- **Frontend**: Blazor, Next.js
- **Mobile**: Flutter
- **AI/ML**: LangChain, OpenAI API, GPT-4
- **Blockchain**: Web3.py, MetaMask, Moralis
- **IoT**: MQTT, ESP32, Azure IoT
- **Security**: ETW, WinAPI, OpenTelemetry
- **Database**: PostgreSQL, Redis, ChromaDB

## Project Structure
```
neurocrypt/
├── ai_productivity/        # AI and productivity features
├── crypto_intelligence/    # Crypto tracking and analysis
├── iot_monitor/           # IoT workspace monitoring
├── system_security/       # System health and security
├── saas_toolkit/          # Developer tools and SaaS features
├── mobile_app/            # Flutter mobile application
├── dashboards/            # Executive dashboards and analytics
├── shared/                # Shared utilities and common code
└── infrastructure/        # DevOps and deployment configs
```

## Getting Started

### Prerequisites
- Python 3.9+
- .NET 6.0+
- Node.js 16+
- Flutter SDK
- Docker

### Installation
1. Clone the repository
```bash
git clone https://github.com/Elyes2024-2023/NeuroCrypt-AI-Powered-CryptoOps-Productivity-SuperPlatform.git
cd NeuroCrypt-AI-Powered-CryptoOps-Productivity-SuperPlatform
```

2. Set up Python environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up .NET environment
```bash
dotnet restore
```

4. Set up Flutter environment
```bash
cd mobile_app
flutter pub get
```

### Configuration
1. Copy `.env.example` to `.env` and fill in your configuration
2. Set up API keys for:
   - OpenAI
   - CoinGecko
   - Moralis
   - Azure IoT Hub

### Running the Application
1. Start the backend services:
```bash
python -m neurocrypt.ai_productivity
dotnet run --project neurocrypt/crypto_intelligence
```

2. Start the frontend:
```bash
cd neurocrypt/frontend
npm install
npm run dev
```

3. Run the mobile app:
```bash
cd neurocrypt/mobile_app
flutter run
```

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
* [OpenAI](https://openai.com/) - For GPT-4 API and AI capabilities
* [FastAPI](https://fastapi.tiangolo.com/) - For the high-performance web framework
* [SQLAlchemy](https://www.sqlalchemy.org/) - For the powerful SQL toolkit and ORM
* [LangChain](https://langchain.com/) - For AI/LLM application framework
* The open-source community for various tools and libraries used in this project
* CoinGecko for crypto data
* MetaMask for wallet integration
* ESP32 community for IoT support 