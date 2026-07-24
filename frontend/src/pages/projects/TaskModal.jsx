import { useState } from 'react'
import Modal from '../../components/ui/Modal'
import Button from '../../components/ui/Button'
import toast from 'react-hot-toast'

const emptyTask = { title: '', description: '', status: 'todo', priority: 'medium', due_date: '', assignee: null }

export default function TaskModal({ isOpen, onClose, onSaved, editing }) {
  const [form, setForm] = useState(emptyTask)
  const [saving, setSaving] = useState(false)

  useState(() => {
    if (editing) setForm(editing)
    else setForm(emptyTask)
  }, [editing, isOpen])

  const handleSave = async () => {
    setSaving(true)
    try {
      const { projectService } = await import('../../services/api')
      if (editing?.id) {
        await projectService.updateTask(editing.id, form)
      } else {
        await projectService.createTask(form)
      }
      toast.success(editing ? 'Task updated' : 'Task created')
      onSaved?.()
      onClose()
    } catch { toast.error('Failed to save task') }
    finally { setSaving(false) }
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={editing ? 'Edit Task' : 'New Task'}>
      <div className="space-y-4">
        <div><label className="block text-sm font-medium text-gray-700 mb-1">Title</label><input type="text" value={form.title} onChange={(e) => setForm({...form, title: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" /></div>
        <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><textarea value={form.description} onChange={(e) => setForm({...form, description: e.target.value})} rows={3} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" /></div>
        <div className="grid grid-cols-2 gap-4">
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select value={form.status} onChange={(e) => setForm({...form, status: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
              <option value="todo">To Do</option><option value="in_progress">In Progress</option><option value="review">In Review</option><option value="done">Done</option>
            </select>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
            <select value={form.priority} onChange={(e) => setForm({...form, priority: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
              <option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option><option value="urgent">Urgent</option>
            </select>
          </div>
        </div>
        <div><label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label><input type="date" value={form.due_date?.split('T')[0] || ''} onChange={(e) => setForm({...form, due_date: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" /></div>
        <div className="flex justify-end gap-3 pt-2">
          <Button variant="secondary" onClick={onClose}>Cancel</Button>
          <Button onClick={handleSave} disabled={saving}>{saving ? 'Saving...' : 'Save'}</Button>
        </div>
      </div>
    </Modal>
  )
}
