import { useEffect, useState, useCallback } from 'react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { crmService } from '../../services/api'

export default function ContractsList() {
  const [contracts, setContracts] = useState([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    try {
      const res = await crmService.getContracts()
      setContracts(res.data.results || res.data)
    } catch { /* silent */ }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { load() }, [load])

  const columns = [
    { header: 'Title', accessor: 'title' },
    { header: 'Client', accessor: 'client_name' },
    { header: 'Status', accessor: 'status', render: (v) => <StatusBadge status={v} /> },
    { header: 'Start Date', accessor: 'start_date', render: (v) => v ? new Date(v).toLocaleDateString() : '-' },
    { header: 'End Date', accessor: 'end_date', render: (v) => v ? new Date(v).toLocaleDateString() : '-' },
    { header: 'Value', accessor: 'value', render: (v) => v ? `$${v}` : '-' },
  ]

  if (loading) return <div className="text-center py-12 text-gray-500">Loading...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Contracts</h1>
      <DataTable columns={columns} data={contracts} />
    </div>
  )
}
