import ICPCampaignFlow from '@/components/ICPCampaignFlow'

export default function NewCampaignPage() {
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

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <ICPCampaignFlow />
      </div>
    </div>
  )
}
