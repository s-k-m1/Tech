import { useEffect, useCallback } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import DataTable from '../../components/ui/DataTable'
import { setClients } from '../../features/crm/crmSlice'
import { crmService } from '../../services/api'

export default function ClientsList() {
  const dispatch = useDispatch()
  const { clients } = useSelector((state) => state.crm)

  const load = useCallback(async () => {
    try {
      const res = await crmService.getClients()
      dispatch(setClients(res.data.results || res.data))
    } catch { /* silent */ }
  }, [dispatch])

  useEffect(() => { load() }, [load])

  const columns = [
    { header: 'Company', accessor: 'company_name' },
    { header: 'Contact', accessor: 'contact_person' },
    { header: 'Email', accessor: 'email' },
    { header: 'Phone', accessor: 'phone' },
    { header: 'Industry', accessor: 'industry' },
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Clients</h1>
      <DataTable columns={columns} data={clients} />
    </div>
  )
}
