import { Chat } from './sections/Chat'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <header className="text-center mb-6">
          <h1 className="text-3xl font-bold text-slate-800 mb-2">
            🐾 Chat Petshop
          </h1>
          <p className="text-slate-600 text-sm">
            Tire suas dúvidas sobre serviços, horários e cuidados para seu pet
          </p>
        </header>

        <Chat />
      </div>
    </div>
  )
}

export default App

