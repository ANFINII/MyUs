import { Quill } from 'react-quill'

const InlineBlot = Quill.import('blots/block')

class LoadingImage extends InlineBlot {
  static create(src) {
    const node = super.create(src)
    if (src === true) return node

    const image = document.createElement('img')
    image.setAttribute('src', src)
    node.appendChild(image)
    return node
  }
  deleteAt(index, length) {
    super.deleteAt(index, length)
    this.cache = {}
  }
  static name(domNode) {
    const { src, custom } = domNode.dataset
    return { src, custom }
  }
}

LoadingImage.blotName = 'imageBlot'
LoadingImage.className = 'image-uploading'
LoadingImage.tagName = 'span'

export default LoadingImage
