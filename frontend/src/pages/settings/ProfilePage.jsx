import { useSelector } from 'react-redux'
import Card from '../../components/ui/Card'

export default function ProfilePage() {
  const user = useSelector((state) => state.auth.user)

  const fields = [
    { label: 'Email', value: user?.email },
    { label: 'Username', value: user?.username },
    { label: 'First Name', value: user?.first_name },
    { label: 'Last Name', value: user?.last_name },
    { label: 'Phone', value: user?.phone },
    { label: 'User Type', value: user?.user_type },
  ]

  return (
    <Card>
      <h2 className="text-lg font-semibold mb-4">Profile Information</h2>
      <div className="space-y-3">
        {fields.map((f) => (
          <div key={f.label} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
            <span className="text-sm text-gray-500">{f.label}</span>
            <span className="text-sm font-medium text-gray-800">{f.value || '—'}</span>
          </div>
        ))}
      </div>
    </Card>
  )
}
