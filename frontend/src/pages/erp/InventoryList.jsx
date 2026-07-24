import { useEffect, useState, useCallback } from 'react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { erpService } from '../../services/api'

export default function InventoryList() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    try {
      const res = await erpService.getInventory()
      setItems(res.data.results || res.data)
    } catch { /* silent */ }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { load() }, [load])

  const columns = [
    { header: 'Product', accessor: 'product_name' },
    { header: 'SKU', accessor: 'sku' },
    { header: 'Warehouse', accessor: 'warehouse_name' },
    { header: 'Quantity', accessor: 'quantity' },
    { header: 'Min Stock', accessor: 'min_stock' },
    { header: 'Status', render: (_, row) => <StatusBadge status={row.status} /> },
  ]

  if (loading) return <div className="text-center py-12 text-gray-500">Loading...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Inventory</h1>
      <DataTable columns={columns} data={items} />
    </div>
  )
}
