interface Props {
  content: string
}

export default function FormatHtml(props: Props) {
  const { content } = props
  return <div dangerouslySetInnerHTML={{ __html: content }} />
}
