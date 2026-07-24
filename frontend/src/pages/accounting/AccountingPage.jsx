import { Routes, Route, Navigate, NavLink } from 'react-router-dom'
import AccountsList from './AccountsList'

const tabs = [
  { name: 'Accounts', path: '/accounting/accounts' },
  { name: 'Transactions', path: '/accounting/transactions' },
  { name: 'Budgets', path: '/accounting/budgets' },
]

export default function AccountingPage() {
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
        <Route index element={<Navigate to="accounts" />} />
        <Route path="accounts" element={<AccountsList />} />
        <Route path="transactions" element={<div className="text-center py-12 text-gray-500">Transactions coming soon</div>} />
        <Route path="budgets" element={<div className="text-center py-12 text-gray-500">Budgets coming soon</div>} />
      </Routes>
    </div>
  )
}
