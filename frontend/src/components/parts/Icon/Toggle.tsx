type ToggleType = 'on' | 'off'

interface Props {
  size: string
  type: ToggleType
}

export default function IconToggle(props: Props) {
  const { size, type } = props

  return (
    <>
      {type === 'on' ? (
        <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" className="bi-toggle-on" viewBox="0 0 16 16">
          <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
        </svg>
      ) : (
        type === 'off' && (
          <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" className="bi-toggle-off" viewBox="0 0 16 16">
            <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z" />
          </svg>
        )
      )}
    </>
  )
}
