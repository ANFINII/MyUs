import { useCallback, useState } from 'react'
import cx from 'utils/functions/cx'
import Link from 'components/parts/Link'
import style from './Title.module.scss'

interface Props {
  href: string
  title: string
}

export default function MiniPlayerTitle(props: Props): React.JSX.Element {
  const { href, title } = props

  const [isFlow, setIsFlow] = useState<boolean>(false)

  const handleTitle = useCallback((el: HTMLDivElement | null) => {
    if (el) setIsFlow(el.scrollWidth > el.clientWidth)
  }, [])

  return (
    <div ref={handleTitle} className={cx(style.title, isFlow && style.flow)}>
      <Link href={href} className={style.link}>
        <span>{title}</span>
        {isFlow && (
          <span aria-hidden="true" className={style.copy}>
            {title}
          </span>
        )}
      </Link>
    </div>
  )
}
