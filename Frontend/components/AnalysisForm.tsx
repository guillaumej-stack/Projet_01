import { useState } from 'react'
import { ChartBarIcon } from '@heroicons/react/24/outline'
import { redditAPI } from '@/lib/api'
import { useChatStore } from '@/lib/store'
import toast from 'react-hot-toast'

console.log('🔍 [DEBUG] AnalysisForm importé')

interface AnalysisFormProps {
  onAnalysisStart?: () => void
  onAnalysisComplete?: () => void
}

export default function AnalysisForm({ onAnalysisStart, onAnalysisComplete }: AnalysisFormProps) {
  console.log('🔍 [DEBUG] AnalysisForm rendu')
  const { addMessage, sessionId, setTyping, messages } = useChatStore()
  console.log('🔍 [DEBUG] Store récupéré, addMessage:', typeof addMessage)
  
  // États du formulaire
  const [subreddit, setSubreddit] = useState('')
  const [numPosts, setNumPosts] = useState(5)
  const [commentsPerPost, setCommentsPerPost] = useState(5)
  const [selectedCriteria, setSelectedCriteria] = useState('top')
  const [timeFilter, setTimeFilter] = useState('month')
  const [isLoading, setIsLoading] = useState(false)

  // Critères disponibles
  const criteriaOptions = [
    { value: 'top', label: 'Top' },
    { value: 'hot', label: 'Hot' },
    { value: 'new', label: 'New' },
    { value: 'rising', label: 'Rising' },
    { value: 'best', label: 'Best' }
]

  // Périodes disponibles
  const timeOptions = [
    { value: 'now', label: 'Maintenant' },
    { value: 'today', label: 'Aujourd\'hui' },
    { value: 'week', label: 'Cette semaine' },
    { value: 'month', label: 'Ce mois-ci' },
    { value: 'year', label: 'Cette année' },
    { value: 'all', label: 'Toutes périodes confondues' }
  ]

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    console.log('🔍 [DEBUG] Formulaire soumis')
    
    if (!subreddit.trim()) {
      toast.error('Veuillez entrer un nom de subreddit')
      return
    }

    // Nettoyer le nom du subreddit (enlever r/ si présent)
    const cleanSubreddit = subreddit.replace(/^r\//, '').trim()
    
    console.log('🔍 [DEBUG] Subreddit nettoyé:', cleanSubreddit)
    
    if (!cleanSubreddit) {
      toast.error('Nom de subreddit invalide')
      return
    }

    setIsLoading(true)
    setTyping(true) // Bloquer le chat
    onAnalysisStart?.()

    try {
      // Construire le message pour l'agent 0
      const analysisMessage = `Analyse le subreddit r/${cleanSubreddit} avec ${numPosts} posts, ${commentsPerPost} commentaires par post, critère ${selectedCriteria}, période ${timeFilter}. Je confirme bien que je suis sûr et je valide les paramètres.`
      
      // Ajouter le message de l'utilisateur dans le chat
      addMessage({ role: 'user', content: analysisMessage })
      // Envoyer via le système de chat existant (agent 0)
      const response = await redditAPI.sendChatMessage(analysisMessage, sessionId)

      console.log('🔍 [DEBUG] Réponse API:', response)

      if (response.success) {
        // Ajouter la réponse de l'Agent 0 au chat
        addMessage({ role: 'assistant', content: response.response })
        // Réinitialiser le formulaire
        setSubreddit('')
        setNumPosts(5)
        setCommentsPerPost(5)
        setSelectedCriteria('top')
        setTimeFilter('month')
      } else {
        toast.error(`❌ Erreur: ${response.response}`)
      }

    } catch (error) {
      console.error('Erreur analyse:', error)
      toast.error('❌ Erreur lors de l\'envoi de l\'analyse')
    } finally {
      setIsLoading(false)
      setTyping(false) // Débloquer le chat
      onAnalysisComplete?.() // Notifier que l'analyse est terminée
    }
  }

  return (
    <div className="card mt-4">
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Analyse de Subreddit
        </h3>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Input Subreddit */}
          <div>
            <label className={`block text-sm font-medium mb-2 ${isLoading ? 'text-gray-400' : 'text-gray-700'}`}>
              Subreddit
            </label>
            <input
              type="text"
              value={subreddit}
              onChange={(e) => setSubreddit(e.target.value)}
              placeholder="r/subreddit"
              className={`input-field ${isLoading ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : ''}`}
              required
              disabled={isLoading}
            />
          </div>

          {/* Slider Nombre de posts */}
          <div className="slider-with-markers">
            <label className={`block text-sm font-medium mb-2 ${isLoading ? 'text-gray-400' : 'text-gray-700'}`}>
              Nombre de posts : {numPosts}
            </label>
            <input
              type="range"
              min="5"
              max="50"
              value={numPosts}
              onChange={(e) => setNumPosts(parseInt(e.target.value))}
              className={`w-full h-2 rounded-lg appearance-none slider ${isLoading ? 'bg-gray-200 cursor-not-allowed' : 'bg-amber-200 cursor-pointer'}`}
              disabled={isLoading}
            />
            <div className={`flex justify-between text-xs mt-1 ${isLoading ? 'text-gray-400' : 'text-gray-500'}`}>
              <span>5</span>
              <span>50</span>
            </div>
          </div>

          {/* Slider Commentaires par post */}
          <div className="slider-with-markers">
            <label className={`block text-sm font-medium mb-2 ${isLoading ? 'text-gray-400' : 'text-gray-700'}`}>
              Commentaires par post : {commentsPerPost}
            </label>
            <input
              type="range"
              min="5"
              max="50"
              value={commentsPerPost}
              onChange={(e) => setCommentsPerPost(parseInt(e.target.value))}
              className={`w-full h-2 rounded-lg appearance-none slider ${isLoading ? 'bg-gray-200 cursor-not-allowed' : 'bg-amber-200 cursor-pointer'}`}
              disabled={isLoading}
            />
            <div className={`flex justify-between text-xs mt-1 ${isLoading ? 'text-gray-400' : 'text-gray-500'}`}>
              <span>5</span>
              <span>50</span>
            </div>
          </div>

          {/* Critères */}
          <div>
            <label className={`block text-sm font-medium mb-2 ${isLoading ? 'text-gray-400' : 'text-gray-700'}`}>
              Critères
            </label>
            <select
              value={selectedCriteria}
              onChange={(e) => setSelectedCriteria(e.target.value)}
              className={`input-field ${isLoading ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : ''}`}
              disabled={isLoading}
            >
              {criteriaOptions.map((criteria) => (
                <option key={criteria.value} value={criteria.value}>
                  {criteria.label}
                </option>
              ))}
            </select>
          </div>

          {/* Menu déroulant Période */}
          <div>
            <label className={`block text-sm font-medium mb-2 ${isLoading ? 'text-gray-400' : 'text-gray-700'}`}>
              Période
            </label>
            <select
              value={timeFilter}
              onChange={(e) => setTimeFilter(e.target.value)}
              className={`input-field ${isLoading ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : ''}`}
              disabled={isLoading}
            >
              {timeOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {/* Bouton d'analyse */}
          <button
            type="submit"
            disabled={isLoading || !subreddit.trim()}
            className="w-full bg-amber-500 hover:bg-amber-600 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-1"
            onClick={() => console.log('🔍 [DEBUG] Bouton cliqué')}
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <ChartBarIcon className="w-4 h-4" />
                Analyse en cours...
              </>
            ) : (
              <>
                <ChartBarIcon className="w-4 h-4" />
                Demander une analyse
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  )
} 