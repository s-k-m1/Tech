import { useEffect, useState, useCallback } from 'react'
import { Plus } from 'lucide-react'
import StatusBadge from '../../components/ui/StatusBadge'
import Button from '../../components/ui/Button'
import TaskModal from './TaskModal'
import toast from 'react-hot-toast'

const columns = [
  { key: 'todo', label: 'To Do', color: 'bg-gray-100' },
  { key: 'in_progress', label: 'In Progress', color: 'bg-blue-50' },
  { key: 'review', label: 'In Review', color: 'bg-orange-50' },
  { key: 'done', label: 'Done', color: 'bg-green-50' },
]

export default function KanbanBoard() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [dragOver, setDragOver] = useState(null)

  const load = useCallback(async () => {
    try {
      const { projectService } = await import('../../services/api')
      const res = await projectService.getTasks()
      setTasks(res.data.results || res.data)
    } catch { /* silent */ }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { load() }, [load])

  const getColumnTasks = (status) => tasks.filter((t) => t.status === status)

  const handleDragStart = (e, task) => {
    e.dataTransfer.setData('text/plain', JSON.stringify(task))
  }

  const handleDrop = async (e, newStatus) => {
    e.preventDefault()
    setDragOver(null)
    try {
      const task = JSON.parse(e.dataTransfer.getData('text/plain'))
      const { projectService } = await import('../../services/api')
      await projectService.updateTask(task.id, { ...task, status: newStatus })
      setTasks((prev) => prev.map((t) => (t.id === task.id ? { ...t, status: newStatus } : t)))
      toast.success(`Task moved to ${newStatus.replace('_', ' ')}`)
    } catch { toast.error('Failed to move task') }
  }

  const openEdit = (task) => { setEditing(task); setModalOpen(true) }
  const handleNew = () => { setEditing(null); setModalOpen(true) }
  const handleSaved = () => { setEditing(null); load() }

  if (loading) return <div className="text-center py-12 text-gray-500">Loading tasks...</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Kanban Board</h1>
        <Button onClick={handleNew}><Plus className="h-4 w-4 mr-1 inline" /> Add Task</Button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {columns.map((col) => (
          <div
            key={col.key}
            onDragOver={(e) => { e.preventDefault(); setDragOver(col.key) }}
            onDragLeave={() => setDragOver(null)}
            onDrop={(e) => handleDrop(e, col.key)}
            className={`rounded-lg p-3 min-h-[400px] transition-colors ${col.color} ${dragOver === col.key ? 'ring-2 ring-primary-400' : ''}`}
          >
            <h3 className="font-semibold text-gray-700 text-sm mb-3 px-2">{col.label} ({getColumnTasks(col.key).length})</h3>
            <div className="space-y-2">
              {getColumnTasks(col.key).map((task) => (
                <div
                  key={task.id}
                  draggable
                  onDragStart={(e) => handleDragStart(e, task)}
                  onClick={() => openEdit(task)}
                  className="bg-white rounded-lg shadow-sm p-3 cursor-grab active:cursor-grabbing hover:shadow-md transition-shadow"
                >
                  <p className="text-sm font-medium text-gray-800 mb-2">{task.title}</p>
                  <div className="flex items-center justify-between">
                    <StatusBadge status={task.priority} />
                    {task.due_date && (
                      <span className="text-xs text-gray-400">{new Date(task.due_date).toLocaleDateString()}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      <TaskModal isOpen={modalOpen} onClose={() => setModalOpen(false)} editing={editing} onSaved={handleSaved} />
    </div>
  )
}
