import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Send } from 'lucide-react'
import StatusBadge from '../../components/ui/StatusBadge'
import Button from '../../components/ui/Button'
import { ticketService } from '../../services/api'
import toast from 'react-hot-toast'

export default function TicketDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [ticket, setTicket] = useState(null)
  const [comments, setComments] = useState([])
  const [newComment, setNewComment] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    (async () => {
      try {
        const res = await ticketService.getTickets()
        const found = (res.data.results || res.data).find((t) => t.id === id)
        if (found) setTicket(found)
      } catch { /* silent */ }
      finally { setLoading(false) }
    })()
  }, [id])

  useEffect(() => {
    (async () => {
      try {
        const res = await ticketService.getComments()
        const ticketComments = (res.data.results || res.data).filter(c => c.ticket === id)
        setComments(ticketComments)
      } catch { /* silent */ }
    })()
  }, [id])

  const handleAddComment = async () => {
    if (!newComment.trim()) return
    try {
      const res = await ticketService.createComment({ ticket: id, content: newComment })
      setComments([...comments, res.data])
      setNewComment('')
      toast.success('Comment added')
    } catch { toast.error('Failed to add comment') }
  }

  if (loading) return <div className="text-center py-12 text-gray-500">Loading...</div>
  if (!ticket) return <div className="text-center py-12 text-gray-500">Ticket not found</div>

  return (
    <div className="max-w-3xl">
      <button onClick={() => navigate('/tickets')} className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 mb-4">
        <ArrowLeft className="h-4 w-4" /> Back to Tickets
      </button>
      <div className="bg-white rounded-lg border p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-xl font-bold text-gray-800">{ticket.subject}</h1>
          <StatusBadge status={ticket.status} />
        </div>
        <div className="flex gap-4 text-sm text-gray-500 mb-4">
          <span>Priority: <StatusBadge status={ticket.priority} /></span>
          {ticket.category && <span>Category: {ticket.category}</span>}
        </div>
        <p className="text-gray-700 whitespace-pre-wrap">{ticket.description}</p>
      </div>
      <div className="bg-white rounded-lg border p-6">
        <h2 className="font-semibold text-gray-800 mb-4">Comments ({comments.length})</h2>
        <div className="space-y-3 mb-4">
          {comments.map((c, i) => (
            <div key={i} className="border-b pb-3">
              <div className="flex items-center gap-2 text-xs text-gray-400 mb-1">
                <span className="font-medium text-gray-600">{c.author_name}</span>
                <span>{new Date(c.created_at).toLocaleString()}</span>
              </div>
              <p className="text-sm text-gray-700">{c.content}</p>
            </div>
          ))}
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Add a comment..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500"
            onKeyDown={(e) => e.key === 'Enter' && handleAddComment()}
          />
          <Button onClick={handleAddComment}><Send className="h-4 w-4" /></Button>
        </div>
      </div>
    </div>
  )
}
