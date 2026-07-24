import { useEffect, useState } from 'react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { projectService } from '../../services/api'

export default function MilestonesList() {
  const [milestones, setMilestones] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    const load = async () => {
      try {
        const res = await projectService.getMilestones()
        if (!cancelled) setMilestones(res.data.results || res.data)
      } catch {
        if (!cancelled) setMilestones([])
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  const columns = [
    { header: 'Title', accessor: 'title' },
    { header: 'Project', accessor: 'project_name' },
    { header: 'Due Date', accessor: 'due_date', render: (v) => v ? new Date(v).toLocaleDateString() : '-' },
    { header: 'Status', accessor: 'status', render: (v) => <StatusBadge status={v} /> },
  ]

  if (loading) {
    return <div className="text-center py-12 text-gray-500">Loading milestones...</div>
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Milestones</h1>
      <DataTable columns={columns} data={milestones} />
    </div>
  )
}
