import { useEffect, useState, useCallback } from 'react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { erpService } from '../../services/api'

export default function ProductsList() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    try {
      const res = await erpService.getProducts()
      setProducts(res.data.results || res.data)
    } catch { /* silent */ }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { load() }, [load])

  const columns = [
    { header: 'Name', accessor: 'name' },
    { header: 'SKU', accessor: 'sku' },
    { header: 'Type', accessor: 'product_type', render: (v) => <StatusBadge status={v?.replace('_', ' ')} /> },
    { header: 'Unit', accessor: 'unit' },
    { header: 'Purchase Price', accessor: 'purchase_price', render: (v) => `$${v}` },
    { header: 'Selling Price', accessor: 'selling_price', render: (v) => `$${v}` },
  ]

  if (loading) return <div className="text-center py-12 text-gray-500">Loading...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Products</h1>
      <DataTable columns={columns} data={products} />
    </div>
  )
}
