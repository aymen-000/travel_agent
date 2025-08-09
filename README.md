# TravelMate AI 🌍✈️

> Your intelligent multi-agent travel companion for seamless trip planning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)

![Download Demo Video ](/doc/demo.mkv)

## 🎯 Project Overview

**TravelMate AI** revolutionizes travel planning through an intelligent multi-agent system that understands, learns, and adapts to your travel needs. Built with cutting-edge AI technology, it seamlessly orchestrates flight bookings, hotel reservations, destination exploration, and comprehensive trip coordination through natural conversations.

### 🏗️ Architecture Highlights

Our sophisticated multi-agent architecture employs specialized AI agents, each mastering specific travel domains while collaborating intelligently to deliver unified, context-aware travel solutions.

---

## ✨ Key Features

### 🤖 **Intelligent Multi-Agent System**
- **Flight Agent**: Advanced flight search, price tracking, and booking assistance
- **Hotel Agent**: Accommodation discovery with preference matching
- **Destination Agent**: Local insights, attractions, and cultural recommendations
- **Team Coordinator**: Orchestrates cross-agent collaboration for complex itineraries

### 💬 **Conversational Intelligence**
- **Contextual Memory**: Maintains full conversation history across sessions
- **Natural Language Processing**: Understands complex, multi-part travel requests
- **Thread Persistence**: Seamless conversation continuity with client-side thread management


### 🔧 **Developer-Friendly Design**
- **Modular Architecture**: Easy to extend with new agents and capabilities
- **RESTful API**: Clean endpoints for seamless integration
- **LangGraph Framework**: State-of-the-art agent orchestration and workflow management

---

## 🛠️ Technology Stack

### Backend Infrastructure
- **Framework**: FastAPI (high-performance async Python web framework)
- **AI/ML**: LangChain + LangGraph (advanced agent orchestration)
- **Language**: Python 

### Frontend Experience
- **Framework**: React  with TypeScript
- **Styling**: Tailwind CSS
- **Type Safety**: Full TypeScript implementation

### Development & Deployment
- **Version Control**: Git with GitHub workflows
- **Testing**: Automated testing suite (coming soon)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16+ and npm
- Git

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/aymen-000/travel-agent.git
cd travel-agent

# Setup Python environment
uv sync 
source .venv/bin/activate



# Start the development server
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Environment Configuration

Create a `.env` root for agents configuration :

```bash
# API Keys (obtain from respective providers)
AMADEUS_CLIENT_ID = ""
AMADEUS_CLIENT_SECRET = ""
FLIGHT_AGENT_MODEL_ID = ""
TOGETHER_API_KEY =""
HOTEL_AGENT_MODEL_ID = ""
TAVILY_API_KEY = ""
```

Create a `.env.local` in frontend root: 
```bash
NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000 
```
 
---

## 📚 API Documentation

### Core Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `POST /search/team` | POST | Comprehensive travel planning coordination | `query`, `thread_id` |
| `POST /search/flights` | POST | Flight search and booking assistance | `query`, `thread_id` |
| `POST /search/hotels` | POST | Hotel discovery and reservation support | `query`, `thread_id` |
| `POST /search/destinations` | POST | Destination insights and recommendations | `query`, `thread_id` |

### Request Format

```json
{
  "query": "Find round-trip flights from NYC to Tokyo for 2 adults, departing June 15th",
  "thread_id": "uuid-v4-thread-identifier"
}
```

### Response Format

```json
{
  "response": "I found several excellent flight options for your NYC to Tokyo trip...",
  "agent_id": "flights",
  "thread_id": "uuid-v4-thread-identifier",
  "timestamp": "2025-08-09T21:00:00Z",
}
```


## 🎯 Future Roadmap

### Short-term Goals 
- [ ] **Car Rental Agent Integration**
  - [ ] Vehicle search and comparison
  - [ ] Rental booking workflow
  - [ ] Insurance and addon management

- [ ] **Enhanced Search Capabilities**
  - [ ] Deep web research agent
  - [ ] Real-time price monitoring
  - [ ] Deal aggregation and alerts

### Medium-term Goals
- [ ] **Advanced Personalization**
  - [ ] User profile system with preferences
  - [ ] AI-driven recommendation engine
  - [ ] Travel history and pattern analysis
  - [ ] Budget optimization algorithms

- [ ] **Infrastructure Improvements**
  - [ ] Redis-based session management
  - [ ] Microservices architecture migration
  - [ ] Kubernetes deployment support
  - [ ] Comprehensive monitoring and logging

### Long-term Vision 
- [ ] **Collaborative Intelligence**
  - [ ] Multi-agent negotiation for complex bookings
  - [ ] Cross-platform integrations (Google Travel, Expedia, etc.)
  - [ ] Group travel coordination features
  - [ ] Real-time collaboration tools

- [ ] **Next-Gen Features**
  - [ ] AR/VR destination previews
  - [ ] Voice-based travel assistant
  - [ ] Blockchain-based loyalty system
  - [ ] Carbon footprint optimization

---

## 🤝 Contributing

We welcome contributions from the community! TravelMate AI thrives on collaborative development and diverse perspectives.

### How to Contribute

1. **Fork the Repository**
   ```bash
   git fork https://github.com/aymen-000/travelmate-ai.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-new-feature
   ```

3. **Make Your Changes**
   - Follow our coding standards and conventions
   - Add tests for new functionality
   - Update documentation as needed

4. **Submit a Pull Request**
   - Provide a clear description of your changes
   - Reference any related issues
   - Ensure all tests pass


--- 

## 📞 Support & Community

### Getting Help
- 🐛 **Issues**: Report bugs via [GitHub Issues](https://github.com/aymen-000/travel-agent/issues)
- 💬 **Discussions**: Join our [GitHub Discussions](https://github.com/aymen-000/travel-agent/discussions)


### Community Guidelines
We foster an inclusive, respectful environment where everyone can contribute meaningfully to advancing intelligent travel technology.

---

## 👨‍💻 About the Creator

**Made with ❤️ by Aimen**

TravelMate AI represents a passion project combining artificial intelligence, travel industry expertise, and user-centered design. Built with dedication to solving real-world travel planning challenges through innovative technology.

*"Travel opens minds, and AI makes it accessible to everyone."* - Aimen

### Connect with Aimen
- 🐙 GitHub: [@aymen-000](https://github.com/aymen-000)
- 💼 LinkedIn: [Aimen's Profile]([https://linkedin.com/in/aimen-profile](https://www.linkedin.com/in/boukhari-aimen-5a64b9284/))


---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Aimen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

##  Acknowledgments

Special thanks to:
- **LangChain Community** for the powerful agent framework
- **FastAPI Team** for the exceptional web framework
- **React Community** for the robust frontend ecosystem
- **Open Source Contributors** who inspire and enable innovation

---

**Current Version**: v1.0.0-beta  
**Development Status**: Active Development  
**Last Updated**: August 2025

---

<div align="center">

**⭐ Star this repository if TravelMate AI helps make your travels extraordinary! ⭐**

*Building the future of intelligent travel, one conversation at a time.*

</div>
