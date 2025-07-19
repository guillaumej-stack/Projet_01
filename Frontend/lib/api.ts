import axios, { AxiosResponse } from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Client API avec configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Intercepteur pour les erreurs
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// Types pour les réponses API
export interface SubredditInfo {
  success: boolean
  exists: boolean
  subreddit: string
  title?: string
  subscribers?: number
  description?: string
  error?: string
}

export interface AnalysisResult {
  success: boolean
  message: string
  data?: {
    subreddit: string
    posts_to_analyze: number
    comments_limit: number
    sort_criteria: string
    status: string
  }
}

export interface ChatResponse {
  success: boolean
  response: string
  session_id?: string
  analysis_results?: {
    subreddit: string
    subscribers: number
    status: string
  }
}

export interface StoredSolution {
  id: number
  comment_id: string
  post_id: string
  author: string
  solution_text: string
  score: number
  pain_type: string
  intensity: number
  subreddit: string
  created_at: string
}

export interface StoredSolutionsResponse {
  success: boolean
  solutions: StoredSolution[]
  count: number
  error?: string
}

// API Functions
export const redditAPI = {
  // Vérifier si un subreddit existe
  async checkSubreddit(subredditName: string): Promise<SubredditInfo> {
    const response: AxiosResponse<SubredditInfo> = await apiClient.post('/check_subreddit', {
      subreddit_name: subredditName
    })
    return response.data
  },

  // Analyser un subreddit
  async analyzeSubreddit(
    subredditName: string, 
    numPosts: number = 10, 
    commentsLimit: number = 10,
    sortCriteria: string = 'top'
  ): Promise<AnalysisResult> {
    const response: AxiosResponse<AnalysisResult> = await apiClient.post('/analyze_subreddit', {
      subreddit_name: subredditName,
      num_posts: numPosts,
      comments_limit: commentsLimit,
      sort_criteria: sortCriteria
    })
    return response.data
  },

  // Chat avec l'assistant
  async sendChatMessage(message: string, sessionId?: string): Promise<ChatResponse> {
    const response: AxiosResponse<ChatResponse> = await apiClient.post('/chat', {
      message: message,
      session_id: sessionId || 'default'
    })
    return response.data
  },

  // Nettoyer l'historique de conversation
  async clearChatHistory(sessionId?: string): Promise<any> {
    const response = await apiClient.post('/chat/clear_history', {}, {
      params: { session_id: sessionId || 'default' }
    })
    return response.data
  },

  // Récupérer l'historique de conversation
  async getChatHistory(sessionId?: string): Promise<any> {
    const response = await apiClient.get('/chat/history', {
      params: { session_id: sessionId || 'default' }
    })
    return response.data
  },

  // Récupérer les solutions stockées
  async getStoredSolutions(subreddit?: string, limit: number = 10): Promise<StoredSolutionsResponse> {
    const params = new URLSearchParams()
    if (subreddit) params.append('subreddit', subreddit)
    params.append('limit', limit.toString())
    
    const response: AxiosResponse<StoredSolutionsResponse> = await apiClient.get(`/stored_solutions?${params}`)
    return response.data
  },

  // Export des résultats
  async exportResults(format: string = 'pdf'): Promise<any> {
    const response = await apiClient.post('/export_results', {
      format_type: format
    })
    return response.data
  },

  // Vérifier l'état de l'API
  async healthCheck(): Promise<any> {
    const response = await apiClient.get('/')
    return response.data
  }
}

// Utilitaires pour gérer les erreurs
export const handleApiError = (error: any): string => {
  if (error.response?.status === 404) {
    return "Service non trouvé"
  }
  if (error.response?.status === 500) {
    return "Erreur interne du serveur"
  }
  if (error.code === 'ECONNREFUSED') {
    return "Impossible de se connecter au serveur. Vérifiez que l'API est en cours d'exécution."
  }
  if (error.response?.data?.detail) {
    return error.response.data.detail
  }
  return error.message || "Erreur inconnue"
}

export default redditAPI 