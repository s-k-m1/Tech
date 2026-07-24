import { render, screen } from '@testing-library/react'
import Button from '../components/ui/Button'

test('renders button with text', () => {
  render(<Button>Click me</Button>)
  expect(screen.getByText('Click me')).toBeInTheDocument()
})

test('applies variant classes', () => {
  const { container } = render(<Button variant="danger">Delete</Button>)
  expect(container.firstChild).toHaveClass('bg-red-600')
})

test('disabled button does not fire click', () => {
  const handleClick = jest.fn()
  render(<Button disabled onClick={handleClick}>Disabled</Button>)
  screen.getByText('Disabled').click()
  expect(handleClick).not.toHaveBeenCalled()
})
