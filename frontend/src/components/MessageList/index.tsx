import { useEffect, useRef } from 'react'
import type { Mensagem } from '../../lib/types'
import { MessageBubble } from '../Mensagem'

interface MessageListProps {
  mensagens: Mensagem[]
}

export function MessageList({ mensagens }: MessageListProps) {
  const finalRef = useRef<HTMLDivElement>(null)

  // scroll automático pra última mensagem
  useEffect(() => {
    finalRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [mensagens])

  if (mensagens.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center px-4 py-12">
        <div className="text-4xl mb-4">🐾</div>
        <h3 className="text-lg font-medium text-slate-700 mb-2">
          Olá! Como posso ajudar?
        </h3>
        <p className="text-sm text-slate-500 max-w-md">
          Pergunte sobre serviços, horários, banho e tosa, vacinas ou qualquer dúvida sobre o petshop.
        </p>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-4 p-4 overflow-y-auto max-h-[500px]">
      {mensagens.map((msg, idx) => (
        <MessageBubble key={idx} mensagem={msg} />
      ))}
      <div ref={finalRef} />
    </div>
  )
}

