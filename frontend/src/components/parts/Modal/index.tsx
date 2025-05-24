import clsx from 'clsx'
import Button from 'components/parts/Button'
import IconCross from 'components/parts/Icon/Cross'
import style from './Modal.module.scss'

export interface Action {
  label: string
  loading?: boolean
  disabled?: boolean
  variant?: 'blue' | 'white' | 'red'
  onClick: () => void
}

export interface Props {
  open: boolean
  onClose: () => void
  title: string
  buttons?: Action[]
  size?: 's' | 'm' | 'l'
  className?: string
  children: React.ReactNode
}

export default function Modal(props: Props): JSX.Element {
  const { open, onClose, title, children, buttons, size = 'm', className } = props

  if (!open) return <></>

  return (
    <div className={style.modal} aria-modal="true">
      <div className={clsx(style.container, style[size], className)}>
        <header className={style.header}>
          <h2 className={style.title}>{title}</h2>
          <button className={style.close} onClick={onClose}>
            <IconCross size="25" />
          </button>
        </header>
        <div className={style.content}>{children}</div>
        {buttons &&
          <footer className={style.footer}>
            {buttons.reverse().map(({ label, loading, disabled, variant, onClick }) => (
              <Button key={label} name={label} color={variant} loading={loading} disabled={disabled} onClick={onClick} />
            ))}
          </footer>
        }
      </div>
    </div>
  )
}
