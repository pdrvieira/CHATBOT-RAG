import type { ChatRequest, ChatResponse } from './types'

const API_URL = 'http://localhost:8000'

export async function enviarMensagem(question: string): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question } as ChatRequest),
  })

  if (!response.ok) {
    // Tenta pegar a mensagem de erro do backend
    let errorMessage = `Erro na API: ${response.status} ${response.statusText}`
    
    try {
      const errorData = await response.json()
      if (errorData.detail) {
        errorMessage = errorData.detail
      }
    } catch {
      // Se não conseguir parsear JSON, usa a mensagem padrão
    }
    
    throw new Error(errorMessage)
  }

  const data: ChatResponse = await response.json()
  return data
}

