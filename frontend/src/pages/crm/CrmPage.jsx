import { Routes, Route, Navigate, NavLink } from 'react-router-dom'
import LeadsList from './LeadsList'
import ClientsList from './ClientsList'
import ContractsList from './ContractsList'
import MeetingsList from './MeetingsList'

const tabs = [
  { name: 'Leads', path: '/crm/leads' },
  { name: 'Clients', path: '/crm/clients' },
  { name: 'Contracts', path: '/crm/contracts' },
  { name: 'Meetings', path: '/crm/meetings' },
]

export default function CrmPage() {
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
        <Route index element={<Navigate to="leads" />} />
        <Route path="leads" element={<LeadsList />} />
        <Route path="clients" element={<ClientsList />} />
        <Route path="contracts" element={<ContractsList />} />
        <Route path="meetings" element={<MeetingsList />} />
      </Routes>
    </div>
  )
}
