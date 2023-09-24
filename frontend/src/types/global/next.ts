export type GetStaticPathsType = {
  paths: { params: { id: string } }[]
  fallback: boolean | 'blocking'
}
