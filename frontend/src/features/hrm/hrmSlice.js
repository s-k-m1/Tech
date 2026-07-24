import { createSlice } from '@reduxjs/toolkit'

const hrmSlice = createSlice({
  name: 'hrm',
  initialState: {
    employees: [],
    attendance: [],
    leaves: [],
    payroll: [],
    loading: false,
    error: null,
  },
  reducers: {
    setEmployees: (state, action) => { state.employees = action.payload },
    setAttendance: (state, action) => { state.attendance = action.payload },
    setLeaves: (state, action) => { state.leaves = action.payload },
    setPayroll: (state, action) => { state.payroll = action.payload },
    setLoading: (state, action) => { state.loading = action.payload },
    setError: (state, action) => { state.error = action.payload },
  },
})

export const { setEmployees, setAttendance, setLeaves, setPayroll, setLoading, setError } = hrmSlice.actions
export default hrmSlice.reducer
