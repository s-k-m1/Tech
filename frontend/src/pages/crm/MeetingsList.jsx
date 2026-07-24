import { useEffect, useState, useCallback } from 'react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { crmService } from '../../services/api'

export default function MeetingsList() {
  const [meetings, setMeetings] = useState([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    try {
      const res = await crmService.getMeetings()
      setMeetings(res.data.results || res.data)
    } catch { /* silent */ }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { load() }, [load])

  const columns = [
    { header: 'Title', accessor: 'title' },
    { header: 'Date', accessor: 'scheduled_at', render: (v) => v ? new Date(v).toLocaleString() : '-' },
    { header: 'Status', accessor: 'status', render: (v) => <StatusBadge status={v} /> },
    { header: 'Notes', accessor: 'notes', render: (v) => v ? v.slice(0, 50) : '-' },
  ]

  if (loading) return <div className="text-center py-12 text-gray-500">Loading...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Meetings</h1>
      <DataTable columns={columns} data={meetings} />
    </div>
  )
}
