import Button from 'components/parts/Button'
import style from 'components/parts/Button/Header.module.css'

interface Color {

}

interface Props extends Color {

}

export default function ButtonHeader(props: Props) {

  return (
    <>
      <Button type={type} value={value} onClick={onClick}></Button>
    </>
  )
 }
