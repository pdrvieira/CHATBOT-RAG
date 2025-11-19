export type TipoMensagem = 'user' | 'assistant'

export interface Mensagem {
  role: TipoMensagem
  content: string
  sources?: string[]
}

export interface ChatRequest {
  question: string
}

export interface ChatResponse {
  answer: string
  sources: string[]
}

