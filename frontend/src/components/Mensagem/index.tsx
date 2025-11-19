import type { Mensagem } from '../../lib/types'

interface MessageBubbleProps {
  mensagem: Mensagem
}

export function MessageBubble({ mensagem }: MessageBubbleProps) {
  const isUser = mensagem.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-3 ${
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-slate-100 text-slate-800'
        }`}
      >
        <p className="text-sm leading-relaxed whitespace-pre-wrap">
          {mensagem.content}
        </p>

        {/* mostra as fontes se tiver */}
        {mensagem.sources && mensagem.sources.length > 0 && (
          <div className="mt-2 pt-2 border-t border-slate-300/50">
            <p className="text-xs text-slate-600 mb-1">Fontes:</p>
            <ul className="text-xs text-slate-500 space-y-0.5">
              {mensagem.sources.map((source, idx) => (
                <li key={idx}>• {source}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

