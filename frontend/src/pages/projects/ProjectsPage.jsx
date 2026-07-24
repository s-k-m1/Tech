import { Routes, Route, Navigate, NavLink } from 'react-router-dom'
import KanbanBoard from './KanbanBoard'
import ProjectsList from './ProjectsList'
import MilestonesList from './MilestonesList'
import SprintsList from './SprintsList'

const tabs = [
  { name: 'Projects', path: '/projects/projects' },
  { name: 'Kanban', path: '/projects/kanban' },
  { name: 'Milestones', path: '/projects/milestones' },
  { name: 'Sprints', path: '/projects/sprints' },
]

export default function ProjectsPage() {
  return (
    <div>
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex gap-6">
          {tabs.map((tab) => (
            <NavLink
              key={tab.path}
              to={tab.path}
              className={({ isActive }) =>
                `pb-3 text-sm font-medium border-b-2 transition-colors ${
                  isActive ? 'border-primary-600 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700'
                }`
              }
            >
              {tab.name}
            </NavLink>
          ))}
        </nav>
      </div>
      <Routes>
        <Route index element={<Navigate to="projects" />} />
        <Route path="projects" element={<ProjectsList />} />
        <Route path="kanban" element={<KanbanBoard />} />
        <Route path="milestones" element={<MilestonesList />} />
        <Route path="sprints" element={<SprintsList />} />
        <Route path="*" element={<Navigate to="projects" />} />
      </Routes>
    </div>
  )
}
