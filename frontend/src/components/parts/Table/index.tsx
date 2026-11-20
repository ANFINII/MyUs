import style from './Table.module.scss'

interface Props {
  children: React.ReactNode
}

export default function Table(props: Props): React.JSX.Element {
  const { children } = props

  return (
    <div className={style.table}>
      <table>
        <tbody>{children}</tbody>
      </table>
    </div>
  )
}
