type ArrowType = 'left' | 'right'

interface Props {
  width: string
  height: string
  type: ArrowType
  className?: string
}

export default function IconChevront(props: Props): JSX.Element {
  const { width, height, type, className = '' } = props

  return (
    <>
      {type === 'left' && (
        <svg xmlns="http://www.w3.org/2000/svg"fill="currentColor" viewBox="0 0 16 16" width={width} height={height} className={className}>
          <path fillRule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z" />
        </svg>
      )}
      {type === 'right' && (
        <svg xmlns="http://www.w3.org/2000/svg"fill="currentColor" viewBox="0 0 16 16" width={width} height={height} className={className} >
          <path fillRule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z" />
        </svg>
      )}
    </>
  )
}
