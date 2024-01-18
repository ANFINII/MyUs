interface Props {
  children: React.ReactNode
}

export default function Table(props: Props) {
  const { children } = props

  return (
    <table className="table">
      <tbody>{children}</tbody>
    </table>
  )
}
