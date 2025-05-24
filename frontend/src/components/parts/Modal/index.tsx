import clsx from 'clsx'
import Button from 'components/parts/Button'
import IconCross from 'components/parts/Icon/Cross'
import style from './Modal.module.scss'

export interface Action {
  name: string
  color?: 'blue' | 'white' | 'red'
  loading?: boolean
  disabled?: boolean
  onClick: () => void
}

export interface Props {
  open: boolean
  onClose: () => void
  title: string
  actions?: Action[]
  size?: 's' | 'm' | 'l'
  className?: string
  children: React.ReactNode
}

export default function Modal(props: Props): JSX.Element {
  const { open, onClose, title, children, actions, size = 'm', className } = props

  if (!open) return <></>

  return (
    <div className={clsx(style.modal, className)} aria-modal="true">
      <div className={clsx(style.container, style[size])}>
        <header className={style.header}>
          <h2 className={style.title}>{title}</h2>
          <button className={style.close} onClick={onClose}>
            <IconCross size="25" />
          </button>
        </header>
        <div className={style.content}>{children}</div>
        {actions &&
          <footer className={style.footer}>
            {actions.reverse().map((action, index) => <Button key={index} {...action} />)}
          </footer>
        }
      </div>
    </div>
  )
}
