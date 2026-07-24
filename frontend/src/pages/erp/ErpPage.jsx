import { Routes, Route, Navigate, NavLink } from 'react-router-dom'
import ProductsList from './ProductsList'
import InventoryList from './InventoryList'
import PurchaseOrdersList from './PurchaseOrdersList'
import SuppliersList from './SuppliersList'
import WarehousesList from './WarehousesList'
import InvoicesList from './InvoicesList'

const tabs = [
  { name: 'Products', path: '/erp/products' },
  { name: 'Inventory', path: '/erp/inventory' },
  { name: 'Purchase Orders', path: '/erp/purchase-orders' },
  { name: 'Suppliers', path: '/erp/suppliers' },
  { name: 'Warehouses', path: '/erp/warehouses' },
  { name: 'Invoices', path: '/erp/invoices' },
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
        <Route path="inventory" element={<InventoryList />} />
        <Route path="purchase-orders" element={<PurchaseOrdersList />} />
        <Route path="suppliers" element={<SuppliersList />} />
        <Route path="warehouses" element={<WarehousesList />} />
        <Route path="invoices" element={<InvoicesList />} />
      </Routes>
    </div>
  )
}
