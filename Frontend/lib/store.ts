import { create } from 'zustand'

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
  addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => void
  setTyping: (isTyping: boolean) => void
  clearMessages: () => void
}

interface AnalysisStore {
  state: AnalysisState
  setSubreddit: (subreddit: string) => void
  setAnalyzing: (isAnalyzing: boolean) => void
  setAnalysisResults: (results: any) => void
  setRecommendations: (recommendations: any) => void
  reset: () => void
}

export const useChatStore = create<ChatStore>((set) => ({
  messages: [],
  isTyping: false,
  addMessage: (message) =>
    set((state) => ({
      messages: [
        ...state.messages,
        {
          ...message,
          id: Date.now().toString(),
          timestamp: new Date(),
        },
      ],
    })),
  setTyping: (isTyping) => set({ isTyping }),
  clearMessages: () => set({ messages: [] }),
}))

export const useAnalysisStore = create<AnalysisStore>((set) => ({
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
  setAnalysisResults: (analysisResults) =>
    set((state) => ({
      state: { ...state.state, analysisResults },
    })),
  setRecommendations: (recommendations) =>
    set((state) => ({
      state: { ...state.state, recommendations },
    })),
  reset: () =>
    set({
      state: {
        subreddit: '',
        isAnalyzing: false,
        analysisResults: null,
        recommendations: null,
      },
    }),
})) 