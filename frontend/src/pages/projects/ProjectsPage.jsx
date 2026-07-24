import { Routes, Route, Navigate } from 'react-router-dom'
import KanbanBoard from './KanbanBoard'

export default function ProjectsPage() {
  return (
    <Routes>
      <Route index element={<Navigate to="kanban" />} />
      <Route path="kanban" element={<KanbanBoard />} />
      <Route path="*" element={<Navigate to="kanban" />} />
    </Routes>
  )
}
