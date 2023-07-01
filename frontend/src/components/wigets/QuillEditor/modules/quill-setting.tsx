import ReactQuill from 'react-quill'
import dynamic from 'next/dynamic'

export interface mentionUser {
  id: number
  value: string
  avatar: string
}

export interface RenderListFunction {
  (mentions: mentionUser[]): void
}

interface modules {
  magicUrl: boolean
  blotFormatter: object
  mention: {
    allowedChars: RegExp
    mentionDenotationChars: string[]
    source: (search: string, renderList: RenderListFunction) => Promise<void>
    renderItem: (item: mentionUser) => string
  }
  toolbar: {
    container: never[]
  }
}

interface ForwardRefProps {
  forwardedRef: React.LegacyRef<ReactQuill>
  placeholder: string
  value: string
  modules: modules
  formats: string[]
  onChange: (value: string) => void
  onFocus: () => void
  onBlur: () => void
}

const QuillEditor = dynamic(
  async () => {
    await import('quill-mention')

    const { default: RQ } = await import('react-quill')
    const { default: QU } = await import('./grispi.attachmentUploader.js')
    const { default: BF } = await import('quill-blot-formatter')
    const { default: MagicUrl } = await import('quill-magic-url')
    const { default: LoadingImage } = await import('./loadingImage.js')

    RQ.Quill.register('modules/imageUploader', QU)
    RQ.Quill.register('modules/blotFormatter', BF)
    RQ.Quill.register('modules/magicUrl', MagicUrl)
    RQ.Quill.register({ 'formats/imageBlot': LoadingImage })

    return function forwardRef({ forwardedRef, ...props }: ForwardRefProps): JSX.Element {
      return <RQ ref={forwardedRef} {...props} />
    }
  },
  { ssr: false },
)
export default QuillEditor
