import { useEffect, useState } from 'react'
import { useSelector } from 'react-redux'
import Card from '../../components/ui/Card'
import DataTable from '../../components/ui/DataTable'
import { authService } from '../../services/api'

export default function SecurityPage() {
  const user = useSelector((state) => state.auth.user)
  const [devices, setDevices] = useState([])

  useEffect(() => {
    authService.getDevices()
      .then((res) => setDevices(res.data.results || res.data))
      .catch(() => {})
  }, [])

  const columns = [
    { header: 'Device Name', accessor: 'device_name' },
    { header: 'Type', accessor: 'device_type' },
    {
      header: 'Last Login',
      accessor: 'last_login',
      render: (v) => v ? new Date(v).toLocaleString() : '—',
    },
    { header: 'IP Address', accessor: 'ip_address' },
  ]

  return (
    <div className="space-y-6">
      <Card>
        <h2 className="text-lg font-semibold mb-4">Two-Factor Authentication</h2>
        <div className="flex items-center gap-2">
          <span className={`inline-block w-2.5 h-2.5 rounded-full ${user?.is_2fa_enabled ? 'bg-green-500' : 'bg-gray-300'}`} />
          <span className="text-sm text-gray-700">
            {user?.is_2fa_enabled ? 'Enabled' : 'Disabled'}
          </span>
        </div>
      </Card>
      <Card>
        <h2 className="text-lg font-semibold mb-4">Devices & Sessions</h2>
        <DataTable columns={columns} data={devices} />
      </Card>
    </div>
  )
}
