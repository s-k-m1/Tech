export default function SecurityPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Security Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: 'Security Events', value: '--', color: 'bg-red-500' },
          { label: 'Threats Blocked', value: '--', color: 'bg-orange-500' },
          { label: 'Active Sessions', value: '--', color: 'bg-green-500' },
          { label: 'Risk Score', value: '--', color: 'bg-purple-500' },
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
