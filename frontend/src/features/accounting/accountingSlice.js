import { createSlice } from '@reduxjs/toolkit'

const accountingSlice = createSlice({
  name: 'accounting',
  initialState: {
    transactions: [],
    accounts: [],
    ledgers: [],
    loading: false,
    error: null,
  },
  reducers: {
    setTransactions: (state, action) => { state.transactions = action.payload },
    setAccounts: (state, action) => { state.accounts = action.payload },
    setLedgers: (state, action) => { state.ledgers = action.payload },
    setLoading: (state, action) => { state.loading = action.payload },
  },
})

export const { setTransactions, setAccounts, setLedgers, setLoading } = accountingSlice.actions
export default accountingSlice.reducer
