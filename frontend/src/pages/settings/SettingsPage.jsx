export default function SettingsPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Settings</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {['Profile', 'Security', 'Notifications', 'Branches', 'Roles & Permissions'].map((item) => (
          <div key={item} className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer">
            <h3 className="font-semibold text-gray-800">{item}</h3>
            <p className="text-sm text-gray-500 mt-1">Manage {item.toLowerCase()}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
