import clsx from 'clsx'

interface Props {
  size: string
  className?: string
}

export default function IconCircle(props: Props) {
  const { size, className = '' } = props

  return (
    <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" className={clsx('bi bi-circle-fill', className)} viewBox="0 0 16 16">
      <circle cx="8" cy="8" r="8" />
    </svg>
  )
}
