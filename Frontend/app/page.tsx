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
  const { messages, addMessage, setTyping, clearMessages } = useChatStore()
  const { state, setAnalyzing, setAnalysisResults, setRecommendations } = useAnalysisStore()
  const [isProcessing, setIsProcessing] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll vers le bas
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Message de bienvenue
  useEffect(() => {
    if (messages.length === 0) {
      addMessage({
        role: 'assistant',
        content: `Bonjour ! Je suis votre assistant d'analyse Reddit. Je peux analyser n'importe quel subreddit pour identifier les problèmes récurrents des utilisateurs et vous proposer des opportunités business.

Quel subreddit souhaitez-vous analyser ?`
      })
    }
  }, [messages.length, addMessage])

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isProcessing) return

    // Ajouter le message utilisateur
    addMessage({ role: 'user', content })
    setIsProcessing(true)
    setTyping(true)

    try {
      // Appel réel à l'API FastAPI
      const response = await redditAPI.sendChatMessage(content)
      
      if (response.success) {
        // Ajouter la réponse de l'assistant
        addMessage({ role: 'assistant', content: response.response })
        
        // Si c'est une analyse, traiter les résultats
        if (response.analysis_results) {
          setAnalyzing(true)
          setTimeout(() => {
            setAnalysisResults(response.analysis_results)
            setAnalyzing(false)
          }, 2000)
        }
      } else {
        addMessage({ 
          role: 'assistant', 
          content: `❌ ${response.response}` 
        })
      }
      
    } catch (error) {
      console.error('Erreur:', error)
      addMessage({ 
        role: 'assistant', 
        content: '❌ Erreur de connexion au serveur. Vérifiez que l\'API est en cours d\'exécution.' 
      })
      toast.error('Erreur de connexion au serveur')
    } finally {
      setIsProcessing(false)
      setTyping(false)
    }
  }

  const simulateBackendResponse = async (message: string): Promise<string> => {
    // Simulation de réponse - à remplacer par votre API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if (message.toLowerCase().includes('bonjour') || message.toLowerCase().includes('salut')) {
      return 'Bonjour ! Comment puis-je vous aider aujourd\'hui ?'
    }
    
    if (message.toLowerCase().includes('aide') || message.toLowerCase().includes('help')) {
      return `Je peux vous aider à analyser n'importe quel subreddit. Voici ce que je fais :

1. **Scraping intelligent** : Je récupère les posts et commentaires les plus pertinents
2. **Analyse des douleurs** : J'identifie les problèmes récurrents des utilisateurs
3. **Détection de solutions** : Je trouve les commentaires proposant des solutions
4. **Recommandations business** : Je génère des opportunités commerciales

Dites-moi simplement quel subreddit vous voulez analyser !`
    }
    
    return 'Je comprends votre demande. Pouvez-vous me donner plus de détails sur ce que vous souhaitez analyser ?'
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
      await new Promise(resolve => setTimeout(resolve, 2000))
      toast.success(`✅ Export ${format.toUpperCase()} terminé !`)
    } catch (error) {
      toast.error('❌ Erreur lors de l\'export')
    }
  }

  const handleClearChat = () => {
    clearMessages()
    setAnalysisResults(null)
    setRecommendations(null)
    toast.success('Chat effacé')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <CpuChipIcon className="w-8 h-8 text-reddit-600" />
              <h1 className="text-xl font-bold text-gray-900">
                Reddit Agents
              </h1>
            </div>
            
            <div className="flex items-center gap-2">
              <button
                onClick={handleClearChat}
                className="btn-secondary flex items-center gap-2"
              >
                <ArrowPathIcon className="w-4 h-4" />
                Nouveau chat
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Chat Section */}
          <div className="lg:col-span-2">
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

          {/* Results Section */}
          <div className="lg:col-span-1">
            <div className="sticky top-8">
              {state.analysisResults ? (
                <AnalysisResults
                  results={state.analysisResults}
                  onExport={handleExport}
                />
              ) : (
                <div className="card">
                  <div className="text-center text-gray-500">
                    <DocumentTextIcon className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                    <h3 className="text-lg font-medium mb-2">
                      Aucune analyse
                    </h3>
                    <p className="text-sm">
                      Lancez une analyse pour voir les résultats ici
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 