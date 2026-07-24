import { useEffect, useState, useCallback } from 'react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { hrmService } from '../../services/api'

const fmt = (v) => v != null ? `$${Number(v).toFixed(2)}` : '-'

export default function PayrollList() {
  const [payroll, setPayroll] = useState([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    try {
      const res = await hrmService.getPayroll()
      setPayroll(res.data.results || res.data)
    } catch { /* silent */ } finally { setLoading(false) }
  }, [])

  useEffect(() => { load() }, [load])

  const columns = [
    { header: 'Employee', accessor: 'employee_name' },
    { header: 'Period', accessor: 'period' },
    { header: 'Gross Pay', accessor: 'gross_pay', render: (v) => fmt(v) },
    { header: 'Deductions', accessor: 'deductions', render: (v) => fmt(v) },
    { header: 'Net Pay', accessor: 'net_pay', render: (v) => fmt(v) },
    { header: 'Status', accessor: 'status', render: (v) => <StatusBadge status={v} /> },
  ]

  if (loading) return <div className="text-center py-8 text-gray-500">Loading...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Payroll</h1>
      <DataTable columns={columns} data={payroll} />
    </div>
  )
}