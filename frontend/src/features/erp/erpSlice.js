import { createSlice } from '@reduxjs/toolkit'

const erpSlice = createSlice({
  name: 'erp',
  initialState: {
    inventory: [],
    purchases: [],
    invoices: [],
    loading: false,
    error: null,
  },
  reducers: {
    setInventory: (state, action) => { state.inventory = action.payload },
    setPurchases: (state, action) => { state.purchases = action.payload },
    setInvoices: (state, action) => { state.invoices = action.payload },
    setLoading: (state, action) => { state.loading = action.payload },
  },
})

export const { setInventory, setPurchases, setInvoices, setLoading } = erpSlice.actions
export default erpSlice.reducer
