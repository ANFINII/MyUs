import clsx from 'clsx'
type ArrowType = 'left' | 'right'

interface Props {
  width: string
  height: string
  type: ArrowType
  className?: string
}

export default function IconChevront(props: Props) {
  const { width, height, type, className = '' } = props

  return (
    <>
      {type === 'left' ? (
        <svg xmlns="http://www.w3.org/2000/svg" width={width} height={height} fill="currentColor" className={clsx('bi-chevron-left', className)} viewBox="0 0 16 16">
          <path fillRule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z" />
        </svg>
      ) : (
        type === 'right' && (
          <svg xmlns="http://www.w3.org/2000/svg" width={width} height={height} fill="currentColor" className={clsx('bi-chevron-right', className)} viewBox="0 0 16 16">
            <path fillRule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z" />
          </svg>
        )
      )}
    </>
  )
}
