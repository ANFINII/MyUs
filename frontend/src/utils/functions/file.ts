export const previewUrl = (file: File, prevUrl?: string): string => {
  if (prevUrl) URL.revokeObjectURL(prevUrl)
  return URL.createObjectURL(file)
}
