export function Input({ className, ...props }: React.InputHTMLAttributes<HTMLInputElement>) {
  return <input className="px-4 h-10 w-full rounded-md border border-slate-200 outline-none focus:border-slate-400" {...props} />
}
