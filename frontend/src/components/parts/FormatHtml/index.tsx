interface Props {
  content: string
}

export default function FormatHtml(props: Props): JSX.Element {
  const { content } = props
  return <div dangerouslySetInnerHTML={{ __html: content }} />
}
