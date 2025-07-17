import { useState, useRef, useEffect } from 'react'
import { PaperAirplaneIcon } from '@heroicons/react/24/outline'

interface ChatInputProps {
  onSendMessage: (message: string) => void
  disabled?: boolean
  placeholder?: string
}

export default function ChatInput({ 
  onSendMessage, 
  disabled = false, 
  placeholder = "Tapez votre message..." 
}: ChatInputProps) {
  const [message, setMessage] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (message.trim() && !disabled) {
      onSendMessage(message.trim())
      setMessage('')
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [message])

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 items-end">
      <div className="flex-1 relative">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          className="input-field resize-none min-h-[44px] max-h-32 py-3 pr-12"
          rows={1}
        />
      </div>
      
      <button
        type="submit"
        disabled={!message.trim() || disabled}
        className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed p-3"
      >
        <PaperAirplaneIcon className="w-5 h-5" />
      </button>
    </form>
  )
} 