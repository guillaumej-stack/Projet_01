import axios, { AxiosResponse } from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Client API avec configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000000,
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

// Types pour les réponses API (alignés avec le backend FastAPI)
export interface ChatResponse {
  success: boolean
  response: string
  session_id: string
}

export interface HealthResponse {
  status: string
  agents: string
  database: string
}

export interface SubredditCheckResponse {
  success: boolean
  response: string
  subreddit: string
}

export interface AnalysisResponse {
  success: boolean
  response: string
  subreddit: string
  parameters: {
    num_posts: number
    comments_limit: number
    sort_criteria: string
    time_filter: string
  }
}

export interface ExportResponse {
  success: boolean
  response: string
  format: string
}

export interface ClearHistoryResponse {
  success: boolean
  message: string
}

// API Functions alignées avec le backend FastAPI
export const redditAPI = {
  // Vérifier l'état de l'API
  async healthCheck(): Promise<HealthResponse> {
    const response: AxiosResponse<HealthResponse> = await apiClient.get('/health')
    return response.data
  },

  // Chat avec l'assistant (endpoint principal)
  async sendChatMessage(message: string, sessionId?: string): Promise<ChatResponse> {
    const response: AxiosResponse<ChatResponse> = await apiClient.post('/chat', {
      message: message,
      session_id: sessionId || 'default'
    })
    return response.data
  },

  // Vérifier si un subreddit existe
  async checkSubreddit(subredditName: string): Promise<SubredditCheckResponse> {
    const response: AxiosResponse<SubredditCheckResponse> = await apiClient.post('/check_subreddit', {
      subreddit_name: subredditName
    })
    return response.data
  },

  // Analyser un subreddit
  async analyzeSubreddit(
    subredditName: string, 
    numPosts: number = 5, 
    commentsLimit: number = 5,
    sortCriteria: string = 'top',
    timeFilter: string = 'month'
  ): Promise<AnalysisResponse> {
    const response: AxiosResponse<AnalysisResponse> = await apiClient.post('/analyze', {
      subreddit_name: subredditName,
      num_posts: numPosts,
      comments_limit: commentsLimit,
      sort_criteria: sortCriteria,
      time_filter: timeFilter
    })
    return response.data
  },

  // Export des résultats
  async exportResults(formatType: string = 'pdf', subreddit?: string): Promise<ExportResponse> {
    const response: AxiosResponse<ExportResponse> = await apiClient.post('/export', {
      format_type: formatType,
      subreddit: subreddit
    })
    return response.data
  },

  // Nettoyer l'historique de conversation
  async clearChatHistory(sessionId?: string): Promise<ClearHistoryResponse> {
    const response: AxiosResponse<ClearHistoryResponse> = await apiClient.delete('/clear_history', {
      data: {
        session_id: sessionId || 'default'
      }
    })
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