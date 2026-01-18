import { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { updateFormData } from '../slices/chatSlice.js'
import './StructuredForm.css'

function StructuredForm() {
  const dispatch = useDispatch()
  const { formData } = useSelector(state => state.chat)
  
  const [materials, setMaterials] = useState([])
  const [samples, setSamples] = useState([])
  const [aiSuggestions] = useState([
    'Schedule a follow-up meeting in 2 weeks',
    'Send OncoBoost Phase III PDF',
    'Add Dr. Sharma to the advisory board invite list'
  ])

  // Update local materials and samples when Redux formData changes
  useEffect(() => {
    if (formData.materials_shared && Array.isArray(formData.materials_shared)) {
      setMaterials(formData.materials_shared)
    }
    if (formData.samples_distributed && Array.isArray(formData.samples_distributed)) {
      setSamples(formData.samples_distributed)
    }
  }, [formData.materials_shared, formData.samples_distributed])

  const handleChange = (e) => {
    const { name, value } = e.target
    dispatch(updateFormData({ [name]: value }))
  }

  const addMaterial = () => {
    const material = prompt('Material name:')
    if (material) {
      const newMaterials = [...materials, material]
      setMaterials(newMaterials)
      dispatch(updateFormData({ materials_shared: newMaterials }))
    }
  }

  const addSample = () => {
    const sample = prompt('Sample name:')
    if (sample) {
      const newSamples = [...samples, sample]
      setSamples(newSamples)
      dispatch(updateFormData({ samples_distributed: newSamples }))
    }
  }

  const addSuggestion = (suggestion) => {
    const currentActions = formData.follow_up_actions
    const newActions = currentActions ? `${currentActions}\n${suggestion}` : suggestion
    dispatch(updateFormData({ follow_up_actions: newActions }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    const structuredInput = `
📝 HCP Interaction Log:

🔹 Interaction Details:
• HCP Name: ${formData.hcp_name}
• Type: ${formData.interaction_type}
• Date: ${formData.date}
• Time: ${formData.time}
• Attendees: ${formData.attendees}
• Topics: ${formData.topics_discussed}

🔹 Materials & Samples:
• Materials Shared: ${materials.join(', ') || 'None'}
• Samples Distributed: ${samples.join(', ') || 'None'}

🔹 HCP Sentiment: ${formData.hcp_sentiment}

🔹 Outcomes & Follow-up:
• Outcomes: ${formData.outcomes}
• Follow-up Actions: ${formData.follow_up_actions}

🤖 AI Description: ${formData.ai_description}
    `.trim()

    dispatch(sendMessage(structuredInput))
  }

  return (
    <div className="structured-form">
      <div className="single-form-container">
        <div className="form-grid">
          {/* Basic Details */}
          <div className="form-group">
            <label>HCP Name *</label>
            <input
              type="text"
              name="hcp_name"
              value={formData.hcp_name}
              onChange={handleChange}
              placeholder="Dr. John Smith"
            />
          </div>

          <div className="form-group">
            <label>Interaction Type</label>
            <select
              name="interaction_type"
              value={formData.interaction_type}
              onChange={handleChange}
            >
              <option value="meeting">Meeting</option>
              <option value="call">Call</option>
              <option value="visit">Visit</option>
              <option value="virtual">Virtual</option>
              <option value="conference">Conference</option>
            </select>
          </div>

          <div className="form-group">
            <label>Date</label>
            <input
              type="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Time</label>
            <input
              type="time"
              name="time"
              value={formData.time}
              onChange={handleChange}
            />
          </div>

          <div className="form-group full-width">
            <label>Attendees</label>
            <input
              type="text"
              name="attendees"
              value={formData.attendees}
              onChange={handleChange}
              placeholder="Names of people present in meeting"
            />
          </div>

          <div className="form-group full-width">
            <label>Topics Discussed</label>
            <textarea
              name="topics_discussed"
              value={formData.topics_discussed}
              onChange={handleChange}
              placeholder="Product details, efficacy, pricing, etc."
              rows={2}
            />
          </div>


          <div className="form-group">
            <label>Materials Shared</label>
            <div className="materials-list">
              {materials.map((material, index) => (
                <span key={index} className="material-tag">
                  {material}
                  <button type="button" onClick={() => {
                    const newMaterials = materials.filter((_, i) => i !== index)
                    setMaterials(newMaterials)
                    dispatch(updateFormData({ materials_shared: newMaterials }))
                  }}>×</button>
                </span>
              ))}
              <button type="button" className="add-btn" onClick={addMaterial}>
                ➕ Add Material
              </button>
            </div>
          </div>

          <div className="form-group">
            <label>Samples Distributed</label>
            <input
              type="text"
              name="samples_distributed"
              value={Array.isArray(formData.samples_distributed) ? formData.samples_distributed.join(', ') : formData.samples_distributed || ''}
              onChange={(e) => {
                const value = e.target.value
                const samplesArray = value ? value.split(',').map(s => s.trim()).filter(s => s) : []
                setSamples(samplesArray)
                dispatch(updateFormData({ samples_distributed: samplesArray }))
              }}
              placeholder="Product Sample, Trial Pack, etc."
            />
          </div>

          {/* HCP Sentiment */}
          <div className="form-group full-width">
            <label>HCP Sentiment</label>
            <div className="sentiment-options">
              <label className={`sentiment-option ${formData.hcp_sentiment === 'positive' ? 'active' : ''}`}>
                <input
                  type="radio"
                  name="hcp_sentiment"
                  value="positive"
                  checked={formData.hcp_sentiment === 'positive'}
                  onChange={handleChange}
                />
                <span className="sentiment-icon">✅</span>
                Positive
              </label>
              
              <label className={`sentiment-option ${formData.hcp_sentiment === 'neutral' ? 'active' : ''}`}>
                <input
                  type="radio"
                  name="hcp_sentiment"
                  value="neutral"
                  checked={formData.hcp_sentiment === 'neutral'}
                  onChange={handleChange}
                />
                <span className="sentiment-icon">⚪</span>
                Neutral
              </label>
              
              <label className={`sentiment-option ${formData.hcp_sentiment === 'negative' ? 'active' : ''}`}>
                <input
                  type="radio"
                  name="hcp_sentiment"
                  value="negative"
                  checked={formData.hcp_sentiment === 'negative'}
                  onChange={handleChange}
                />
                <span className="sentiment-icon">❌</span>
                Negative
              </label>
            </div>
          </div>

          <div className="form-group full-width">
            <label>Outcomes</label>
            <textarea
              name="outcomes"
              value={formData.outcomes}
              onChange={handleChange}
              placeholder="Interest shown, trial agreed, etc."
              rows={2}
            />
          </div>

          <div className="form-group full-width">
            <label>Follow-up Actions</label>
            <textarea
              name="follow_up_actions"
              value={formData.follow_up_actions}
              onChange={handleChange}
              placeholder="Next meeting, email, call, etc."
              rows={2}
            />
          </div>

          <div className="form-group full-width">
            <label>🤖 AI Assistant - Describe Interaction</label>
            <textarea
              name="ai_description"
              value={formData.ai_description}
              onChange={handleChange}
              placeholder="Describe your interaction in natural language - AI will auto-fill the form"
              rows={3}
            />
          </div>

          <div className="form-group full-width">
            <label>🤖 AI Suggested Follow-ups</label>
            <div className="ai-suggestions">
              {aiSuggestions.map((suggestion, index) => (
                <button
                  key={index}
                  type="button"
                  className="suggestion-btn"
                  onClick={() => addSuggestion(suggestion)}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        </div>
        
        <div className="auto-fill-indicator">
          🤖 Form auto-fills as you chat with AI
        </div>
      </div>
    </div>
  )
}

export default StructuredForm