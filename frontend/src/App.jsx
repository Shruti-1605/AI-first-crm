import { useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { setMode } from './slices/chatSlice.js'
import ChatInterface from './components/ChatInterface.jsx'
import StructuredForm from './components/StructuredForm.jsx'
import './App.css'

function App() {
  const dispatch = useDispatch()
  const { mode } = useSelector(state => state.chat)

  return (
    <div className="app">
      <header className="header">
        <h1>AI-First CRM</h1>
        <p>Healthcare Professional Interaction Management</p>
      </header>

      <div className="mode-toggle">
        <button 
          className={mode === 'both' ? 'active' : ''}
          onClick={() => dispatch(setMode('both'))}
        >
          🔄 Both Interfaces
        </button>
        <button 
          className={mode === 'chat' ? 'active' : ''}
          onClick={() => dispatch(setMode('chat'))}
        >
          💬 Chat Only
        </button>
        <button 
          className={mode === 'form' ? 'active' : ''}
          onClick={() => dispatch(setMode('form'))}
        >
          📋 Form Only
        </button>
      </div>

      <main className={`content ${mode === 'both' ? 'split-view' : ''}`}>
        {mode === 'both' ? (
          <div className="interface-section">
            <h3>📋 HCP Interaction Details</h3>
            <div className="form-side">
              <StructuredForm />
            </div>
            <div className="ai-side">
              <h4>🤖 AI Assistant</h4>
              <ChatInterface />
            </div>
          </div>
        ) : mode === 'chat' ? (
          <ChatInterface />
        ) : (
          <StructuredForm />
        )}
      </main>
    </div>
  )
}

export default App