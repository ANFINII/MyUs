interface Props {
  content: string
}

export default function FormatHtml(props: Props): React.JSX.Element {
  const { content } = props
  return <div dangerouslySetInnerHTML={{ __html: content }} />
}
