import { useEffect, useState } from 'react'
import { Shield, AlertTriangle, CheckCircle, Activity } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import { securityService } from '../../services/api'
import StatusBadge from '../../components/ui/StatusBadge'

const chartData = [
  { hour: '00', events: 4, threats: 1 }, { hour: '04', events: 2, threats: 0 },
  { hour: '08', events: 12, threats: 3 }, { hour: '12', events: 8, threats: 2 },
  { hour: '16', events: 15, threats: 4 }, { hour: '20', events: 6, threats: 1 },
]

const threatData = [
  { type: 'SQL Injection', count: 12 }, { type: 'XSS', count: 8 },
  { type: 'Brute Force', count: 5 }, { type: 'Directory Traversal', count: 3 },
  { type: 'Suspicious Login', count: 7 },
]

export default function SecurityDashboard() {
  const [dashboard, setDashboard] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    (async () => {
      try {
        const res = await securityService.getDashboard()
        setDashboard(res.data)
      } catch { /* silent */ }
      finally { setLoading(false) }
    })()
  }, [])

  if (loading) return <div className="text-center py-12 text-gray-500">Loading security data...</div>

  const stats = [
    { label: 'Total Events', value: dashboard?.total_events ?? '--', icon: Activity, color: 'text-blue-600', bg: 'bg-blue-100' },
    { label: 'Critical', value: dashboard?.critical_events ?? '--', icon: Shield, color: 'text-red-600', bg: 'bg-red-100' },
    { label: 'High Risk', value: dashboard?.high_risk_events ?? '--', icon: AlertTriangle, color: 'text-orange-600', bg: 'bg-orange-100' },
    { label: 'Low Risk', value: dashboard?.low_risk_events ?? '--', icon: CheckCircle, color: 'text-green-600', bg: 'bg-green-100' },
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Security Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.label} className="bg-white rounded-lg border p-4">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${stat.bg}`}>
                  <Icon className={`h-5 w-5 ${stat.color}`} />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-800">{stat.value}</p>
                  <p className="text-xs text-gray-500">{stat.label}</p>
                </div>
              </div>
            </div>
          )
        })}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg border p-6">
          <h3 className="font-semibold text-gray-800 mb-4">Event Timeline (Last 24h)</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="hour" stroke="#9ca3af" fontSize={12} />
              <YAxis stroke="#9ca3af" fontSize={12} />
              <Tooltip />
              <Line type="monotone" dataKey="events" stroke="#3b82f6" strokeWidth={2} dot={{ r: 3 }} />
              <Line type="monotone" dataKey="threats" stroke="#ef4444" strokeWidth={2} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-lg border p-6">
          <h3 className="font-semibold text-gray-800 mb-4">Threats by Type</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={threatData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="type" stroke="#9ca3af" fontSize={11} angle={-20} textAnchor="end" />
              <YAxis stroke="#9ca3af" fontSize={12} />
              <Tooltip />
              <Bar dataKey="count" fill="#ef4444" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="bg-white rounded-lg border p-6">
        <h3 className="font-semibold text-gray-800 mb-4">Recent Events</h3>
        <div className="space-y-2">
          {[
            { action: 'login_success', risk: 'low', time: '2 min ago' },
            { action: 'failed_login', risk: 'medium', time: '5 min ago' },
            { action: 'sql_injection_blocked', risk: 'critical', time: '12 min ago' },
            { action: 'api_abuse_detected', risk: 'high', time: '18 min ago' },
            { action: 'login_success', risk: 'low', time: '25 min ago' },
          ].map((event, i) => (
            <div key={i} className="flex items-center justify-between py-2 border-b last:border-0">
              <div className="flex items-center gap-3">
                <span className="text-sm font-medium text-gray-700 capitalize">{event.action.replace(/_/g, ' ')}</span>
                <StatusBadge status={event.risk} />
              </div>
              <span className="text-xs text-gray-400">{event.time}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
