import { useEffect, useState, useCallback } from 'react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { hrmService } from '../../services/api'

export default function AttendanceList() {
  const [attendance, setAttendance] = useState([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    try {
      const res = await hrmService.getAttendance()
      setAttendance(res.data.results || res.data)
    } catch { /* silent */ } finally { setLoading(false) }
  }, [])

  useEffect(() => { load() }, [load])

  const columns = [
    { header: 'Employee', accessor: 'employee_name' },
    { header: 'Date', accessor: 'scheduled_at', render: (v) => v ? new Date(v).toLocaleDateString() : '-' },
    { header: 'Status', accessor: 'status', render: (v) => <StatusBadge status={v} /> },
    { header: 'Check In', accessor: 'check_in' },
    { header: 'Check Out', accessor: 'check_out' },
  ]

  if (loading) return <div className="text-center py-8 text-gray-500">Loading...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Attendance</h1>
      <DataTable columns={columns} data={attendance} />
    </div>
  )
}