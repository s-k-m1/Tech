import { configureStore } from '@reduxjs/toolkit'
import authReducer from './auth/authSlice'
import crmReducer from './crm/crmSlice'
import hrmReducer from './hrm/hrmSlice'
import projectReducer from './projects/projectSlice'
import ticketReducer from './tickets/ticketSlice'
import dashboardReducer from './dashboard/dashboardSlice'
import securityReducer from './security/securitySlice'
import notificationReducer from './notifications/notificationSlice'
import erpReducer from './erp/erpSlice'
import accountingReducer from './accounting/accountingSlice'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    crm: crmReducer,
    hrm: hrmReducer,
    projects: projectReducer,
    tickets: ticketReducer,
    dashboard: dashboardReducer,
    security: securityReducer,
    notifications: notificationReducer,
    erp: erpReducer,
    accounting: accountingReducer,
  },
})
