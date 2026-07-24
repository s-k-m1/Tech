import { Routes, Route, Navigate, NavLink } from 'react-router-dom'
import EmployeesList from './EmployeesList'
import LeavesList from './LeavesList'
import LeaveForm from './LeaveForm'

const tabs = [
  { name: 'Employees', path: '/hrm/employees' },
  { name: 'Leaves', path: '/hrm/leaves' },
  { name: 'Apply Leave', path: '/hrm/apply-leave' },
]

export default function HrmPage() {
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
        <Route index element={<Navigate to="employees" />} />
        <Route path="employees" element={<EmployeesList />} />
        <Route path="leaves" element={<LeavesList />} />
        <Route path="apply-leave" element={<LeaveForm />} />
      </Routes>
    </div>
  )
}
