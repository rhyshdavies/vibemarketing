import Dashboard from '@/components/Dashboard'

export default function DashboardPage() {
  // Temporarily bypassing Clerk auth for testing
  // Uncomment below when you add Clerk keys

  /*
  import { auth } from '@clerk/nextjs'
  import { redirect } from 'next/navigation'

  const { userId } = auth()
  if (!userId) {
    redirect('/')
  }
  */

  return <Dashboard />
}
