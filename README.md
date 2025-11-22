# AI Voice Agents Challenge - Day 1 Complete ✅

Welcome to my Murf AI Voice Agents Challenge journey!

## 🎯 Day 1 Task - Get Your Starter Voice Agent Running

**Status:** ✅ Completed

### What I Accomplished:
✅ Set up the complete development environment (Python 3.11, Node.js, pnpm, uv)
✅ Configured backend with Murf Falcon TTS integration
✅ Configured frontend Next.js application
✅ Downloaded and set up LiveKit Server
✅ Successfully connected all services (LiveKit, Backend Agent, Frontend)
✅ Had my first real-time voice conversation with the AI agent
✅ Pushed code to GitHub repository

### About the Challenge
Building 10 AI Voice Agents over 10 Days using Murf Falcon – the consistently fastest TTS API!

This is Day 1 of the #MurfAIVoiceAgentsChallenge #10DaysofAIVoiceAgents

---

## Repository Structure

This is a monorepo that contains both the backend and frontend for building voice agent applications. It's designed to be your starting point for each day's challenge task.

```
ten-days-of-voice-agents-2025/
├── backend/          # LiveKit Agents backend with Murf Falcon TTS
├── frontend/         # React/Next.js frontend for voice interaction
├── challenges/       # Daily challenge tasks
└── README.md         # This file
```

### Backend
The backend is based on [LiveKit's agent-starter-python](https://github.com/livekit-examples/agent-starter-python) with modifications to integrate **Murf Falcon TTS** for ultra-fast, high-quality voice synthesis.

**Features:**
- Complete voice AI agent framework using LiveKit Agents
- Murf Falcon TTS integration for fastest text-to-speech
- LiveKit Turn Detector for contextually-aware speaker detection
- Background voice cancellation
- Integrated metrics and logging
- Complete test suite with evaluation framework
- Production-ready Dockerfile

[→ Backend Documentation](./backend/README.md)

### Frontend
The frontend is based on [LiveKit's agent-starter-react](https://github.com/livekit-examples/agent-starter-react), providing a modern, beautiful UI for interacting with your voice agents.

**Features:**
- Real-time voice interaction with LiveKit Agents
- Camera video streaming support
- Screen sharing capabilities
- Audio visualization and level monitoring
- Light/dark theme switching
- Highly customizable branding and UI

[→ Frontend Documentation](./frontend/README.md)

---

## Quick Start

### Prerequisites
Make sure you have the following installed:
- **Python 3.11 or 3.12** (Python 3.14 not yet supported by all dependencies)
- **uv package manager:** `pip install uv`
- **Node.js 18+ with pnpm:** `npm install -g pnpm`
- **LiveKit Server:** [Download from LiveKit Releases](https://github.com/livekit/livekit/releases)

### Required API Keys
- `MURF_API_KEY` - Get from [Murf.ai](https://murf.ai)
- `GOOGLE_API_KEY` - Get from Google AI Studio
- `DEEPGRAM_API_KEY` - Get from Deepgram Console

### 1. Clone the Repository
```bash
git clone https://github.com/GhanshyamJha05/first_day_Task-Murf-AI-.git
cd first_day_Task-Murf-AI-
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies (use Python 3.11 or 3.12)
uv sync --python 3.11

# Create .env.local file with your API keys
# Copy from .env.example and add:
# LIVEKIT_URL=ws://127.0.0.1:7880
# LIVEKIT_API_KEY=devkey
# LIVEKIT_API_SECRET=secret
# MURF_API_KEY=<your_key>
cp .env.example .env.local

# Download required models
uv run python src/agent.py download-files
```

For LiveKit Cloud users, you can automatically populate credentials:
```bash
lk cloud auth
lk app env -w -d .env.local
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
pnpm install

# Create .env.local file
# LIVEKIT_API_KEY=devkey
# LIVEKIT_API_SECRET=secret
# LIVEKIT_URL=ws://127.0.0.1:7880
cp .env.example .env.local
```

### 4. Download and Run LiveKit Server
Download LiveKit Server:
1. Visit [LiveKit Releases](https://github.com/livekit/livekit/releases)
2. Download `livekit_X.X.X_windows_amd64.zip` (or your OS version)
3. Extract to project root

### 5. Run the Application
Run these in 3 separate terminals:

**Terminal 1 - LiveKit Server:**
*Windows*
```powershell
.\livekit-server.exe --dev
```
*Mac/Linux*
```bash
./livekit-server --dev
```

**Terminal 2 - Backend Agent:**
```bash
cd backend

# Activate virtual environment (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Then run
python src\agent.py dev
```
*Or using uv directly:*
```bash
uv run python src/agent.py dev
```

**Terminal 3 - Frontend:**
```bash
cd frontend
pnpm dev
```

Open http://localhost:3000 in your browser! 🎉

---

## 📅 Challenge Progress

- **Day 1:** ✅ Get Your Starter Voice Agent Running - **COMPLETED**
- **Day 2:** 🔜 Coming soon...
- **Day 3:** 🔜 Coming soon...
- **Day 4:** 🔜 Coming soon...
- **Day 5:** 🔜 Coming soon...
- **Day 6:** 🔜 Coming soon...
- **Day 7:** 🔜 Coming soon...
- **Day 8:** 🔜 Coming soon...
- **Day 9:** 🔜 Coming soon...
- **Day 10:** 🔜 Coming soon...

---

## Documentation & Resources
- [Murf Falcon TTS Documentation](https://murf.ai/api/docs/text-to-speech/streaming)
- [LiveKit Agents Documentation](https://docs.livekit.io/agents)
- [Original Backend Template](https://github.com/livekit-examples/agent-starter-python)
- [Original Frontend Template](https://github.com/livekit-examples/agent-starter-react)

## 🛠️ Tech Stack
- **Backend:** Python 3.11, LiveKit Agents, Murf Falcon TTS, Google Gemini LLM, Deepgram STT
- **Frontend:** Next.js 15, React 19, TypeScript, Tailwind CSS
- **Real-time Communication:** LiveKit Server
- **Package Managers:** uv (Python), pnpm (Node.js)

## 📝 Notes
- Use Python 3.11 or 3.12 (not 3.14) for compatibility
- All three services must be running simultaneously
- API keys are stored in `.env.local` files (not committed to Git)
- LiveKit server binary files are excluded from Git (download when needed)

## License
This project is based on MIT-licensed templates from LiveKit and includes integration with Murf Falcon. See individual LICENSE files in backend and frontend directories for details.

---

## Have Fun!
Remember, the goal is to learn, experiment, and build amazing voice AI agents. Don't hesitate to be creative and push the boundaries of what's possible with Murf Falcon and LiveKit!

Good luck with the challenge!

*Built for the AI Voice Agents Challenge by [murf.ai](https://murf.ai)*
