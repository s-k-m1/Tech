import { Routes, Route, Navigate, NavLink } from 'react-router-dom'

const tabs = [
  { name: 'Profile', path: '/settings/profile' },
  { name: 'Security', path: '/settings/security' },
  { name: 'Branches', path: '/settings/branches' },
  { name: 'Roles', path: '/settings/roles' },
]

export default function SettingsPage() {
  return (
    <div>
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex gap-6">
          {tabs.map((tab) => (
            <NavLink
              key={tab.path}
              to={tab.path}
              className={({ isActive }) =>
                `pb-3 text-sm font-medium border-b-2 transition-colors ${
                  isActive ? 'border-primary-600 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700'
                }`
              }
            >
              {tab.name}
            </NavLink>
          ))}
        </nav>
      </div>
      <Routes>
        <Route index element={<Navigate to="profile" />} />
        <Route path="profile" element={<div className="bg-white rounded-lg border p-6 max-w-lg"><h2 className="text-lg font-semibold mb-4">Profile Settings</h2><p className="text-gray-500">Coming soon</p></div>} />
        <Route path="security" element={<div className="bg-white rounded-lg border p-6 max-w-lg"><h2 className="text-lg font-semibold mb-4">Security Settings</h2><p className="text-gray-500">2FA, sessions, and device management coming soon</p></div>} />
        <Route path="branches" element={<div className="bg-white rounded-lg border p-6 max-w-lg"><h2 className="text-lg font-semibold mb-4">Branch Management</h2><p className="text-gray-500">Coming soon</p></div>} />
        <Route path="roles" element={<div className="bg-white rounded-lg border p-6 max-w-lg"><h2 className="text-lg font-semibold mb-4">Roles & Permissions</h2><p className="text-gray-500">Coming soon</p></div>} />
      </Routes>
    </div>
  )
}
