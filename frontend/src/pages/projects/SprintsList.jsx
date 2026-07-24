import { useEffect, useState } from 'react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { projectService } from '../../services/api'

export default function SprintsList() {
  const [sprints, setSprints] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    const load = async () => {
      try {
        const res = await projectService.getSprints()
        if (!cancelled) setSprints(res.data.results || res.data)
      } catch {
        if (!cancelled) setSprints([])
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  const columns = [
    { header: 'Name', accessor: 'name' },
    { header: 'Project', accessor: 'project_name' },
    { header: 'Start Date', accessor: 'start_date', render: (v) => v ? new Date(v).toLocaleDateString() : '-' },
    { header: 'End Date', accessor: 'end_date', render: (v) => v ? new Date(v).toLocaleDateString() : '-' },
    { header: 'Status', accessor: 'status', render: (v) => <StatusBadge status={v} /> },
  ]

  if (loading) {
    return <div className="text-center py-12 text-gray-500">Loading sprints...</div>
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Sprints</h1>
      <DataTable columns={columns} data={sprints} />
    </div>
  )
}
