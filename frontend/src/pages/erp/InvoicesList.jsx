import { useEffect, useState, useCallback } from 'react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { erpService } from '../../services/api'

function fmtDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString()
}

function fmtCurrency(v) {
  if (v == null) return ''
  return `$${Number(v).toFixed(2)}`
}

export default function InvoicesList() {
  const [invoices, setInvoices] = useState([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    try {
      const res = await erpService.getInvoices()
      setInvoices(res.data.results || res.data)
    } catch { /* silent */ }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { load() }, [load])

  const columns = [
    { header: 'Invoice #', accessor: 'invoice_number' },
    { header: 'Supplier', accessor: 'supplier_name' },
    { header: 'Date', render: (_, row) => fmtDate(row.created_at) },
    { header: 'Amount', render: (_, row) => fmtCurrency(row.amount) },
    { header: 'Due Date', render: (_, row) => fmtDate(row.due_date) },
    { header: 'Status', render: (_, row) => <StatusBadge status={row.status} /> },
  ]

  if (loading) return <div className="text-center py-12 text-gray-500">Loading...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Invoices</h1>
      <DataTable columns={columns} data={invoices} />
    </div>
  )
}
