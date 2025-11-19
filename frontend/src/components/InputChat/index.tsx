import { useState, KeyboardEvent } from 'react'

interface MessageInputProps {
  aoEnviar: (mensagem: string) => void
  carregando: boolean
}

export function MessageInput({ aoEnviar, carregando }: MessageInputProps) {
  const [texto, setTexto] = useState('')

  const enviar = () => {
    if (texto.trim() && !carregando) {
      aoEnviar(texto.trim())
      setTexto('')
    }
  }

  // enter envia, shift+enter quebra linha
  const aoTeclar = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      enviar()
    }
  }

  return (
    <div className="flex gap-2 p-4 border-t border-slate-200">
      <textarea
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        onKeyDown={aoTeclar}
        placeholder="Digite sua pergunta..."
        disabled={carregando}
        rows={1}
        className="flex-1 resize-none rounded-lg border border-slate-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-slate-100 disabled:cursor-not-allowed"
      />
      <button
        onClick={enviar}
        disabled={!texto.trim() || carregando}
        className="px-6 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors"
      >
        Enviar
      </button>
    </div>
  )
}

