import style from 'components/parts/Input/Input.module.css'

interface Props {
  id?: string
  className?: string
  name?: string
  value?: string | number
  placeholder?: string
  children?: React.ReactNode
}

export default function Select(props: Props) {
  const {id, className, name, value, children} = props

  return (
    <select name={name} id={id} className={`${style.input} ` + (className ? className : '' )}>
      <option value="">{children}</option>
      <option value={value} selected>{value}</option>
    </select>
  )
}
