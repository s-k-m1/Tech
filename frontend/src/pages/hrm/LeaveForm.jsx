import { useState } from 'react'
import Button from '../../components/ui/Button'
import toast from 'react-hot-toast'

export default function LeaveForm() {
  const [form, setForm] = useState({ leave_type: 'annual', start_date: '', end_date: '', reason: '' })
  const [saving, setSaving] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      const { hrmService } = await import('../../services/api')
      await hrmService.createLeave(form)
      toast.success('Leave request submitted')
      setForm({ leave_type: 'annual', start_date: '', end_date: '', reason: '' })
    } catch {
      toast.error('Failed to submit leave request')
    } finally { setSaving(false) }
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Apply for Leave</h1>
      <div className="bg-white rounded-lg border p-6 max-w-lg">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Leave Type</label>
            <select value={form.leave_type} onChange={(e) => setForm({...form, leave_type: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500">
              <option value="annual">Annual</option><option value="sick">Sick</option><option value="personal">Personal</option><option value="maternity">Maternity</option><option value="paternity">Paternity</option><option value="unpaid">Unpaid</option>
            </select>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label><input type="date" value={form.start_date} onChange={(e) => setForm({...form, start_date: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500" required /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">End Date</label><input type="date" value={form.end_date} onChange={(e) => setForm({...form, end_date: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500" required /></div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Reason</label><textarea value={form.reason} onChange={(e) => setForm({...form, reason: e.target.value})} rows={3} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500" required /></div>
          <Button type="submit" disabled={saving}>{saving ? 'Submitting...' : 'Submit Request'}</Button>
        </form>
      </div>
    </div>
  )
}
