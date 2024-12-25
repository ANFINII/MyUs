import clsx from 'clsx'

type CaretType = 'square' | 'right' | 'left' | 'down'

interface Props {
  size: string
  type?: CaretType
  className?: string
}

export default function IconCaret(props: Props) {
  const { size, type = 'square', className = '' } = props

  return (
    <>
      {type === 'square' ? (
        <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" className={clsx('bi bi-caret-right-square', className)} viewBox="0 0 16 16">
          <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z" />
          <path d="M5.795 12.456A.5.5 0 0 1 5.5 12V4a.5.5 0 0 1 .832-.374l4.5 4a.5.5 0 0 1 0 .748l-4.5 4a.5.5 0 0 1-.537.082z" />
        </svg>
      ) : type === 'right' ? (
        <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" className={clsx('bi bi-caret-right-fill', className)} viewBox="0 0 16 16">
          <path d="m12.14 8.753-5.482 4.796c-.646.566-1.658.106-1.658-.753V3.204a1 1 0 0 1 1.659-.753l5.48 4.796a1 1 0 0 1 0 1.506z"/>
        </svg>
      ) : (
        type === 'left' ? (
          <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" className={clsx('bi bi-caret-left-fill', className)} viewBox="0 0 16 16">
            <path d="m3.86 8.753 5.482 4.796c.646.566 1.658.106 1.658-.753V3.204a1 1 0 0 0-1.659-.753l-5.48 4.796a1 1 0 0 0 0 1.506z"/>
          </svg>
        ) : (
          type === 'down' && (
            <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" className={clsx('bi bi-caret-down-fill', className)} viewBox="0 0 16 16">
              <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
            </svg>
          )
        )
      )}
    </>
  )
}
