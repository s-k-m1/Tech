import { createSlice } from '@reduxjs/toolkit'

const projectSlice = createSlice({
  name: 'projects',
  initialState: {
    projects: [],
    milestones: [],
    sprints: [],
    tasks: [],
    loading: false,
    error: null,
  },
  reducers: {
    setProjects: (state, action) => { state.projects = action.payload },
    setMilestones: (state, action) => { state.milestones = action.payload },
    setSprints: (state, action) => { state.sprints = action.payload },
    setTasks: (state, action) => { state.tasks = action.payload },
    setLoading: (state, action) => { state.loading = action.payload },
    setError: (state, action) => { state.error = action.payload },
  },
})

export const { setProjects, setMilestones, setSprints, setTasks, setLoading, setError } = projectSlice.actions
export default projectSlice.reducer
