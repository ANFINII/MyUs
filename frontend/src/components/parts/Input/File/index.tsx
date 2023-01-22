import {useState} from 'react'
import style from 'components/parts/Input/File/File.module.css'
import Input from 'components/parts/Input'

interface Props {
  checked?: boolean
  name?: string
  id?: string
  className?: string
  children: React.ReactNode
}

export default function CheckBox(props: Props) {
  const {checked, name, id, className, children} = props
  const [checkValue, setCheckValue] = useState(checked)
  const handleChange = () => {setCheckValue(false)}

  return (
    <>
      <Input type="file" name="music" accept="audio/*" id="custom_file_1" className={style.none} required />
      <Input type="text" id="file_1" placeholder="ファイル選択..." onClick={handleChange} />
    </>
  )
}
