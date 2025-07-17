import { motion } from 'framer-motion'
import { 
  ChartBarIcon, 
  LightBulbIcon, 
  DocumentTextIcon,
  ArrowDownTrayIcon 
} from '@heroicons/react/24/outline'

interface AnalysisResultsProps {
  results: any
  onExport: (format: 'pdf' | 'csv' | 'txt') => void
}

export default function AnalysisResults({ results, onExport }: AnalysisResultsProps) {
  if (!results) return null

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      {/* En-tête */}
      <div className="card">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Analyse de r/{results.subreddit}
            </h2>
            <p className="text-gray-600">
              {results.posts_analyzed} posts analysés • {results.total_comments_analyzed} commentaires
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => onExport('pdf')}
              className="btn-secondary flex items-center gap-2"
            >
              <DocumentTextIcon className="w-4 h-4" />
              PDF
            </button>
            <button
              onClick={() => onExport('csv')}
              className="btn-secondary flex items-center gap-2"
            >
              <ArrowDownTrayIcon className="w-4 h-4" />
              CSV
            </button>
          </div>
        </div>
      </div>

      {/* Top 3 des douleurs */}
      {results.top_3_pains && results.top_3_pains.length > 0 && (
        <div className="card">
          <div className="flex items-center gap-2 mb-4">
            <ChartBarIcon className="w-6 h-6 text-reddit-600" />
            <h3 className="text-xl font-semibold">Top 3 des problèmes identifiés</h3>
          </div>
          
          <div className="space-y-4">
            {results.top_3_pains.map((pain: any, index: number) => (
              <motion.div
                key={pain.pain_type}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="border-l-4 border-reddit-500 pl-4 py-2"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-semibold text-gray-900">
                      #{index + 1} {pain.pain_type}
                    </h4>
                    <p className="text-gray-600 text-sm mt-1">
                      {pain.summary}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-reddit-600">
                      {pain.score}
                    </div>
                    <div className="text-xs text-gray-500">
                      Score de priorité
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Solutions trouvées */}
      {results.solutions_found && results.solutions_found.length > 0 && (
        <div className="card">
          <div className="flex items-center gap-2 mb-4">
            <LightBulbIcon className="w-6 h-6 text-green-600" />
            <h3 className="text-xl font-semibold">
              Solutions exceptionnelles trouvées ({results.solutions_found.length})
            </h3>
          </div>
          
          <div className="space-y-3">
            {results.solutions_found.slice(0, 5).map((solution: any, index: number) => (
              <motion.div
                key={solution.comment_id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-green-50 border border-green-200 rounded-lg p-4"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-sm text-gray-600 mb-2">
                      Par {solution.author} • Score: {solution.score}
                    </p>
                    <p className="text-gray-900">{solution.solution_text}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Résumé global */}
      {results.overall_summary && (
        <div className="card">
          <h3 className="text-xl font-semibold mb-4">Résumé de l'analyse</h3>
          <p className="text-gray-700 leading-relaxed">
            {results.overall_summary}
          </p>
        </div>
      )}
    </motion.div>
  )
} 