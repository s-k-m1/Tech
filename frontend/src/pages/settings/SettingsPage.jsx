import { Routes, Route, Navigate, NavLink } from 'react-router-dom'
import ProfilePage from './ProfilePage'
import SecurityPage from './SecurityPage'
import BranchesPage from './BranchesPage'
import RolesPage from './RolesPage'

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
        <Route path="profile" element={<ProfilePage />} />
        <Route path="security" element={<SecurityPage />} />
        <Route path="branches" element={<BranchesPage />} />
        <Route path="roles" element={<RolesPage />} />
      </Routes>
    </div>
  )
}
