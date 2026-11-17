import { useState } from 'react'

interface DragItem {
  draggable: boolean
  onDragStart: () => void
  onDragOver: (e: React.DragEvent) => void
  onDragLeave: (e: React.DragEvent) => void
  onDrop: () => void
  onDragEnd: () => void
}

interface OutProps {
  dragIndex: number | null
  dragOverIndex: number | null
  dragItem: (index: number) => DragItem
}

export function useDragSort<T>(items: T[], onSort: (items: T[]) => void): OutProps {
  const [dragIndex, setDragIndex] = useState<number | null>(null)
  const [dragOverIndex, setDragOverIndex] = useState<number | null>(null)

  const handleDrag = (e: React.DragEvent, index: number | null) => {
    e.preventDefault()
    setDragOverIndex(index)
  }

  const handleDrop = (index: number) => {
    if (dragIndex === null || dragIndex === index) return
    const newItems = [...items]
    const removed = newItems.splice(dragIndex, 1)
    if (removed[0] === undefined) return
    newItems.splice(index, 0, removed[0])
    onSort(newItems)
  }

  const handleDragEnd = () => {
    setDragIndex(null)
    setDragOverIndex(null)
  }

  const dragItem = (index: number): DragItem => ({
    draggable: true,
    onDragStart: () => setDragIndex(index),
    onDragOver: (e) => handleDrag(e, index),
    onDragLeave: (e) => handleDrag(e, null),
    onDrop: () => handleDrop(index),
    onDragEnd: handleDragEnd,
  })

  return { dragIndex, dragOverIndex, dragItem }
}
