import { useRef, useState } from 'react'
import { Editor } from '@tiptap/react'
import clsx from 'clsx'
import { Option } from 'types/internal/other'
import Select from 'components/parts/Select'
import IconBlockquote from './Icon/Blockquote'
import IconBold from './Icon/Bold'
import IconBulletList from './Icon/BulletList'
import IconCodeBlock from './Icon/CodeBlock'
import IconColor from './Icon/Color'
import IconImage from './Icon/Image'
import IconItalic from './Icon/Italic'
import IconLink from './Icon/Link'
import IconOrderedList from './Icon/OrderedList'
import IconStrike from './Icon/Strike'
import IconSubscript from './Icon/Subscript'
import IconSuperscript from './Icon/Superscript'
import IconUnderline from './Icon/Underline'
import LinkInput from './LinkInput'
import style from './TextEditor.module.scss'

interface Props {
  editor: Editor
}

export default function Toolbar(props: Props): React.JSX.Element {
  const { editor } = props

  const [heading, setHeading] = useState('0')
  const [align, setAlign] = useState('left')
  const [color, setColor] = useState('rgb(0, 0, 0)')
  const [isLinkInput, setIsLinkInput] = useState(false)
  const fileRef = useRef<HTMLInputElement>(null)

  const headingOptions: Option[] = [
    { label: 'Normal', value: '0' },
    { label: 'Heading 1', value: '1' },
    { label: 'Heading 2', value: '2' },
    { label: 'Heading 3', value: '3' },
    { label: 'Heading 4', value: '4' },
    { label: 'Heading 5', value: '5' },
  ]

  const alignOptions: Option[] = [
    { label: 'Left', value: 'left' },
    { label: 'Center', value: 'center' },
    { label: 'Right', value: 'right' },
    { label: 'Justify', value: 'justify' },
  ]

  const btnClass = (isActive: boolean) => clsx(style.button, isActive && style.button_active)

  const handleHeading = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value
    setHeading(value)
    if (value === '0') {
      editor.chain().focus().setParagraph().run()
    } else {
      const level = Number(value) as 1 | 2 | 3 | 4 | 5
      editor.chain().focus().toggleHeading({ level }).run()
    }
  }

  const handleAlign = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value
    setAlign(value)
    editor.chain().focus().setTextAlign(value).run()
  }

  const handleColor = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setColor(value)
    editor.chain().focus().setColor(value).run()
  }

  const handleLink = () => {
    if (editor.isActive('link')) {
      editor.chain().focus().unsetLink().run()
      return
    }
    setIsLinkInput((prev) => !prev)
  }

  const handleLinkSubmit = (url: string) => {
    editor.chain().focus().setLink({ href: url }).run()
    setIsLinkInput(false)
  }

  const handleLinkCancel = () => {
    setIsLinkInput(false)
    editor.commands.focus()
  }

  const handleImageClick = () => fileRef.current?.click()

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => {
      const src = reader.result
      if (typeof src === 'string') {
        editor.chain().focus().setImage({ src }).run()
      }
    }
    reader.readAsDataURL(file)
    e.target.value = ''
  }

  return (
    <div>
      <div className={style.toolbar}>
        <div className={style.group}>
          <Select value={heading} options={headingOptions} onChange={handleHeading} className={style.select} />
        </div>

        <div className={style.group}>
          <Select value={align} options={alignOptions} onChange={handleAlign} className={style.select} />
        </div>

        <div className={style.group}>
          <button type="button" className={btnClass(editor.isActive('bold'))} title="太字" onClick={() => editor.chain().focus().toggleBold().run()}>
            <IconBold className={style.icon} />
          </button>
          <button type="button" className={btnClass(editor.isActive('italic'))} title="斜体" onClick={() => editor.chain().focus().toggleItalic().run()}>
            <IconItalic className={style.icon} />
          </button>
          <button type="button" className={btnClass(editor.isActive('underline'))} title="下線" onClick={() => editor.chain().focus().toggleUnderline().run()}>
            <IconUnderline className={style.icon} />
          </button>
          <button type="button" className={btnClass(editor.isActive('strike'))} title="取り消し線" onClick={() => editor.chain().focus().toggleStrike().run()}>
            <IconStrike className={style.icon} />
          </button>
          <label className={style.color_label} title="文字色">
            <IconColor className={style.icon} color={color} />
            <input type="color" className={style.color_input} onChange={handleColor} />
          </label>
          <button type="button" className={btnClass(editor.isActive('superscript'))} title="上付き" onClick={() => editor.chain().focus().toggleSuperscript().run()}>
            <IconSuperscript className={style.icon} />
          </button>
          <button type="button" className={btnClass(editor.isActive('subscript'))} title="下付き" onClick={() => editor.chain().focus().toggleSubscript().run()}>
            <IconSubscript className={style.icon} />
          </button>
        </div>

        <div className={style.group}>
          <button type="button" className={btnClass(editor.isActive('orderedList'))} title="番号付きリスト" onClick={() => editor.chain().focus().toggleOrderedList().run()}>
            <IconOrderedList className={style.icon} />
          </button>
          <button type="button" className={btnClass(editor.isActive('bulletList'))} title="箇条書き" onClick={() => editor.chain().focus().toggleBulletList().run()}>
            <IconBulletList className={style.icon} />
          </button>
        </div>

        <div className={style.group}>
          <button type="button" className={btnClass(editor.isActive('codeBlock'))} title="コードブロック" onClick={() => editor.chain().focus().toggleCodeBlock().run()}>
            <IconCodeBlock className={style.icon} />
          </button>
          <button type="button" className={btnClass(editor.isActive('blockquote'))} title="引用" onClick={() => editor.chain().focus().toggleBlockquote().run()}>
            <IconBlockquote className={style.icon} />
          </button>
          <button type="button" className={btnClass(editor.isActive('link') || isLinkInput)} title="リンク" onClick={handleLink}>
            <IconLink className={style.icon_link} />
          </button>
          <button type="button" className={style.button} title="画像" onClick={handleImageClick}>
            <IconImage className={style.icon_wide} />
          </button>
          <input ref={fileRef} type="file" accept="image/*" className={style.file_hidden} onChange={handleFile} />
        </div>
      </div>

      {isLinkInput && <LinkInput onSubmit={handleLinkSubmit} onCancel={handleLinkCancel} />}
    </div>
  )
}
