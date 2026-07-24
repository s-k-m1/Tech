import { createSlice } from '@reduxjs/toolkit'

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState: {
    stats: {},
    charts: {},
    loading: false,
    error: null,
  },
  reducers: {
    setStats: (state, action) => { state.stats = action.payload },
    setCharts: (state, action) => { state.charts = action.payload },
    setLoading: (state, action) => { state.loading = action.payload },
  },
})

export const { setStats, setCharts, setLoading } = dashboardSlice.actions
export default dashboardSlice.reducer
