import clsx from 'clsx'

interface Props {
  size?: string
  width?: string
  height?: string
  className?: string
}

export default function IconList(props: Props) {
  const { size = '', width = '', height = '', className = '' } = props

  return (
    <svg xmlns="http://www.w3.org/2000/svg" width={size || width} height={size || height} fill="currentColor" className={clsx('bi bi-list', className)} viewBox="0 0 16 16">
      <path d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5z" />
    </svg>
  )
}
