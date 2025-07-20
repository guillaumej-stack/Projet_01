import { Message } from '@/lib/store'
import { motion } from 'framer-motion'
import { UserIcon, WrenchIcon, FaceSmileIcon } from '@heroicons/react/24/outline'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface ChatMessageProps {
  message: Message
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user'
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      {!isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-[#DAA520] rounded-full flex items-center justify-center">
            <WrenchIcon className="w-5 h-5 text-black" />
          </div>
        </div>
      )}
      
      <div className={`max-w-4xl ${isUser ? 'order-first' : ''}`}>
        <div
          className={`chat-message ${
            isUser ? 'user' : 'assistant'
          }`}
        >
          <div className="flex items-start gap-2">
            {isUser && (
              <div className="flex-shrink-0">
                <div className="w-6 h-6 bg-[#A0522D] rounded-full flex items-center justify-center">
                  <FaceSmileIcon className="w-4 h-4 text-white" />
                </div>
              </div>
            )}
            
            <div className="flex-1">
              <div className={`text-sm font-medium mb-1 ${isUser ? 'text-[#8B4513]' : 'text-[#DAA520]'}`}>
                {isUser ? 'Vous' : 'Reddit Golddigger'}
              </div>
              
              {/* Contenu avec support Markdown */}
              <div className="prose prose-sm max-w-none dark:prose-invert">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    // Personnalisation des composants markdown
                    p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                    strong: ({ children }) => <strong className="font-bold text-gray-900">{children}</strong>,
                    em: ({ children }) => <em className="italic text-gray-800">{children}</em>,
                    code: ({ children }) => (
                      <code className="bg-gray-100 px-1.5 py-0.5 rounded text-sm font-mono text-red-600">
                        {children}
                      </code>
                    ),
                    pre: ({ children }) => (
                      <pre className="bg-gray-100 p-3 rounded-md overflow-x-auto my-2">
                        {children}
                      </pre>
                    ),
                    ul: ({ children }) => <ul className="list-disc list-inside mb-2">{children}</ul>,
                    ol: ({ children }) => <ol className="list-decimal list-inside mb-2">{children}</ol>,
                    li: ({ children }) => <li className="mb-1">{children}</li>,
                    h1: ({ children }) => <h1 className="text-xl font-bold mb-2">{children}</h1>,
                    h2: ({ children }) => <h2 className="text-lg font-bold mb-2">{children}</h2>,
                    h3: ({ children }) => <h3 className="text-md font-bold mb-1">{children}</h3>,
                    blockquote: ({ children }) => (
                      <blockquote className="border-l-4 border-gray-300 pl-4 italic my-2">
                        {children}
                      </blockquote>
                    ),
                    a: ({ href, children }) => (
                      <a 
                        href={href} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 underline"
                      >
                        {children}
                      </a>
                    ),
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </div>
              
              <div className={`text-xs mt-2 ${isUser ? 'text-[#A0522D]' : 'text-[#8B4513]'}`}>
                {message.timestamp.toLocaleTimeString('fr-FR', {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  )
} 