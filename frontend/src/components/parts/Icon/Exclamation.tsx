import clsx from 'clsx'

interface Props {
  size: string
  className?: string
}

export default function IconExclamation(props: Props): JSX.Element {
  const { size, className = '' } = props

  return (
    <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" className={clsx('bi bi-exclamation-lg', className)} viewBox="0 0 16 16">
      <path d="M7.005 3.1a1 1 0 1 1 1.99 0l-.388 6.35a.61.61 0 0 1-1.214 0L7.005 3.1ZM7 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0Z" />
    </svg>
  )
}
