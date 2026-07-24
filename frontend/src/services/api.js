import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        const response = await axios.post('/api/auth/token/refresh/', {
          refresh: refreshToken,
        })
        localStorage.setItem('access_token', response.data.access)
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`
        return api(originalRequest)
      } catch {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/auth/login'
      }
    }
    return Promise.reject(error)
  }
)

export const authService = {
  login: (credentials) => api.post('/auth/login/', credentials),
  register: (data) => api.post('/auth/register/', data),
  logout: () => api.post('/auth/logout/'),
  getProfile: () => api.get('/auth/profile/'),
  getDevices: () => api.get('/auth/devices/'),
  deleteDevice: (id) => api.delete(`/auth/devices/${id}/`),
}

export const crmService = {
  getLeads: () => api.get('/crm/leads/'),
  createLead: (data) => api.post('/crm/leads/', data),
  updateLead: (id, data) => api.put(`/crm/leads/${id}/`, data),
  deleteLead: (id) => api.delete(`/crm/leads/${id}/`),
  getClients: () => api.get('/crm/clients/'),
  getContracts: () => api.get('/crm/contracts/'),
  getMeetings: () => api.get('/crm/meetings/'),
}

export const hrmService = {
  getEmployees: () => api.get('/hrm/employees/'),
  getAttendance: () => api.get('/hrm/attendance/'),
  getLeaves: () => api.get('/hrm/leaves/'),
  getPayroll: () => api.get('/hrm/payroll/'),
}

export const projectService = {
  getProjects: () => api.get('/projects/projects/'),
  getTasks: () => api.get('/projects/tasks/'),
  getMilestones: () => api.get('/projects/milestones/'),
  getSprints: () => api.get('/projects/sprints/'),
}

export const ticketService = {
  getTickets: () => api.get('/tickets/tickets/'),
  createTicket: (data) => api.post('/tickets/tickets/', data),
  updateTicket: (id, data) => api.put(`/tickets/tickets/${id}/`, data),
}

export const securityService = {
  getDashboard: () => api.get('/security/dashboard/'),
  getReport: () => api.get('/security/report/'),
}

export const notificationService = {
  getNotifications: () => api.get('/notifications/notifications/'),
  markAsRead: (id) => api.patch(`/notifications/notifications/${id}/`, { is_read: true }),
}

export default api
