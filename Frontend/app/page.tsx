'use client'

import { useState, useEffect, useRef } from 'react'
import { useChatStore, useAnalysisStore } from '@/lib/store'
import { redditAPI } from '@/lib/api'
import ChatMessage from '@/components/ChatMessage'
import ChatInput from '@/components/ChatInput'
import AnalysisResults from '@/components/AnalysisResults'
import LoadingSpinner from '@/components/LoadingSpinner'
import { 
  CpuChipIcon, 
  ArrowPathIcon,
  DocumentTextIcon 
} from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'

export default function Home() {
  const { messages, addMessage, setTyping, clearMessages, sessionId } = useChatStore()
  const { state, setAnalyzing, setAnalysisResults, setRecommendations } = useAnalysisStore()
  const [isProcessing, setIsProcessing] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const welcomeMessageAdded = useRef(false)

  // Auto-scroll vers le bas
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Message de bienvenue - s'exécute une seule fois
  useEffect(() => {
    if (messages.length === 0 && !welcomeMessageAdded.current) {
      welcomeMessageAdded.current = true
      addMessage({
        role: 'assistant',
        content: `Bonjour ! Je suis votre assistant d'analyse Reddit. Je peux analyser n'importe quel subreddit pour identifier les problèmes récurrents des utilisateurs et vous proposer des opportunités business.

Quel subreddit souhaitez-vous analyser ?`
      })
    }
  }, [messages.length])

  const handleClearHistory = async () => {
    try {
      const response = await redditAPI.clearChatHistory(sessionId)
      if (response.success) {
        clearMessages()
        welcomeMessageAdded.current = false // Réinitialise le flag pour le message de bienvenue
        toast.success(response.message || 'Historique nettoyé')
      } else {
        toast.error('Erreur lors du nettoyage de l\'historique')
      }
    } catch (error) {
      console.error('Erreur lors du nettoyage:', error)
      toast.error('Erreur lors du nettoyage de l\'historique')
    }
  }




const handleSendMessage = async (content: string) => {
  if (!content.trim() || isProcessing) return

  addMessage({ role: 'user', content })
  setIsProcessing(true)
  setTyping(true)

  try {
    // Appel direct à l'API FastAPI backend
    const response = await redditAPI.sendChatMessage(content, sessionId)
    
    if (response.success) {
      addMessage({ role: 'assistant', content: response.response })
      
      // Vérifier si le message contient des mots-clés d'analyse pour déclencher l'affichage des résultats
      if (content.toLowerCase().includes('analyse') || content.toLowerCase().includes('analyser')) {
        // Optionnel : déclencher une analyse séparée si nécessaire
        // Cette logique peut être ajustée selon vos besoins
      }
    } else {
      addMessage({ 
        role: 'assistant', 
        content: `❌ Erreur: ${response.response}` 
      })
    }
    
  } catch (error) {
    console.error('Erreur:', error)
    const errorMessage = error instanceof Error ? error.message : 'Erreur de connexion au serveur'
    addMessage({ 
      role: 'assistant', 
      content: `❌ ${errorMessage}` 
    })
    toast.error('Erreur de connexion au serveur')
  } finally {
    setIsProcessing(false)
    setTyping(false)
  }
}

  const handleAnalysis = async (message: string) => {
    setAnalyzing(true)
    
    try {
      // Extraire le nom du subreddit du message
      const subredditMatch = message.match(/r\/(\w+)/i)
      const subreddit = subredditMatch ? subredditMatch[1] : 'programming'
      
      // Simuler l'analyse (à remplacer par votre API)
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      const mockResults = {
        subreddit,
        posts_analyzed: 15,
        total_comments_analyzed: 150,
        top_3_pains: [
          {
            pain_type: 'Complexité technique',
            score: 85.2,
            summary: 'Les développeurs rencontrent des difficultés avec les nouvelles technologies'
          },
          {
            pain_type: 'Documentation insuffisante',
            score: 72.8,
            summary: 'Manque de documentation claire et à jour'
          },
          {
            pain_type: 'Performance',
            score: 68.4,
            summary: 'Problèmes de performance et d\'optimisation'
          }
        ],
        solutions_found: [
          {
            comment_id: '1',
            author: 'dev_expert',
            solution_text: 'Créez un guide étape par étape avec des exemples concrets',
            score: 45
          }
        ],
        overall_summary: 'Le subreddit révèle des défis techniques récurrents avec un besoin fort de documentation et d\'outils d\'aide.'
      }
      
      setAnalysisResults(mockResults)
      toast.success('✅ Analyse terminée avec succès !')
      
    } catch (error) {
      console.error('Erreur analyse:', error)
      toast.error('❌ Erreur lors de l\'analyse')
    } finally {
      setAnalyzing(false)
    }
  }

  const handleExport = async (format: 'pdf' | 'csv' | 'txt') => {
    try {
      toast.loading(`Export en cours (${format.toUpperCase()})...`)
      
      const subreddit = state.analysisResults?.subreddit
      const response = await redditAPI.exportResults(format, subreddit)
      
      if (response.success) {
        toast.success(`✅ Export ${format.toUpperCase()} terminé !`)
        // Vous pouvez ajouter ici la logique pour télécharger le fichier
        // si votre backend retourne un lien de téléchargement
      } else {
        toast.error(`❌ Erreur lors de l'export: ${response.response}`)
      }
    } catch (error) {
      console.error('Erreur export:', error)
      toast.error('❌ Erreur lors de l\'export')
    }
  }

  const handleClearChat = () => {
    clearMessages()
    setAnalysisResults(null)
    setRecommendations(null)
    welcomeMessageAdded.current = false // Réinitialise le flag pour le message de bienvenue
    toast.success('Chat effacé')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-center h-16">
            {/* Titre centré */}
            <div className="flex items-center gap-3">
              <CpuChipIcon className="w-8 h-8 text-reddit-600" />
              <h1 className="text-xl font-bold text-gray-900">
                Reddit Analysis
              </h1>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Menu Section - Gauche */}
          <div className="lg:col-span-1">
            <div className="sticky top-8">
              <div className="card">
                <div className="p-4">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Actions
                  </h3>
                  
                  {/* Bouton Nouveau Chat */}
                  <button
                    onClick={handleClearHistory}
                    className="w-full btn-secondary flex items-center gap-2 justify-center mb-3"
                  >
                    <ArrowPathIcon className="w-4 h-4" />
                    Nouveau chat
                  </button>
                  
                  {/* Boutons Export */}
                  <div className="space-y-2">
                    <h4 className="text-sm font-medium text-gray-700 mb-2">
                      Exporter les résultats
                    </h4>
                    
                    <button
                      onClick={() => handleExport('pdf')}
                      className="w-full btn-outline flex items-center gap-2 justify-center"
                      disabled={!state.analysisResults}
                    >
                      <DocumentTextIcon className="w-4 h-4" />
                      Export PDF
                    </button>
                    
                    <button
                      onClick={() => handleExport('csv')}
                      className="w-full btn-outline flex items-center gap-2 justify-center"
                      disabled={!state.analysisResults}
                    >
                      <DocumentTextIcon className="w-4 h-4" />
                      Export CSV
                    </button>
                    
                    <button
                      onClick={() => handleExport('txt')}
                      className="w-full btn-outline flex items-center gap-2 justify-center"
                      disabled={!state.analysisResults}
                    >
                      <DocumentTextIcon className="w-4 h-4" />
                      Export TXT
                    </button>
                  </div>
                  
                  {/* Résultats d'analyse compacts */}
                  {state.analysisResults && (
                    <div className="mt-6 pt-4 border-t border-gray-200">
                      <h4 className="text-sm font-medium text-gray-700 mb-2">
                        Dernière analyse
                      </h4>
                      <div className="text-xs text-gray-600 space-y-1">
                        <p>Subreddit: r/{state.analysisResults.subreddit}</p>
                        <p>Posts: {state.analysisResults.posts_analyzed}</p>
                        <p>Commentaires: {state.analysisResults.total_comments_analyzed}</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Chat Section - Droite (3/4) */}
          <div className="lg:col-span-3">
            <div className="card h-[600px] flex flex-col">
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
                
                {state.isAnalyzing && (
                  <div className="flex justify-center">
                    <LoadingSpinner message="Analyse en cours..." />
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>
              
              <div className="p-4 border-t border-gray-200">
                <ChatInput
                  onSendMessage={handleSendMessage}
                  disabled={isProcessing}
                  placeholder="Tapez votre message ou dites-moi quel subreddit analyser..."
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 