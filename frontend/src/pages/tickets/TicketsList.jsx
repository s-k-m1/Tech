import { useEffect, useState, useCallback } from 'react'
import { Plus } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import Button from '../../components/ui/Button'
import Modal from '../../components/ui/Modal'
import toast from 'react-hot-toast'
import { ticketService } from '../../services/api'

const emptyTicket = { subject: '', description: '', priority: 'medium', category: '' }

export default function TicketsList() {
  const navigate = useNavigate()
  const [tickets, setTickets] = useState([])
  const [modalOpen, setModalOpen] = useState(false)
  const [form, setForm] = useState(emptyTicket)
  const [saving, setSaving] = useState(false)

  const load = useCallback(async () => {
    try {
      const res = await ticketService.getTickets()
      setTickets(res.data.results || res.data)
    } catch { /* silent */ }
  }, [])

  useEffect(() => { load() }, [load])

  const handleCreate = async () => {
    setSaving(true)
    try {
      await ticketService.createTicket(form)
      toast.success('Ticket created')
      setModalOpen(false)
      setForm(emptyTicket)
      await load()
    } catch { toast.error('Failed to create ticket') }
    finally { setSaving(false) }
  }

  const handleStatusChange = async (ticket, newStatus) => {
    try {
      await ticketService.updateTicket(ticket.id, { ...ticket, status: newStatus })
      toast.success(`Ticket ${newStatus}`)
      await load()
    } catch { toast.error('Failed to update ticket') }
  }

  const columns = [
    { header: 'Subject', accessor: 'subject' },
    { header: 'Status', accessor: 'status', render: (v) => <StatusBadge status={v} /> },
    { header: 'Priority', accessor: 'priority', render: (v) => <StatusBadge status={v} /> },
    { header: 'Category', accessor: 'category' },
    { header: 'Assignee', accessor: 'assignee' },
    {
      header: 'Actions', accessor: 'status',
      render: (v, row) => (
        <select
          value={v}
          onChange={(e) => { e.stopPropagation(); handleStatusChange(row, e.target.value) }}
          onClick={(e) => e.stopPropagation()}
          className="text-xs border border-gray-300 rounded px-1 py-0.5 focus:ring-1 focus:ring-primary-500"
        >
          <option value="open">Open</option><option value="in_progress">In Progress</option>
          <option value="resolved">Resolved</option><option value="closed">Closed</option>
        </select>
      ),
    },
  ]

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Tickets</h1>
        <Button onClick={() => setModalOpen(true)}><Plus className="h-4 w-4 mr-1 inline" /> New Ticket</Button>
      </div>
      <DataTable columns={columns} data={tickets} onRowClick={(row) => navigate(`/tickets/${row.id}`)} />
      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="New Ticket">
        <div className="space-y-4">
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Subject</label><input type="text" value={form.subject} onChange={(e) => setForm({...form, subject: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><textarea value={form.description} onChange={(e) => setForm({...form, description: e.target.value})} rows={3} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" /></div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
              <select value={form.priority} onChange={(e) => setForm({...form, priority: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
                <option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option><option value="critical">Critical</option>
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Category</label><input type="text" value={form.category} onChange={(e) => setForm({...form, category: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" /></div>
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <Button variant="secondary" onClick={() => setModalOpen(false)}>Cancel</Button>
            <Button onClick={handleCreate} disabled={saving}>{saving ? 'Creating...' : 'Create'}</Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
