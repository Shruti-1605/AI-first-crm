import { useState, useRef, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { sendMessage } from '../slices/chatSlice.js'
import './ChatInterface.css'

function ChatInterface() {
  const [input, setInput] = useState('')
  const [connectionStatus, setConnectionStatus] = useState('checking')
  const dispatch = useDispatch()
  const { messages, loading, error } = useSelector(state => state.chat)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Check backend connection
  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await fetch('http://localhost:8000/', {
          method: 'GET',
          mode: 'cors'
        })
        if (response.ok) {
          setConnectionStatus('connected')
        } else {
          setConnectionStatus('error')
        }
      } catch (error) {
        console.log('Connection check failed:', error)
        setConnectionStatus('error')
      }
    }
    
    checkConnection()
    const interval = setInterval(checkConnection, 5000) // Check every 5s
    return () => clearInterval(interval)
  }, [])

  const handleSend = () => {
    if (input.trim() && !loading) {
      dispatch(sendMessage(input.trim()))
      setInput('')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const getConnectionStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return '#10b981'
      case 'error': return '#ef4444'
      default: return '#f59e0b'
    }
  }

  return (
    <div className="chat-container">
      <div className="connection-status" style={{ color: getConnectionStatusColor() }}>
        ● {connectionStatus === 'connected' ? 'AI Connected' : connectionStatus === 'error' ? 'Backend Offline' : 'Checking...'}
      </div>
      
      <div className="messages-area">
        {messages.length === 0 && (
          <div className="message ai-message">
            Log interaction details here (e.g., 'Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure') or ask for help.
          </div>
        )}
        
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.type}-message`}>
            <div className="message-content">
              {message.content}
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="message ai-message">
            <div className="loading">🤖 AI is analyzing... Please wait</div>
          </div>
        )}
        
        {error && (
          <div className="message error-message">
            ❌ Error: {error}
            <br />Make sure backend is running on http://localhost:8000
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Describe interaction..."
          disabled={loading}
          rows={1}
        />
        <button 
          onClick={handleSend} 
          disabled={loading || !input.trim()}
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  )
}

export default ChatInterface