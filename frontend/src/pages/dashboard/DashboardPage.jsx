import { useSelector } from 'react-redux'

export default function DashboardPage() {
  const user = useSelector((state) => state.auth.user)

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">
        Welcome, {user?.first_name || user?.username || 'User'}
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: 'Active Projects', value: '--', color: 'bg-blue-500' },
          { label: 'Open Tickets', value: '--', color: 'bg-yellow-500' },
          { label: 'Employees', value: '--', color: 'bg-green-500' },
          { label: 'Leads', value: '--', color: 'bg-purple-500' },
        ].map((stat) => (
          <div key={stat.label} className="bg-white rounded-lg shadow p-6">
            <div className={`h-2 w-12 rounded ${stat.color} mb-4`} />
            <p className="text-3xl font-bold text-gray-800">{stat.value}</p>
            <p className="text-sm text-gray-500 mt-1">{stat.label}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
