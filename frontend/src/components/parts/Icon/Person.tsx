type PersonType = 'square' | 'circle'

interface Props {
  size: string
  type: PersonType
  className?: string
}

export default function IconPerson(props: Props) {
  const { size, type, className = '' } = props

  return (
    <>
      {type === 'square' ? (
        <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" className={'bi bi-person-square' + (className && ' ' + className)} viewBox="0 0 16 16">
          <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
          <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm12 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1v-1c0-1-1-4-6-4s-6 3-6 4v1a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12z" />
        </svg>
      ) : (
        type === 'circle' && (
          <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" className={'bi bi-person-circle' + (className && ' ' + className)} viewBox="0 0 16 16">
            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
            <path fillRule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z" />
          </svg>
        )
      )}
    </>
  )
}
