import { useCallback, useEffect, useRef } from 'react'
import Link from '@tiptap/extension-link'
import Placeholder from '@tiptap/extension-placeholder'
import Underline from '@tiptap/extension-underline'
import { EditorContent, useEditor } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import cx from 'utils/functions/cx'
import { useRecording } from 'components/hooks/useRecording'
import Button from 'components/parts/Button'
import IconMic from 'components/parts/Icon/Mic'
import HStack from 'components/parts/Stack/Horizontal'
import Toolbar, { ToolbarConfig } from 'components/widgets/TextEditor/Toolbar'
import style from './ChatEditor.module.scss'
import SendButton from '../SendButton'

const baseExtensions = [StarterKit.configure({ heading: false }), Link.configure({ openOnClick: false }), Underline]

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
  placeholder?: string
  onChange?: (html: string) => void
  onCancel?: () => void
  onSave?: () => void
}

export default function ChatEditor(props: Props): React.JSX.Element {
  const { value, disabled = false, placeholder, onChange, onCancel, onSave } = props

  const onChangeRef = useRef(onChange)
  const onSaveRef = useRef(onSave)
  const suppressRef = useRef(false)

  useEffect(() => {
    onChangeRef.current = onChange
  }, [onChange])

  useEffect(() => {
    onSaveRef.current = onSave
  }, [onSave])

  const handleKeyDown = useCallback((_view: unknown, event: KeyboardEvent) => {
    if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') {
      if (onSaveRef.current) {
        onSaveRef.current()
      } else {
        const form = (event.target as HTMLElement).closest('form')
        form?.requestSubmit()
      }
      return true
    }
    return false
  }, [])

  const handleUpdate = useCallback(({ editor: e }: { editor: { getHTML: () => string } }) => {
    if (suppressRef.current) return
    onChangeRef.current?.(e.getHTML())
  }, [])

  const extensions = [...baseExtensions, Placeholder.configure({ placeholder, showOnlyWhenEditable: false })]

  const editor = useEditor({
    extensions,
    content: value || '',
    immediatelyRender: false,
    editable: !disabled,
    editorProps: { handleKeyDown },
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

  const handleSpeechResult = useCallback(
    (transcript: string) => {
      editor?.commands.insertContent(transcript)
    },
    [editor],
  )

  const { isRecording, isSpeaking, isSupported, handleToggle } = useRecording({ onResult: handleSpeechResult })

  const isEmpty = value.replace(/<[^>]*>/g, '').trim().length === 0

  return (
    <div className={cx(style.editor, disabled && style.disabled)}>
      {editor && (
        <>
          <Toolbar editor={editor} toolbarConfig={toolbarConfig} />
          <EditorContent editor={editor} />
        </>
      )}
      <div className={style.actions}>
        {isSupported && (
          <button type="button" className={cx(style.mic_button, isRecording && style.recording, isSpeaking && style.speaking)} onClick={handleToggle}>
            <IconMic size="16" />
          </button>
        )}
        {onCancel && onSave ? (
          <HStack gap="2" className={style.edit_actions}>
            <Button name="キャンセル" color="white" size="s" onClick={onSave} />
            <Button name="保存" color="blue" size="s" onClick={onSave} disabled={isEmpty} />
          </HStack>
        ) : (
          <SendButton disabled={disabled || isEmpty} />
        )}
      </div>
    </div>
  )
}
