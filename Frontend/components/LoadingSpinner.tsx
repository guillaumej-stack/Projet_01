import { motion } from 'framer-motion'

interface LoadingSpinnerProps {
  message?: string
  size?: 'sm' | 'md' | 'lg'
}

export default function LoadingSpinner({ 
  message = "Analyse en cours...", 
  size = 'md' 
}: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  }

  return (
    <div className="flex flex-col items-center justify-center p-8">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        className={`${sizeClasses[size]} border-2 border-primary-200 border-t-primary-600 rounded-full`}
      />
      
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="mt-4 text-gray-600 text-center"
      >
        {message}
      </motion.p>
      
      <div className="loading-dots mt-2">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  )
} 