import clsx from 'clsx'

type CrossType = 'defalt' | 'large'

interface Props {
  size: string
  type?: CrossType
  className?: string
  onClick?: () => void
}

export default function IconCross(props: Props) {
  const { size, type = 'defalt', className = '', onClick } = props

  return (
    <>
      {type === 'defalt' ? (
        <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" className={clsx('bi bi-x', className)} onClick={onClick} viewBox="0 0 16 16">
          <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z" />
        </svg>
      ) : (
        type === 'large' && (
          <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" className={clsx('bi bi-x-lg', className)} onClick={onClick} viewBox="0 0 16 16">
            <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z" />
          </svg>
        )
      )}
    </>
  )
}
