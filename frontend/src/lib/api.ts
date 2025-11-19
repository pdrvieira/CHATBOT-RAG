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
    throw new Error(`Erro na API: ${response.status} ${response.statusText}`)
  }

  const data: ChatResponse = await response.json()
  return data
}

