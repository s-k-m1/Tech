import { useEffect, useCallback } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import Button from '../../components/ui/Button'
import { setLeaves } from '../../features/hrm/hrmSlice'
import { hrmService } from '../../services/api'

export default function LeavesList() {
  const dispatch = useDispatch()
  const { leaves } = useSelector((state) => state.hrm)

  const load = useCallback(async () => {
    try {
      const res = await hrmService.getLeaves()
      dispatch(setLeaves(res.data.results || res.data))
    } catch { /* silent */ }
  }, [dispatch])

  useEffect(() => { load() }, [load])

  const columns = [
    { header: 'Type', accessor: 'leave_type' },
    { header: 'Start', accessor: 'start_date' },
    { header: 'End', accessor: 'end_date' },
    { header: 'Reason', accessor: 'reason' },
    { header: 'Status', accessor: 'status', render: (v) => <StatusBadge status={v} /> },
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Leave Requests</h1>
      <DataTable columns={columns} data={leaves} />
    </div>
  )
}
