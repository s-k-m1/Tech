import { useEffect, useState, useCallback } from 'react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { erpService } from '../../services/api'

export default function WarehousesList() {
  const [warehouses, setWarehouses] = useState([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    try {
      const res = await erpService.getWarehouses()
      setWarehouses(res.data.results || res.data)
    } catch { /* silent */ }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { load() }, [load])

  const columns = [
    { header: 'Name', accessor: 'name' },
    { header: 'Code', accessor: 'code' },
    { header: 'Address', render: (_, row) => row.address?.length > 50 ? row.address.slice(0, 50) + '...' : row.address },
    { header: 'Manager', accessor: 'manager_name' },
    { header: 'Status', render: (_, row) => <StatusBadge status={row.status} /> },
  ]

  if (loading) return <div className="text-center py-12 text-gray-500">Loading...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Warehouses</h1>
      <DataTable columns={columns} data={warehouses} />
    </div>
  )
}
