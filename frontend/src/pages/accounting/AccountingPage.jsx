import { Routes, Route, Navigate, NavLink } from 'react-router-dom'
import AccountsList from './AccountsList'
import TransactionsList from './TransactionsList'
import BudgetsList from './BudgetsList'
import AccountTypesList from './AccountTypesList'
import JournalEntriesList from './JournalEntriesList'

const tabs = [
  { name: 'Accounts', path: '/accounting/accounts' },
  { name: 'Transactions', path: '/accounting/transactions' },
  { name: 'Budgets', path: '/accounting/budgets' },
  { name: 'Account Types', path: '/accounting/account-types' },
  { name: 'Journal Entries', path: '/accounting/journal-entries' },
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
        <Route path="transactions" element={<TransactionsList />} />
        <Route path="budgets" element={<BudgetsList />} />
        <Route path="account-types" element={<AccountTypesList />} />
        <Route path="journal-entries" element={<JournalEntriesList />} />
      </Routes>
    </div>
  )
}