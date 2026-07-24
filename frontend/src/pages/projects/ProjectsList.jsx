import { useEffect, useState } from 'react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { projectService } from '../../services/api'

export default function ProjectsList() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    const load = async () => {
      try {
        const res = await projectService.getProjects()
        if (!cancelled) setProjects(res.data.results || res.data)
      } catch {
        if (!cancelled) setProjects([])
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  const columns = [
    { header: 'Name', accessor: 'name' },
    { header: 'Status', accessor: 'status', render: (v) => <StatusBadge status={v} /> },
    { header: 'Start Date', accessor: 'start_date', render: (v) => v ? new Date(v).toLocaleDateString() : '-' },
    { header: 'Due Date', accessor: 'due_date', render: (v) => v ? new Date(v).toLocaleDateString() : '-' },
    { header: 'Progress', accessor: 'progress' },
  ]

  if (loading) {
    return <div className="text-center py-12 text-gray-500">Loading projects...</div>
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Projects</h1>
      <DataTable columns={columns} data={projects} />
    </div>
  )
}
