import { useEffect, useState, useCallback } from 'react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { accountingService } from '../../services/api'

export default function AccountsList() {
  const [accounts, setAccounts] = useState([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    try {
      const res = await accountingService.getAccounts()
      setAccounts(res.data.results || res.data)
    } catch { /* silent */ }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { load() }, [load])

  const columns = [
    { header: 'Code', accessor: 'code' },
    { header: 'Name', accessor: 'name' },
    { header: 'Type', accessor: 'account_type' },
    { header: 'Opening Balance', accessor: 'opening_balance', render: (v) => `$${parseFloat(v || 0).toLocaleString()}` },
    { header: 'Current Balance', accessor: 'current_balance', render: (v) => <span className={v < 0 ? 'text-red-600 font-medium' : 'text-green-600 font-medium'}>${parseFloat(v || 0).toLocaleString()}</span> },
  ]

  if (loading) return <div className="text-center py-12 text-gray-500">Loading...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Chart of Accounts</h1>
      <DataTable columns={columns} data={accounts} />
    </div>
  )
}
