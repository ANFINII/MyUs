export const addCodeCopyButtons = (html: string, label: string): string => {
  const doc = new DOMParser().parseFromString(html, 'text/html')
  doc.body.querySelectorAll('pre').forEach((pre) => {
    const block = doc.createElement('div')
    block.setAttribute('data-code-block', '')
    const button = doc.createElement('button')
    button.type = 'button'
    button.setAttribute('data-code-copy', '')
    button.textContent = label
    pre.replaceWith(block)
    block.append(button, pre)
  })
  return doc.body.innerHTML
}
