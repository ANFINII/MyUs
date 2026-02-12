import { useCallback, useEffect, useRef } from 'react'
import { Color } from '@tiptap/extension-color'
import Highlight from '@tiptap/extension-highlight'
import Image from '@tiptap/extension-image'
import Link from '@tiptap/extension-link'
import Subscript from '@tiptap/extension-subscript'
import Superscript from '@tiptap/extension-superscript'
import TextAlign from '@tiptap/extension-text-align'
import { TextStyle } from '@tiptap/extension-text-style'
import Underline from '@tiptap/extension-underline'
import { EditorContent, useEditor } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import clsx from 'clsx'
import VStack from 'components/parts/Stack/Vertical'
import style from './TextEditor.module.scss'
import Toolbar from './Toolbar'

const extensions = [
  StarterKit.configure({ heading: { levels: [1, 2, 3, 4, 5] } }),
  TextStyle,
  Color,
  Highlight.configure({ multicolor: true }),
  TextAlign.configure({ types: ['heading', 'paragraph'] }),
  Underline,
  Link.configure({ openOnClick: false }),
  Image,
  Subscript,
  Superscript,
]

interface Props {
  label?: string
  value?: string
  required?: boolean
  className?: string
  onChange?: (html: string) => void
}

export default function TextEditor(props: Props): React.JSX.Element {
  const { label, value, required = false, className, onChange } = props

  const onChangeRef = useRef(onChange)
  const suppressRef = useRef(false)

  useEffect(() => {
    onChangeRef.current = onChange
  }, [onChange])

  const handleUpdate = useCallback(({ editor: e }: { editor: { getHTML: () => string } }) => {
    if (suppressRef.current) return
    onChangeRef.current?.(e.getHTML())
  }, [])

  const editor = useEditor({
    extensions,
    content: value ?? '',
    immediatelyRender: false,
    onUpdate: handleUpdate,
  })

  useEffect(() => {
    if (!editor) return
    const current = editor.getHTML()
    const next = value ?? ''
    if (current === next) return

    suppressRef.current = true
    editor.commands.setContent(next, { emitUpdate: false })
    suppressRef.current = false
  }, [editor, value])

  const handleLabel = () => editor?.commands.focus()
  const isRequired = required && value === ''

  return (
    <VStack gap="2" className={className}>
      {label && (
        <label className={style.label} onClick={handleLabel}>
          {label}
        </label>
      )}
      {editor && (
        <div className={clsx(style.editor, isRequired && style.error)}>
          <Toolbar editor={editor} />
          <EditorContent editor={editor} />
        </div>
      )}
      {isRequired && <p className={style.error_text}>※必須入力です！</p>}
    </VStack>
  )
}
