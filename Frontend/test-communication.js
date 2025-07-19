#!/usr/bin/env node

/**
 * Script de test de communication Frontend-Backend
 * Usage: node test-communication.js
 */

const axios = require('axios')

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Configuration du client de test
const testClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Tests de communication
const tests = [
  {
    name: 'Health Check',
    method: 'GET',
    endpoint: '/health',
    data: null,
    expectedFields: ['status', 'agents', 'database']
  },
  {
    name: 'Root Endpoint',
    method: 'GET', 
    endpoint: '/',
    data: null,
    expectedFields: ['message', 'version', 'endpoints']
  },
  {
    name: 'Chat Message',
    method: 'POST',
    endpoint: '/chat',
    data: { message: 'Bonjour, es-tu en ligne ?', session_id: 'test' },
    expectedFields: ['success', 'response', 'session_id']
  },
  {
    name: 'Check Subreddit',
    method: 'POST',
    endpoint: '/check_subreddit',
    data: { subreddit_name: 'programming' },
    expectedFields: ['success', 'response', 'subreddit']
  }
]

// Fonction de test
async function runTest(test) {
  try {
    console.log(`\n🧪 Test: ${test.name}`)
    console.log(`   ${test.method} ${test.endpoint}`)
    
    let response
    if (test.method === 'GET') {
      response = await testClient.get(test.endpoint)
    } else if (test.method === 'POST') {
      response = await testClient.post(test.endpoint, test.data)
    } else if (test.method === 'DELETE') {
      response = await testClient.delete(test.endpoint, { data: test.data })
    }
    
    // Vérifier le statut HTTP
    if (response.status === 200) {
      console.log(`   ✅ Statut HTTP: ${response.status}`)
    } else {
      console.log(`   ⚠️  Statut HTTP: ${response.status}`)
    }
    
    // Vérifier les champs attendus
    const data = response.data
    console.log('   📄 Réponse:', JSON.stringify(data, null, 2).substring(0, 200) + '...')
    
    if (test.expectedFields) {
      const missingFields = test.expectedFields.filter(field => !(field in data))
      if (missingFields.length === 0) {
        console.log(`   ✅ Tous les champs attendus sont présents`)
      } else {
        console.log(`   ❌ Champs manquants: ${missingFields.join(', ')}`)
      }
    }
    
    return { success: true, data }
    
  } catch (error) {
    console.log(`   ❌ Erreur: ${error.message}`)
    if (error.response) {
      console.log(`   📄 Statut: ${error.response.status}`)
      console.log(`   📄 Données: ${JSON.stringify(error.response.data)}`)
    }
    return { success: false, error }
  }
}

// Fonction principale
async function main() {
  console.log('🚀 Test de Communication Frontend-Backend')
  console.log('==========================================')
  console.log(`🔗 URL Backend: ${API_BASE_URL}`)
  
  let passedTests = 0
  let totalTests = tests.length
  
  for (const test of tests) {
    const result = await runTest(test)
    if (result.success) {
      passedTests++
    }
    
    // Attendre un peu entre les tests
    await new Promise(resolve => setTimeout(resolve, 500))
  }
  
  console.log('\n📊 Résultats des tests:')
  console.log('========================')
  console.log(`✅ Tests réussis: ${passedTests}/${totalTests}`)
  console.log(`❌ Tests échoués: ${totalTests - passedTests}/${totalTests}`)
  
  if (passedTests === totalTests) {
    console.log('\n🎉 Tous les tests ont réussi ! La communication fonctionne correctement.')
    process.exit(0)
  } else {
    console.log('\n⚠️  Certains tests ont échoué. Vérifiez que le backend est démarré.')
    console.log('    Commande: cd Backend && uv run core/api.py')
    process.exit(1)
  }
}

// Gestion des erreurs globales
process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ Erreur non gérée:', reason)
  process.exit(1)
})

process.on('uncaughtException', (error) => {
  console.error('❌ Exception non capturée:', error)
  process.exit(1)
})

// Lancement des tests
if (require.main === module) {
  main()
} 