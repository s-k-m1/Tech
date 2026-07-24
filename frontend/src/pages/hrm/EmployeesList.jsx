import { useEffect, useCallback } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import DataTable from '../../components/ui/DataTable'
import StatusBadge from '../../components/ui/StatusBadge'
import { setEmployees } from '../../features/hrm/hrmSlice'
import { hrmService } from '../../services/api'

export default function EmployeesList() {
  const dispatch = useDispatch()
  const { employees } = useSelector((state) => state.hrm)

  const load = useCallback(async () => {
    try {
      const res = await hrmService.getEmployees()
      dispatch(setEmployees(res.data.results || res.data))
    } catch { /* silent */ }
  }, [dispatch])

  useEffect(() => { load() }, [load])

  const columns = [
    { header: 'Employee ID', accessor: 'employee_id' },
    { header: 'Designation', accessor: 'designation' },
    { header: 'Department', accessor: 'department' },
    { header: 'Joining Date', accessor: 'joining_date' },
    { header: 'Salary', accessor: 'salary' },
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Employees</h1>
      <DataTable columns={columns} data={employees} />
    </div>
  )
}
