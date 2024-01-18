import style from 'components/widgets/Table/Table.module.scss'

interface Props {
  children: React.ReactNode
}

export default function Table(props: Props) {
  const { children } = props

  return (
    <table className={style.table}>
      <tbody>{children}</tbody>
    </table>
  )
}
