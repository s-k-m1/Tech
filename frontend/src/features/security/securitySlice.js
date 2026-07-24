import { createSlice } from '@reduxjs/toolkit'

const securitySlice = createSlice({
  name: 'security',
  initialState: {
    events: [],
    dashboard: null,
    loading: false,
    error: null,
  },
  reducers: {
    setEvents: (state, action) => { state.events = action.payload },
    setDashboard: (state, action) => { state.dashboard = action.payload },
    setLoading: (state, action) => { state.loading = action.payload },
    setError: (state, action) => { state.error = action.payload },
  },
})

export const { setEvents, setDashboard, setLoading, setError } = securitySlice.actions
export default securitySlice.reducer
