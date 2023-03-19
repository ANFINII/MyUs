interface Props {
  title?: string
  children: React.ReactNode
}

export default function Main(props: Props) {
  const {title, children} = props
  return (
    <main className='main'>
      <h1 className='main_title'>{title}</h1>
      {children}
    </main>
  )
}
