import { Routes, Route, Navigate } from 'react-router-dom'
import TicketsList from './TicketsList'
import TicketDetail from './TicketDetail'

export default function TicketsPage() {
  return (
    <Routes>
      <Route index element={<TicketsList />} />
      <Route path=":id" element={<TicketDetail />} />
    </Routes>
  )
}
