import { sanitizeHtml } from 'utils/functions/sanitize'

interface Props {
  content: string
  isSponsored?: boolean
}

export default function FormatHtml(props: Props): React.JSX.Element {
  const { content, isSponsored } = props
  return <div dangerouslySetInnerHTML={{ __html: sanitizeHtml(content, isSponsored) }} />
}
