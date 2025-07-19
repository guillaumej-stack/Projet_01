import toast from 'react-hot-toast'
import { redditAPI } from './api'

// Types pour les états de connexion
export interface ConnectionStatus {
  isConnected: boolean
  isHealthy: boolean
  lastChecked: Date
  error?: string
}

// Vérifier la connexion au backend
export async function checkBackendConnection(): Promise<ConnectionStatus> {
  try {
    const response = await redditAPI.healthCheck()
    return {
      isConnected: true,
      isHealthy: response.status === 'healthy',
      lastChecked: new Date(),
    }
  } catch (error) {
    return {
      isConnected: false,
      isHealthy: false,
      lastChecked: new Date(),
      error: error instanceof Error ? error.message : 'Erreur inconnue'
    }
  }
}

// Wrapper pour les appels API avec gestion d'erreur automatique
export async function safeApiCall<T>(
  apiCall: () => Promise<T>,
  errorMessage?: string
): Promise<T | null> {
  try {
    return await apiCall()
  } catch (error) {
    console.error('API Error:', error)
    
    const message = errorMessage || 'Erreur lors de la communication avec le serveur'
    toast.error(message)
    
    return null
  }
}

// Validation des paramètres d'analyse
export interface AnalysisParams {
  subredditName: string
  numPosts?: number
  commentsLimit?: number
  sortCriteria?: string
  timeFilter?: string
}

export function validateAnalysisParams(params: AnalysisParams): string[] {
  const errors: string[] = []
  
  if (!params.subredditName || params.subredditName.trim().length === 0) {
    errors.push('Le nom du subreddit est requis')
  }
  
  if (params.subredditName && params.subredditName.length > 21) {
    errors.push('Le nom du subreddit ne peut pas dépasser 21 caractères')
  }
  
  if (params.numPosts !== undefined && (params.numPosts < 1 || params.numPosts > 100)) {
    errors.push('Le nombre de posts doit être entre 1 et 100')
  }
  
  if (params.commentsLimit !== undefined && (params.commentsLimit < 1 || params.commentsLimit > 50)) {
    errors.push('Le nombre de commentaires doit être entre 1 et 50')
  }
  
  const validSortCriteria = ['hot', 'new', 'top', 'rising']
  if (params.sortCriteria && !validSortCriteria.includes(params.sortCriteria)) {
    errors.push('Critère de tri invalide')
  }
  
  const validTimeFilters = ['hour', 'day', 'week', 'month', 'year', 'all']
  if (params.timeFilter && !validTimeFilters.includes(params.timeFilter)) {
    errors.push('Filtre de temps invalide')
  }
  
  return errors
}

// Extraire le nom du subreddit depuis un message
export function extractSubredditName(message: string): string | null {
  // Recherche r/subreddit ou /r/subreddit
  const match = message.match(/(?:\/)?r\/([a-zA-Z0-9_]+)/i)
  if (match && match[1]) {
    return match[1]
  }
  
  // Recherche un nom de subreddit simple (sans r/)
  const words = message.split(' ')
  for (const word of words) {
    if (word.length > 2 && word.length <= 21 && /^[a-zA-Z0-9_]+$/.test(word)) {
      return word
    }
  }
  
  return null
}

// Formater les réponses pour l'affichage
export function formatApiResponse(response: string): string {
  // Remplacer les sauts de ligne par des <br> pour l'affichage HTML
  return response
    .replace(/\n\n/g, '<br><br>')
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
}

// Détecter le type de message (analyse, question générale, etc.)
export function detectMessageType(message: string): 'analysis' | 'check' | 'export' | 'general' {
  const lowerMessage = message.toLowerCase()
  
  if (lowerMessage.includes('analys') || lowerMessage.includes('examine')) {
    return 'analysis'
  }
  
  if (lowerMessage.includes('existe') || lowerMessage.includes('vérif') || lowerMessage.includes('check')) {
    return 'check'
  }
  
  if (lowerMessage.includes('export') || lowerMessage.includes('télécharg') || lowerMessage.includes('download')) {
    return 'export'
  }
  
  return 'general'
}

// Gestionnaire d'état pour la reconnexion automatique
export class ConnectionManager {
  private checkInterval: NodeJS.Timeout | null = null
  private onStatusChange?: (status: ConnectionStatus) => void
  
  constructor(onStatusChange?: (status: ConnectionStatus) => void) {
    this.onStatusChange = onStatusChange
  }
  
  startMonitoring(intervalMs: number = 1000000) {
    this.stopMonitoring()
    
    this.checkInterval = setInterval(async () => {
      const status = await checkBackendConnection()
      this.onStatusChange?.(status)
      
      if (!status.isConnected) {
        toast.error('Connexion au serveur perdue', { id: 'connection-lost' })
      }
    }, intervalMs)
  }
  
  stopMonitoring() {
    if (this.checkInterval) {
      clearInterval(this.checkInterval)
      this.checkInterval = null
    }
  }
} 