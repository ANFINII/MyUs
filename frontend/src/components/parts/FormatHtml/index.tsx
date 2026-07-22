import { sanitizeHtml } from 'utils/functions/sanitize'

interface Props {
  content: string
}

export default function FormatHtml(props: Props): React.JSX.Element {
  const { content } = props
  return <div dangerouslySetInnerHTML={{ __html: sanitizeHtml(content) }} />
}
