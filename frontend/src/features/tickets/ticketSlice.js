import { createSlice } from '@reduxjs/toolkit'

const ticketSlice = createSlice({
  name: 'tickets',
  initialState: {
    tickets: [],
    comments: [],
    loading: false,
    error: null,
  },
  reducers: {
    setTickets: (state, action) => { state.tickets = action.payload },
    setComments: (state, action) => { state.comments = action.payload },
    setLoading: (state, action) => { state.loading = action.payload },
    setError: (state, action) => { state.error = action.payload },
  },
})

export const { setTickets, setComments, setLoading, setError } = ticketSlice.actions
export default ticketSlice.reducer
