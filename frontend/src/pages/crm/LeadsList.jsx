import { useEffect, useState, useCallback } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Plus } from 'lucide-react'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import Modal from '../../components/ui/Modal'
import Button from '../../components/ui/Button'
import { setLeads } from '../../features/crm/crmSlice'
import { crmService } from '../../services/api'

const emptyLead = { first_name: '', last_name: '', email: '', phone: '', company: '', source: '', status: 'new', notes: '' }

export default function LeadsList() {
  const dispatch = useDispatch()
  const { leads } = useSelector((state) => state.crm)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(emptyLead)
  const [saving, setSaving] = useState(false)

  const load = useCallback(async () => {
    try {
      const res = await crmService.getLeads()
      dispatch(setLeads(res.data.results || res.data))
    } catch { /* silent */ }
  }, [dispatch])

  useEffect(() => { load() }, [load])

  const openCreate = () => { setEditing(null); setForm(emptyLead); setModalOpen(true) }
  const openEdit = (row) => { setEditing(row); setForm(row); setModalOpen(true) }

  const handleSave = async () => {
    setSaving(true)
    try {
      if (editing) {
        await crmService.updateLead(editing.id, form)
      } else {
        await crmService.createLead(form)
      }
      setModalOpen(false)
      await load()
    } finally { setSaving(false) }
  }

  const columns = [
    { header: 'Name', accessor: 'first_name', render: (_, r) => `${r.first_name} ${r.last_name}` },
    { header: 'Email', accessor: 'email' },
    { header: 'Company', accessor: 'company' },
    { header: 'Status', accessor: 'status', render: (v) => <StatusBadge status={v} /> },
    { header: 'Source', accessor: 'source' },
    { header: 'Score', accessor: 'score' },
  ]

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Leads</h1>
        <Button onClick={openCreate}><Plus className="h-4 w-4 mr-1 inline" /> Add Lead</Button>
      </div>
      <DataTable columns={columns} data={leads} onRowClick={openEdit} />
      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title={editing ? 'Edit Lead' : 'New Lead'}>
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">First Name</label><input type="text" value={form.first_name} onChange={(e) => setForm({...form, first_name: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500" /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label><input type="text" value={form.last_name} onChange={(e) => setForm({...form, last_name: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500" /></div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Email</label><input type="email" value={form.email} onChange={(e) => setForm({...form, email: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500" /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Phone</label><input type="text" value={form.phone} onChange={(e) => setForm({...form, phone: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500" /></div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Company</label><input type="text" value={form.company} onChange={(e) => setForm({...form, company: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500" /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Source</label>
              <select value={form.source} onChange={(e) => setForm({...form, source: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500">
                <option value="">Select</option><option value="website">Website</option><option value="referral">Referral</option><option value="social">Social Media</option><option value="email">Email</option><option value="call">Phone Call</option>
              </select>
            </div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select value={form.status} onChange={(e) => setForm({...form, status: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500">
              <option value="new">New</option><option value="contacted">Contacted</option><option value="qualified">Qualified</option><option value="converted">Converted</option><option value="lost">Lost</option>
            </select>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Notes</label><textarea value={form.notes} onChange={(e) => setForm({...form, notes: e.target.value})} rows={3} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500" /></div>
          <div className="flex justify-end gap-3 pt-2">
            <Button variant="secondary" onClick={() => setModalOpen(false)}>Cancel</Button>
            <Button onClick={handleSave} disabled={saving}>{saving ? 'Saving...' : 'Save'}</Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
