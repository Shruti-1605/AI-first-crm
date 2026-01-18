import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

export const sendMessage = createAsyncThunk(
  'chat/sendMessage',
  async (message) => {
    const response = await axios.post(`${API_BASE}/chat`, { message })
    return { message, response: response.data }
  }
)

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: [],
    loading: false,
    error: null,
    mode: 'both',
    // Form data that AI will fill
    formData: {
      hcp_name: '',
      interaction_type: 'meeting',
      date: '',
      time: '',
      attendees: '',
      topics_discussed: '',
      voice_note_summary: '',
      materials_shared: [],
      samples_distributed: [],
      hcp_sentiment: 'neutral',
      outcomes: '',
      follow_up_actions: '',
      ai_description: ''
    }
  },
  reducers: {
    setMode: (state, action) => {
      state.mode = action.payload
    },
    clearMessages: (state) => {
      state.messages = []
    },
    updateFormData: (state, action) => {
      state.formData = { ...state.formData, ...action.payload }
    },
    clearFormData: (state) => {
      state.formData = {
        hcp_name: '',
        interaction_type: 'meeting',
        date: '',
        time: '',
        attendees: '',
        topics_discussed: '',
        voice_note_summary: '',
        materials_shared: [],
        samples_distributed: [],
        hcp_sentiment: 'neutral',
        outcomes: '',
        follow_up_actions: '',
        ai_description: ''
      }
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.loading = false
        
        // Add user message
        state.messages.push({
          type: 'user',
          content: action.payload.message,
          timestamp: new Date().toISOString()
        })
        
        // Add AI response
        state.messages.push({
          type: 'ai',
          content: action.payload.response.response,
          action_taken: action.payload.response.action_taken,
          tools_used: action.payload.response.tools_used,
          timestamp: new Date().toISOString()
        })
        
        // Extract form data from AI response
        const userMessage = action.payload.message.toLowerCase()
        const aiResponse = action.payload.response.response.toLowerCase()
        
        // Auto-fill form based on conversation
        const updates = {}
        
        // Set current date and time if not already set
        if (!state.formData.date) {
          const now = new Date()
          updates.date = now.toISOString().split('T')[0]
          updates.time = now.toTimeString().slice(0, 5)
        }
        
        // Extract HCP name
        const hcpMatch = action.payload.message.match(/dr\.?\s+([a-z]+)/i)
        if (hcpMatch) {
          updates.hcp_name = `Dr. ${hcpMatch[1]}`
        }
        
        // Extract interaction type
        if (userMessage.includes('met') || userMessage.includes('meeting')) {
          updates.interaction_type = 'meeting'
        } else if (userMessage.includes('call') || userMessage.includes('phone')) {
          updates.interaction_type = 'call'
        } else if (userMessage.includes('visit') || userMessage.includes('visited')) {
          updates.interaction_type = 'visit'
        } else if (userMessage.includes('email')) {
          updates.interaction_type = 'email'
        }
        
        // Extract attendees
        if (userMessage.includes('with') && !userMessage.includes('discussed with')) {
          const attendeesMatch = userMessage.match(/with\s+([^.]+)/)
          if (attendeesMatch) {
            updates.attendees = attendeesMatch[1].trim()
          }
        }
        
        // Extract topics discussed
        if (userMessage.includes('discuss') || userMessage.includes('talk') || userMessage.includes('about')) {
          const topicsPatterns = [
            /discuss(?:ed)?\s+(.+?)(?:\.|,|$)/,
            /talk(?:ed)?\s+about\s+(.+?)(?:\.|,|$)/,
            /about\s+(.+?)(?:\.|,|$)/
          ]
          
          for (const pattern of topicsPatterns) {
            const match = userMessage.match(pattern)
            if (match) {
              updates.topics_discussed = match[1].trim()
              break
            }
          }
        }
        
        // Extract materials shared
        const materials = []
        if (userMessage.includes('brochure')) materials.push('Product Brochure')
        if (userMessage.includes('pdf')) materials.push('PDF Document')
        if (userMessage.includes('oncoboost')) materials.push('OncoBoost Phase III PDF')
        if (userMessage.includes('study') || userMessage.includes('research')) materials.push('Clinical Study Data')
        if (userMessage.includes('presentation')) materials.push('Product Presentation')
        if (materials.length > 0) {
          updates.materials_shared = materials
        }
        
        // Extract samples
        const samples = []
        if (userMessage.includes('sample')) samples.push('Product Sample')
        if (userMessage.includes('trial pack')) samples.push('Trial Pack')
        if (samples.length > 0) {
          updates.samples_distributed = samples
        }
        
        // Extract sentiment
        if (userMessage.includes('positive') || userMessage.includes('good') || userMessage.includes('great') || 
            userMessage.includes('excellent') || userMessage.includes('interested') || userMessage.includes('happy')) {
          updates.hcp_sentiment = 'positive'
        } else if (userMessage.includes('negative') || userMessage.includes('bad') || userMessage.includes('poor') || 
                   userMessage.includes('disappointed') || userMessage.includes('unhappy')) {
          updates.hcp_sentiment = 'negative'
        } else if (userMessage.includes('neutral') || userMessage.includes('okay') || userMessage.includes('fine')) {
          updates.hcp_sentiment = 'neutral'
        }
        
        // Extract outcomes - more comprehensive patterns
        if (userMessage.includes('agreed') || userMessage.includes('interested') || userMessage.includes('positive response') ||
            userMessage.includes('showed interest') || userMessage.includes('very interested') || userMessage.includes('keen') ||
            userMessage.includes('excited') || userMessage.includes('enthusiastic') || userMessage.includes('impressed')) {
          updates.outcomes = 'Positive engagement and interest shown'
        } else if (userMessage.includes('declined') || userMessage.includes('not interested') || userMessage.includes('rejected') ||
                   userMessage.includes('refused') || userMessage.includes('hesitant') || userMessage.includes('skeptical')) {
          updates.outcomes = 'Declined or showed limited interest'
        } else if (userMessage.includes('will consider') || userMessage.includes('thinking') || userMessage.includes('review') ||
                   userMessage.includes('discuss internally') || userMessage.includes('need time')) {
          updates.outcomes = 'Will consider and get back'
        } else if (userMessage.includes('trial') || userMessage.includes('pilot') || userMessage.includes('test')) {
          updates.outcomes = 'Agreed to trial or pilot program'
        } else if (userMessage.includes('questions') || userMessage.includes('concerns') || userMessage.includes('clarification')) {
          updates.outcomes = 'Had questions and concerns addressed'
        } else if (userMessage.includes('meeting') || userMessage.includes('discussion') || userMessage.includes('conversation')) {
          updates.outcomes = 'Productive discussion held'
        }
        
        // Extract follow-up actions from AI response or user message
        if (aiResponse.includes('follow-up') || aiResponse.includes('meeting') || userMessage.includes('schedule')) {
          updates.follow_up_actions = 'Schedule follow-up meeting in 2 weeks'
        } else if (aiResponse.includes('send') && aiResponse.includes('pdf')) {
          updates.follow_up_actions = 'Send OncoBoost Phase III PDF'
        } else if (aiResponse.includes('advisory board')) {
          updates.follow_up_actions = 'Add Dr. to advisory board invite list'
        }
        
        // Set AI description as the user's message
        updates.ai_description = action.payload.message
        
        // Update form data
        if (Object.keys(updates).length > 0) {
          state.formData = { ...state.formData, ...updates }
        }
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
  }
})

export const { setMode, clearMessages, updateFormData, clearFormData } = chatSlice.actions
export default chatSlice.reducer