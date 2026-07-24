import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { Bell } from 'lucide-react'
import { setNotifications, markAsRead } from '../../features/notifications/notificationSlice'
import { notificationService } from '../../services/api'

export default function NotificationsDropdown() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { notifications, unreadCount } = useSelector((state) => state.notifications)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    (async () => {
      try {
        const res = await notificationService.getNotifications()
        dispatch(setNotifications(res.data.results || res.data))
      } catch { /* silent */ }
    })()
  }, [dispatch])

  const handleMarkRead = async (id) => {
    try {
      await notificationService.markAsRead(id)
      dispatch(markAsRead(id))
    } catch { /* silent */ }
  }

  return (
    <div className="relative">
      <button onClick={() => setOpen(!open)} className="relative p-2 text-gray-500 hover:text-gray-700">
        <Bell className="h-5 w-5" />
        {unreadCount > 0 && (
          <span className="absolute top-1 right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
            {unreadCount}
          </span>
        )}
      </button>
      {open && (
        <>
          <div className="fixed inset-0 z-10" onClick={() => setOpen(false)} />
          <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border z-20">
            <div className="p-3 border-b">
              <h3 className="text-sm font-semibold text-gray-700">Notifications</h3>
            </div>
            <div className="max-h-64 overflow-y-auto">
              {notifications.length === 0 ? (
                <p className="text-center text-gray-500 text-sm py-6">No notifications</p>
              ) : (
                notifications.slice(0, 10).map((n) => (
                  <div key={n.id} className={`p-3 border-b hover:bg-gray-50 cursor-pointer ${!n.is_read ? 'bg-primary-50' : ''}`}
                    onClick={() => { handleMarkRead(n.id); navigate(n.link || '/dashboard') }}>
                    <p className="text-sm font-medium text-gray-700">{n.title}</p>
                    <p className="text-xs text-gray-500 mt-1">{n.message}</p>
                    <p className="text-xs text-gray-400 mt-1">{new Date(n.created_at).toLocaleString()}</p>
                  </div>
                ))
              )}
            </div>
          </div>
        </>
      )}
    </div>
  )
}
