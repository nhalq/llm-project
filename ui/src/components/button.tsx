import { clsfmt } from 'lib/utils'

type ButtonType = 'primary' | 'secondary'

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  buttonType?: ButtonType
}

export function Button({ buttonType, className, ...props }: ButtonProps) {
  return (
    <button
      className={clsfmt(
        'px-4 py-2 min-w-10 flex items-center justify-center border rounded-md hover:bg-slate-100 active:bg-slate-200',
        buttonType === 'primary' &&
          'bg-slate-700 hover:bg-slate-600 active:bg-slate-800 text-white',
        className
      )}
      {...props}
    />
  )
}
