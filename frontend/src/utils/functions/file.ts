export const downloadFile = async (file: File, fileName: string, extension: string): Promise<void> => {
  const blob = new Blob([file])
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', `${fileName}.${extension}`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}
