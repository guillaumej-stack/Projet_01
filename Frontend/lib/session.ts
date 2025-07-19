// Gestionnaire de session pour persist dans la session courante uniquement
// Se renouvelle à chaque fermeture/actualisation de page

export interface SessionData {
  sessionId: string
  createdAt: Date
  messages: any[]
  analysisResults: any
}

class SessionManager {
  private static instance: SessionManager
  private sessionId: string
  private storageKey = 'reddit-analysis-session'

  private constructor() {
    // Générer un nouvel ID de session à chaque instanciation (= chaque actualisation/ouverture)
    this.sessionId = this.generateSessionId()
    this.initializeSession()
  }

  public static getInstance(): SessionManager {
    if (!SessionManager.instance) {
      SessionManager.instance = new SessionManager()
    }
    return SessionManager.instance
  }

  private generateSessionId(): string {
    // Format: timestamp + random string
    const timestamp = Date.now()
    const randomPart = Math.random().toString(36).substring(2, 15)
    return `session_${timestamp}_${randomPart}`
  }

  private initializeSession(): void {
    // Toujours créer une nouvelle session (ne pas récupérer l'ancienne)
    const sessionData: SessionData = {
      sessionId: this.sessionId,
      createdAt: new Date(),
      messages: [],
      analysisResults: null
    }
    
    this.saveToSessionStorage(sessionData)
    console.log(`🆔 Nouvelle session créée: ${this.sessionId}`)
  }

  public getSessionId(): string {
    return this.sessionId
  }

  public saveMessages(messages: any[]): void {
    const sessionData = this.getSessionData()
    if (sessionData) {
      sessionData.messages = messages
      this.saveToSessionStorage(sessionData)
    }
  }

  public getMessages(): any[] {
    const sessionData = this.getSessionData()
    return sessionData?.messages || []
  }

  public saveAnalysisResults(results: any): void {
    const sessionData = this.getSessionData()
    if (sessionData) {
      sessionData.analysisResults = results
      this.saveToSessionStorage(sessionData)
    }
  }

  public getAnalysisResults(): any {
    const sessionData = this.getSessionData()
    return sessionData?.analysisResults || null
  }

  public clearSession(): void {
    sessionStorage.removeItem(this.storageKey)
    this.initializeSession()
  }

  private getSessionData(): SessionData | null {
    try {
      const stored = sessionStorage.getItem(this.storageKey)
      if (stored) {
        const parsed = JSON.parse(stored)
        // Reconstituer les dates
        parsed.createdAt = new Date(parsed.createdAt)
        return parsed
      }
    } catch (error) {
      console.error('Erreur lors de la lecture de la session:', error)
    }
    return null
  }

  private saveToSessionStorage(data: SessionData): void {
    try {
      sessionStorage.setItem(this.storageKey, JSON.stringify(data))
    } catch (error) {
      console.error('Erreur lors de la sauvegarde de la session:', error)
    }
  }

  public getSessionInfo(): { sessionId: string; createdAt: Date; messageCount: number } {
    const data = this.getSessionData()
    return {
      sessionId: this.sessionId,
      createdAt: data?.createdAt || new Date(),
      messageCount: data?.messages?.length || 0
    }
  }
}

// Export de l'instance singleton
export const sessionManager = SessionManager.getInstance()

// Utilitaires pour React
export const useSessionPersistence = () => {
  return {
    sessionId: sessionManager.getSessionId(),
    saveMessages: sessionManager.saveMessages.bind(sessionManager),
    getMessages: sessionManager.getMessages.bind(sessionManager),
    saveAnalysisResults: sessionManager.saveAnalysisResults.bind(sessionManager),
    getAnalysisResults: sessionManager.getAnalysisResults.bind(sessionManager),
    clearSession: sessionManager.clearSession.bind(sessionManager),
    getSessionInfo: sessionManager.getSessionInfo.bind(sessionManager)
  }
} 