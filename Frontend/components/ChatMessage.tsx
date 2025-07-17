import { Message } from '@/lib/store'
import { motion } from 'framer-motion'
import { UserIcon, CpuChipIcon } from '@heroicons/react/24/outline'

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
          <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
            <CpuChipIcon className="w-5 h-5 text-primary-600" />
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
                <div className="w-6 h-6 bg-primary-600 rounded-full flex items-center justify-center">
                  <UserIcon className="w-4 h-4 text-white" />
                </div>
              </div>
            )}
            
            <div className="flex-1">
              <div className="text-sm font-medium mb-1">
                {isUser ? 'Vous' : 'Assistant Reddit'}
              </div>
              <div className="whitespace-pre-wrap">{message.content}</div>
              <div className="text-xs text-gray-500 mt-2">
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