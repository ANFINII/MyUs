import { useCallback, useEffect, useRef } from 'react'
import Link from '@tiptap/extension-link'
import Underline from '@tiptap/extension-underline'
import { EditorContent, useEditor } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import clsx from 'clsx'
import IconCaret from 'components/parts/Icon/Caret'
import Toolbar, { ToolbarConfig } from 'components/widgets/TextEditor/Toolbar'
import style from './ChatEditor.module.scss'

const extensions = [StarterKit.configure({ heading: false }), Link.configure({ openOnClick: false }), Underline]

const toolbarConfig: ToolbarConfig = {
  heading: false,
  align: false,
  underline: false,
  color: false,
  superscript: false,
  subscript: false,
  image: false,
}

interface Props {
  value: string
  disabled?: boolean
  onChange?: (html: string) => void
}

export default function ChatEditor(props: Props): React.JSX.Element {
  const { value, disabled = false, onChange } = props

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
    content: value || '',
    immediatelyRender: false,
    editable: !disabled,
    onUpdate: handleUpdate,
  })

  useEffect(() => {
    if (!editor) return
    const current = editor.getHTML()
    const next = value || ''
    if (current === next) return

    suppressRef.current = true
    editor.commands.setContent(next, { emitUpdate: false })
    suppressRef.current = false
  }, [editor, value])

  useEffect(() => {
    if (!editor) return
    editor.setEditable(!disabled)
  }, [editor, disabled])

  const isEmpty = value.replace(/<[^>]*>/g, '').trim().length === 0

  return (
    <div className={clsx(style.editor, disabled && style.disabled)}>
      {editor && (
        <>
          <Toolbar editor={editor} toolbarConfig={toolbarConfig} />
          <EditorContent editor={editor} />
        </>
      )}
      <div className={style.actions}>
        <button type="submit" className={style.send_button} disabled={disabled || isEmpty}>
          <IconCaret size="16" type="right" />
        </button>
      </div>
    </div>
  )
}
