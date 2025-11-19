export function Loading() {
  return (
    <div className="flex items-center gap-2 text-slate-500">
      <div className="flex gap-1">
        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></span>
      </div>
      <span className="text-sm">Gerando resposta...</span>
    </div>
  )
}
