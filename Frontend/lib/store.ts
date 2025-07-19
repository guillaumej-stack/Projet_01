import { create } from 'zustand'
import { sessionManager } from './session'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  isLoading?: boolean
}

export interface AnalysisState {
  subreddit: string
  isAnalyzing: boolean
  analysisResults: any
  recommendations: any
}

interface ChatStore {
  messages: Message[]
  isTyping: boolean
  sessionId: string
  addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => void
  setTyping: (isTyping: boolean) => void
  clearMessages: () => void
  setSessionId: (sessionId: string) => void
  initializeFromSession: () => void
}

interface AnalysisStore {
  state: AnalysisState
  setSubreddit: (subreddit: string) => void
  setAnalyzing: (isAnalyzing: boolean) => void
  setAnalysisResults: (results: any) => void
  setRecommendations: (recommendations: any) => void
  reset: () => void
  initializeFromSession: () => void
}

export const useChatStore = create<ChatStore>((set, get) => ({
  messages: [],
  isTyping: false,
  sessionId: sessionManager.getSessionId(), // Utiliser l'ID de session généré
  
  addMessage: (message) => {
    const newMessage = {
      ...message,
      id: Date.now().toString(),
      timestamp: new Date(),
    }
    
    set((state) => {
      const updatedMessages = [...state.messages, newMessage]
      // Sauvegarder dans sessionStorage
      sessionManager.saveMessages(updatedMessages)
      return { messages: updatedMessages }
    })
  },
  
  setTyping: (isTyping) => set({ isTyping }),
  
  clearMessages: () => {
    set({ messages: [] })
    // Effacer aussi de sessionStorage
    sessionManager.saveMessages([])
  },
  
  setSessionId: (sessionId) => set({ sessionId }),
  
  initializeFromSession: () => {
    // Charger les messages depuis sessionStorage au démarrage
    const savedMessages = sessionManager.getMessages()
    if (savedMessages.length > 0) {
      // Reconstituer les dates des messages
      const messagesWithDates = savedMessages.map(msg => ({
        ...msg,
        timestamp: new Date(msg.timestamp)
      }))
      set({ 
        messages: messagesWithDates,
        sessionId: sessionManager.getSessionId()
      })
    } else {
      set({ sessionId: sessionManager.getSessionId() })
    }
  }
}))

export const useAnalysisStore = create<AnalysisStore>((set, get) => ({
  state: {
    subreddit: '',
    isAnalyzing: false,
    analysisResults: null,
    recommendations: null,
  },
  
  setSubreddit: (subreddit) =>
    set((state) => ({
      state: { ...state.state, subreddit },
    })),
     
  setAnalyzing: (isAnalyzing) =>
    set((state) => ({
      state: { ...state.state, isAnalyzing },
    })),
     
  setAnalysisResults: (analysisResults) => {
    set((state) => ({
      state: { ...state.state, analysisResults },
    }))
    // Sauvegarder dans sessionStorage
    sessionManager.saveAnalysisResults(analysisResults)
  },
  
  setRecommendations: (recommendations) =>
    set((state) => ({
      state: { ...state.state, recommendations },
    })),
     
  reset: () => {
    set({
      state: {
        subreddit: '',
        isAnalyzing: false,
        analysisResults: null,
        recommendations: null,
      },
    })
    // Effacer de sessionStorage
    sessionManager.saveAnalysisResults(null)
  },
  
  initializeFromSession: () => {
    // Charger les résultats d'analyse depuis sessionStorage
    const savedResults = sessionManager.getAnalysisResults()
    if (savedResults) {
      set((state) => ({
        state: { ...state.state, analysisResults: savedResults }
      }))
    }
  }
}))