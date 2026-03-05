import style from './Tabs.module.scss'

export interface TabItem<T extends string> {
  key: T
  label: string
}

interface Props<T extends string> {
  items: TabItem<T>[]
  selected: T
  onSelect: (key: T) => void
}

export default function Tabs<T extends string>(props: Props<T>): React.JSX.Element {
  const { items, selected, onSelect } = props

  return (
    <div className={style.tabs}>
      {items.map((item) => (
        <a key={item.key} className={selected === item.key ? style.active : ''} onClick={() => onSelect(item.key)}>
          {item.label}
        </a>
      ))}
    </div>
  )
}
