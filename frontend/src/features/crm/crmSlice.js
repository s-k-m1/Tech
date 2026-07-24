import { createSlice } from '@reduxjs/toolkit'

const crmSlice = createSlice({
  name: 'crm',
  initialState: {
    leads: [],
    clients: [],
    contracts: [],
    meetings: [],
    loading: false,
    error: null,
  },
  reducers: {
    setLeads: (state, action) => {
      state.leads = action.payload
    },
    setClients: (state, action) => {
      state.clients = action.payload
    },
    setContracts: (state, action) => {
      state.contracts = action.payload
    },
    setMeetings: (state, action) => {
      state.meetings = action.payload
    },
    setLoading: (state, action) => {
      state.loading = action.payload
    },
    setError: (state, action) => {
      state.error = action.payload
    },
  },
})

export const { setLeads, setClients, setContracts, setMeetings, setLoading, setError } = crmSlice.actions
export default crmSlice.reducer
