import { useState } from 'react'
import type { Mensagem } from '../../lib/types'
import { enviarMensagem } from '../../lib/api'
import { MessageList } from '../../components/MessageList'
import { MessageInput } from '../../components/InputChat'
import { Loading } from '../../components/Loading'

export function Chat() {
  const [mensagens, setMensagens] = useState<Mensagem[]>([])
  const [carregando, setCarregando] = useState(false)

  const aoEnviarMensagem = async (texto: string) => {
    // adiciona a mensagem do usuário
    const novaMensagemUser: Mensagem = {
      role: 'user',
      content: texto,
    }
    setMensagens((prev) => [...prev, novaMensagemUser])
    setCarregando(true)

    try {
      const resposta = await enviarMensagem(texto)

      // adiciona a resposta do assistente
      const novaMensagemAssistant: Mensagem = {
        role: 'assistant',
        content: resposta.answer,
        sources: resposta.sources,
      }
      setMensagens((prev) => [...prev, novaMensagemAssistant])
    } catch (erro) {
      console.error('Erro ao enviar mensagem:', erro)
      
      // Extrai a mensagem de erro (pode vir do backend ou ser genérica)
      const mensagemErroTexto = erro instanceof Error 
        ? erro.message 
        : 'Desculpe, não consegui processar sua mensagem. Tente novamente.'
      
      // mostra erro pro usuário
      const mensagemErro: Mensagem = {
        role: 'assistant',
        content: mensagemErroTexto,
      }
      setMensagens((prev) => [...prev, mensagemErro])
    } finally {
      setCarregando(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg flex flex-col h-[600px]">
      <MessageList mensagens={mensagens} />
      
      {carregando && (
        <div className="px-4 py-3">
          <Loading />
        </div>
      )}

      <MessageInput aoEnviar={aoEnviarMensagem} carregando={carregando} />
    </div>
  )
}

