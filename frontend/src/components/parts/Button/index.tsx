import style from 'components/parts/Button/Button.module.css'

interface Color {
  blue?: boolean
  purple?: boolean
  red?: boolean
  green?: boolean
  light?: boolean
}

interface Props extends Color {
  children?: string | string[]
  className?: string
  value?: string
  size?: 'xl' | 'xs'
  type?: 'submit' | 'reset' | 'button'
  onClick?(): void
}

export default function Button(props: Props) {
  const {blue, purple, red, green, light} = props
  const {children, className, type, value, size, onClick} = props

  return (
    <>
      {blue ?
        <button type={type} value={value} onClick={onClick}
        className={`${style.button} ${style.blue} `
          + (size === 'xl' ? `${style.xl} ` : '')
          + (size === 'xs' ? `${style.xs} ` : '')
          + (className ? className : '' )
        }
        >{children}
        </button>
      :purple ?
        <button type={type} value={value} onClick={onClick}
          className={`${style.button} ${style.purple} `
            + (size === 'xl' ? `${style.xl} ` : '')
            + (size === 'xs' ? `${style.xs} ` : '')
            + (className ? className : '' )
          }
        >{children}
        </button>
      :red ?
        <button type={type} value={value} onClick={onClick}
          className={`${style.button} ${style.red} `
            + (size === 'xl' ? `${style.xl} ` : '')
            + (size === 'xs' ? `${style.xs} ` : '')
            + (className ? className : '' )
          }
        >{children}
        </button>
      :green ?
        <button type={type} value={value} onClick={onClick}
          className={`${style.button} ${style.green} `
            + (size === 'xl' ? `${style.xl} ` : '')
            + (size === 'xs' ? `${style.xs} ` : '')
            + (className ? className : '' )
          }
        >{children}
        </button>
      :light ?
        <button type={type} value={value} onClick={onClick}
          className={`${style.button} ${style.light} `
            + (size === 'xl' ? `${style.xl} ` : '')
            + (size === 'xs' ? `${style.xs} ` : '')
            + (className ? className : '' )
          }
        >{children}
        </button>
      :
        <button type={type} value={value} onClick={onClick}
          className={`${style.button} `
            + (size === 'xl' ? `${style.xl} ` : '')
            + (size === 'xs' ? `${style.xs} ` : '')
            + (className ? className : '' )
          }
        >{children}
        </button>
      }
    </>
  )
 }
