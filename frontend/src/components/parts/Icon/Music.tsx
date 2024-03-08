import clsx from 'clsx'

interface Props {
  size: string
  className?: string
}

export default function IconMusic(props: Props) {
  const { size, className = '' } = props

  return (
    <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" className={clsx('bi bi-headphones', className)} viewBox="0 0 16 16">
      <path d="M8 3a5 5 0 0 0-5 5v1h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V8a6 6 0 1 1 12 0v5a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1V8a5 5 0 0 0-5-5z" />
    </svg>
  )
}
