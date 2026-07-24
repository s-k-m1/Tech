import { Routes, Route, Navigate, NavLink } from 'react-router-dom'
import ProductsList from './ProductsList'

const tabs = [
  { name: 'Products', path: '/erp/products' },
  { name: 'Inventory', path: '/erp/inventory' },
  { name: 'Purchase Orders', path: '/erp/purchase-orders' },
]

export default function ErpPage() {
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
        <Route index element={<Navigate to="products" />} />
        <Route path="products" element={<ProductsList />} />
        <Route path="inventory" element={<div className="text-center py-12 text-gray-500">Inventory coming soon</div>} />
        <Route path="purchase-orders" element={<div className="text-center py-12 text-gray-500">Purchase Orders coming soon</div>} />
      </Routes>
    </div>
  )
}
