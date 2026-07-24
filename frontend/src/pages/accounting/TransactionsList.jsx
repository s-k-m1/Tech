import { useEffect, useState, useCallback } from 'react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { accountingService } from '../../services/api'

export default function TransactionsList() {
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    try {
      const res = await accountingService.getTransactions()
      setTransactions(res.data.results || res.data)
    } catch { /* silent */ }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { load() }, [load])

  const columns = [
    { header: 'Date', accessor: 'created_at', render: (v) => new Date(v).toLocaleDateString() },
    { header: 'Description', accessor: 'description' },
    { header: 'Debit', accessor: 'debit', render: (v) => `$${parseFloat(v || 0).toLocaleString()}` },
    { header: 'Credit', accessor: 'credit', render: (v) => `$${parseFloat(v || 0).toLocaleString()}` },
    { header: 'Account', accessor: 'account_name' },
    { header: 'Status', accessor: 'status', render: (v) => <StatusBadge status={v} /> },
  ]

  if (loading) return <div className="text-center py-12 text-gray-500">Loading...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Transactions</h1>
      <DataTable columns={columns} data={transactions} />
    </div>
  )
}