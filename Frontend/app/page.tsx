'use client'

import { useState, useEffect, useRef } from 'react'
import { useChatStore, useAnalysisStore } from '@/lib/store'
import { redditAPI } from '@/lib/api'
import ChatMessage from '@/components/ChatMessage'
import ChatInput from '@/components/ChatInput'
import AnalysisForm from '@/components/AnalysisForm'

import { 
  BanknotesIcon,
  SparklesIcon, 
  ArrowPathIcon
} from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'

export default function Home() {
  const { messages, addMessage, setTyping, clearMessages, sessionId, setSessionId } = useChatStore()
  const { state, setAnalysisResults, setRecommendations } = useAnalysisStore()
  const [isProcessing, setIsProcessing] = useState(false)
  const [isAnalysisRunning, setIsAnalysisRunning] = useState(false)
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

  const handleClearHistory = () => {
    // Effacer seulement l'UI, pas l'historique en base
    clearMessages()
    setAnalysisResults(null)
    setRecommendations(null)
    welcomeMessageAdded.current = false // Réinitialise le flag pour le message de bienvenue
    
    // Générer un nouveau session_id
    const newSessionId = crypto.randomUUID()
    setSessionId(newSessionId)
    
    toast.success('Nouveau chat ouvert')
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







  return (
    <div className="h-screen bg-amber-50 flex flex-col">
      {/* Header */}
      <header className="bg-gradient-to-r from-amber-500 to-amber-600 shadow-lg border-b border-amber-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-center h-16">
            {/* Titre centré */}
            <div className="flex items-center gap-3">
              <BanknotesIcon className="w-8 h-8 text-white" />
              <h1 className="text-xl font-bold text-white">
                Reddit Goldmine
              </h1>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex-1">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Menu Section - Gauche */}
          <div className="lg:col-span-1">
            <div className="sticky top-8">
              <div className="card">
                <div className="p-4">
                  
                  {/* Bouton Nouveau Chat */}
                  <button
                    onClick={handleClearHistory}
                    className="w-full btn-secondary flex items-center gap-2 justify-center mb-3"
                  >
                    <ArrowPathIcon className="w-4 h-4" />
                    Nouveau chat
                  </button>
                  
                  {/* Formulaire d'analyse */}
                  <AnalysisForm 
                    onAnalysisStart={() => setIsAnalysisRunning(true)}
                    onAnalysisComplete={() => setIsAnalysisRunning(false)}
                  />

                </div>
              </div>
            </div>
          </div>

          {/* Chat Section - Droite (2/3) */}
          <div className="lg:col-span-2">
            <div className="card flex-1 flex flex-col">
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
                

                
                <div ref={messagesEndRef} />
              </div>
              
              <div className="p-4 border-t border-gray-200">
                <ChatInput
                  onSendMessage={handleSendMessage}
                  disabled={isProcessing || isAnalysisRunning}
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