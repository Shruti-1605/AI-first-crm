# AI-First CRM - Healthcare Professional Interaction Management

A modern, AI-powered Customer Relationship Management system specifically designed for healthcare professional interactions. Built with React 19, FastAPI, LangGraph, and Groq AI.

## 🚀 Features

### Core Functionality
- **Dual Interface System**: Chat-based AI interaction and structured form input
- **AI-Powered Auto-Fill**: Natural language processing automatically populates form fields
- **Real-time Form Sync**: Chat conversations instantly update structured data
- **Interactive UI**: Modern, responsive design with green theme

### AI Capabilities
- **LangGraph Agent**: 5 specialized tools for HCP interaction management
- **Groq LLM Integration**: Fast inference with gemma2-9b-it model
- **Natural Language Processing**: Extract structured data from conversational input
- **Smart Suggestions**: AI-powered follow-up action recommendations

### Data Management
- **13 Comprehensive Fields**: Complete HCP interaction tracking
- **SQLAlchemy ORM**: Database-agnostic with SQLite/PostgreSQL/MySQL support
- **Real-time Validation**: Pydantic models ensure data integrity
- **Sentiment Analysis**: Automatic sentiment detection from interactions

## 🏗️ Architecture

### Frontend (React 19 + Vite)
```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.jsx      # AI chat component
│   │   └── StructuredForm.jsx     # Form component
│   ├── slices/
│   │   └── chatSlice.js          # Redux state management
│   └── App.jsx                   # Main application
├── package.json
└── vite.config.js
```

### Backend (FastAPI + LangGraph)
```
backend/
├── agent/
│   ├── langgraph_agent.py        # AI agent workflow
│   ├── tools.py                  # 5 specialized tools
│   └── main.py                   # Agent orchestration
├── models.py                     # SQLAlchemy models
├── final_app.py                  # Main FastAPI application
├── requirements.txt              # Python dependencies
└── .env                         # Environment configuration
```

## 🛠️ Technology Stack

### Frontend
- **React 19** - Latest React with concurrent features
- **Vite** - Fast build tool and dev server
- **Redux Toolkit** - State management
- **Axios** - HTTP client for API communication
- **CSS3** - Modern styling with animations

### Backend
- **FastAPI** - Modern Python web framework
- **LangGraph** - AI agent workflow framework
- **LangChain** - LLM application development
- **Groq** - Fast LLM inference platform
- **SQLAlchemy** - Python ORM
- **Pydantic** - Data validation and serialization

### AI & ML
- **Groq API** - LLM inference with gemma2-9b-it
- **LangGraph Tools** - Structured AI agent capabilities
- **Natural Language Processing** - Text analysis and extraction
- **Sentiment Analysis** - Automatic emotion detection

### Database
- **SQLite** (Development) - Lightweight file-based database
- **PostgreSQL** (Production Ready) - Enterprise-grade database
- **MySQL** (Production Ready) - Alternative production database

## 📋 Form Fields

The system captures comprehensive HCP interaction data:

1. **HCP Name** - Healthcare professional identification
2. **Interaction Type** - Meeting, call, visit, email, conference
3. **Date & Time** - Interaction timestamp
4. **Attendees** - Meeting participants
5. **Topics Discussed** - Conversation subjects
6. **Materials Shared** - Documents, brochures, presentations
7. **Samples Distributed** - Product samples provided
8. **HCP Sentiment** - Positive, neutral, or negative
9. **Outcomes** - Meeting results and decisions
10. **Follow-up Actions** - Next steps and commitments
11. **AI Description** - Natural language interaction summary

## 🤖 AI Agent Tools

### 1. log_interaction
Logs new HCP interactions with AI-powered data extraction and structuring.

### 2. edit_interaction
Modifies existing interactions with AI re-analysis capabilities.

### 3. get_hcp_history
Retrieves comprehensive interaction history for specific HCPs.

### 4. analyze_interaction_trends
Analyzes patterns and trends across multiple interactions.

### 5. suggest_next_actions
Provides AI-powered recommendations for follow-up actions.

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.8+
- **Git**

### Installation

1. **Clone Repository**
```bash
git clone <repository-url>
cd ai-first-crm
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd ../frontend
npm install
```

### Running the Application

1. **Start Backend Server**
```bash
cd backend
python final_app.py
```
Backend runs on: `http://localhost:8000`

2. **Start Frontend Development Server**
```bash
cd frontend
npm run dev
```
Frontend runs on: `http://localhost:3000`

### Usage

1. **Access Application**: Open `http://localhost:3000`
2. **Select Mode**: Choose between "Both Interfaces", "Chat Only", or "Form Only"
3. **AI Interaction**: Type natural language descriptions like:
   - "I met with Dr. Smith about cardiac devices"
   - "Had a positive call with Dr. Johnson regarding OncoBoost trial"
4. **Auto-Fill**: Watch form fields populate automatically
5. **Manual Entry**: Use structured form for detailed data entry

## 🔧 Configuration

### Environment Variables (.env)
```bash
# AI Configuration
GROQ_API_KEY=your_groq_api_key
PRIMARY_MODEL=gemma2-9b-it
AI_TEMPERATURE=0.1

# Database (Choose one)
DATABASE_URL=sqlite:///./crm_database.db
# DATABASE_URL=postgresql://user:pass@localhost:5432/crm_db
# DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/crm_db

# Application Settings
DEBUG=True
CORS_ORIGINS=["http://localhost:3000"]
```

## 📊 API Endpoints

### Core Endpoints
- `GET /` - Health check and API status
- `POST /chat` - AI chat interaction
- `GET /health` - System health with AI status

## 🎨 UI/UX Features

### Design System
- **Green Theme** - Professional healthcare color scheme
- **Interactive Elements** - Hover effects and smooth animations
- **Responsive Design** - Works on desktop, tablet, and mobile

### User Experience
- **Dual Mode Operation** - Chat and form work together seamlessly
- **Real-time Updates** - Instant form population from chat
- **Visual Feedback** - Loading states and success indicators
- **Intuitive Navigation** - Clear mode switching and controls

## 🔒 Security Features

- **Environment Variables** - Sensitive data in .env files
- **API Key Management** - Secure Groq API integration
- **Input Validation** - Pydantic models prevent injection
- **CORS Configuration** - Controlled cross-origin requests

## 📈 Performance

### Frontend Optimization
- **Vite Build System** - Fast development and production builds
- **React 19 Features** - Concurrent rendering and automatic batching
- **Redux Toolkit** - Efficient state management

### Backend Performance
- **FastAPI** - High-performance async framework
- **Groq API** - Ultra-fast LLM inference
- **SQLAlchemy** - Optimized database queries

## 🧪 Testing

### Development Testing
```bash
# Backend API testing
curl http://localhost:8000/health

# Frontend development
npm run dev
```

## 📦 Deployment

### Development Deployment
- Local development with SQLite
- Environment variables included
- Hot reload for both frontend and backend

### Production Considerations
- PostgreSQL/MySQL database setup
- Environment variable security
- SSL/HTTPS configuration

