import { useEffect, useState, useCallback } from 'react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { accountingService } from '../../services/api'

export default function BudgetsList() {
  const [budgets, setBudgets] = useState([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    try {
      const res = await accountingService.getBudgets()
      setBudgets(res.data.results || res.data)
    } catch { /* silent */ }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { load() }, [load])

  const columns = [
    { header: 'Name', accessor: 'name' },
    { header: 'Period', accessor: 'period' },
    { header: 'Amount', accessor: 'amount', render: (v) => `$${parseFloat(v || 0).toLocaleString()}` },
    { header: 'Spent', accessor: 'spent', render: (v) => `$${parseFloat(v || 0).toLocaleString()}` },
    { header: 'Remaining', accessor: 'remaining', render: (v, row) => {
      const remaining = parseFloat(row.amount || 0) - parseFloat(row.spent || 0)
      const cls = remaining < 0 ? 'text-red-600 font-medium' : 'text-green-600 font-medium'
      return <span className={cls}>${remaining.toLocaleString()}</span>
    }},
    { header: 'Status', accessor: 'status', render: (v) => <StatusBadge status={v} /> },
  ]

  if (loading) return <div className="text-center py-12 text-gray-500">Loading...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Budgets</h1>
      <DataTable columns={columns} data={budgets} />
    </div>
  )
}