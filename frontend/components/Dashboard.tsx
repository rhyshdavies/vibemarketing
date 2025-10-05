'use client'

import { useEffect, useState, useCallback } from 'react'
// Temporarily disabled Clerk for testing
// import { useUser } from '@clerk/nextjs'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Mail, MousePointer, Reply, TrendingUp, Loader2, Linkedin } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Campaign {
  id: string
  campaign_id: string
  url: string
  target_audience: string
  status: string
  sent: number
  opened: number
  clicked: number
  replied: number
  open_rate: number
  click_rate: number
  reply_rate: number
  created_at: string
}

interface Stats {
  total_campaigns: number
  active_campaigns: number
  total_sent: number
  total_opened: number
  total_clicked: number
  total_replied: number
  avg_open_rate: number
  avg_reply_rate: number
}

export default function Dashboard() {
  // Temporary: Using mock user for testing
  const user = { id: 'demo_user_123' }
  const [campaigns, setCampaigns] = useState<Campaign[]>([])
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)
  const [hasLinkedInAccount, setHasLinkedInAccount] = useState<boolean | null>(null)

  const loadDashboardData = useCallback(async () => {
    try {
      setLoading(true)

      // Load campaigns
      const campaignsResponse = await axios.get(`${API_URL}/api/campaigns`, {
        params: { user_id: user.id }
      })
      console.log('[Dashboard] Campaigns response:', campaignsResponse.data)
      console.log('[Dashboard] Setting campaigns:', campaignsResponse.data.campaigns?.length || 0)
      setCampaigns(campaignsResponse.data.campaigns || [])

      // Calculate stats
      const campaignData = campaignsResponse.data.campaigns || []
      const calculatedStats: Stats = {
        total_campaigns: campaignData.length,
        active_campaigns: campaignData.filter((c: Campaign) => c.status === 'active').length,
        total_sent: campaignData.reduce((sum: number, c: Campaign) => sum + (c.sent || 0), 0),
        total_opened: campaignData.reduce((sum: number, c: Campaign) => sum + (c.opened || 0), 0),
        total_clicked: campaignData.reduce((sum: number, c: Campaign) => sum + (c.clicked || 0), 0),
        total_replied: campaignData.reduce((sum: number, c: Campaign) => sum + (c.replied || 0), 0),
        avg_open_rate: 0,
        avg_reply_rate: 0
      }

      if (calculatedStats.total_sent > 0) {
        calculatedStats.avg_open_rate = Math.round((calculatedStats.total_opened / calculatedStats.total_sent) * 100)
        calculatedStats.avg_reply_rate = Math.round((calculatedStats.total_replied / calculatedStats.total_sent) * 100)
      }

      setStats(calculatedStats)
    } catch (error) {
      console.error('Error loading dashboard:', error)
    } finally {
      setLoading(false)
    }
  }, [user.id])

  useEffect(() => {
    loadDashboardData()

    // Check LinkedIn account status once on mount
    const checkLinkedInAccount = async () => {
      try {
        const accountsResponse = await axios.get(`${API_URL}/api/linkedin/accounts`)
        setHasLinkedInAccount(accountsResponse.data.has_account)
      } catch (error) {
        console.error('Error checking LinkedIn account:', error)
      }
    }
    checkLinkedInAccount()
  }, [loadDashboardData])

  // Separate effect for handling LinkedIn auth redirect
  useEffect(() => {
    console.log('[Redirect] Effect running, campaigns.length:', campaigns.length)

    // Only run once campaigns are loaded
    if (campaigns.length === 0) {
      console.log('[Redirect] Waiting for campaigns to load...')
      return
    }

    // Check if redirected back from LinkedIn auth with campaign_id
    const urlParams = new URLSearchParams(window.location.search)
    const linkedinConnected = urlParams.get('linkedin_connected')
    const campaignId = urlParams.get('campaign_id')

    console.log('[Redirect] URL params:', { linkedinConnected, campaignId })

    if (linkedinConnected === 'true' && campaignId) {
      // Find the campaign and auto-open the modal
      const campaign = campaigns.find(c => c.campaign_id === campaignId)
      console.log('[Redirect] Found campaign:', campaign?.url || 'NOT FOUND')

      if (campaign) {
        // Clear URL params
        window.history.replaceState({}, '', '/dashboard')

        // Mark LinkedIn as connected
        setHasLinkedInAccount(true)

        // Open modal at generate step
        setLinkedInModal({
          show: true,
          campaign,
          step: 'generate',
          message: '',
          loading: false,
          leads: [],
          previewLead: null
        })
      }
    }
  }, [campaigns])

  const [linkedInModal, setLinkedInModal] = useState<{
    show: boolean
    campaign: Campaign | null
    step: 'select-account' | 'generate' | 'preview' | 'confirm'
    message: string
    loading: boolean
    leads: any[]
    previewLead: any | null
    accounts: any[]
    selectedAccount: any | null
  }>({
    show: false,
    campaign: null,
    step: 'select-account',
    message: '',
    loading: false,
    leads: [],
    previewLead: null,
    accounts: [],
    selectedAccount: null
  })

  const handleLaunchLinkedIn = async (campaign: Campaign) => {
    try {
      // Always fetch the current list of LinkedIn accounts
      const accountsResponse = await axios.get(`${API_URL}/api/linkedin/accounts`)
      const accounts = accountsResponse.data.accounts || []

      // Show modal with account selection step
      setLinkedInModal({
        show: true,
        campaign,
        step: 'select-account',
        message: '',
        loading: false,
        leads: [],
        previewLead: null,
        accounts,
        selectedAccount: accounts.length > 0 ? accounts[0] : null
      })
    } catch (error: any) {
      console.error('Error launching LinkedIn flow:', error)
      alert(`Failed to start LinkedIn campaign: ${error.response?.data?.detail || error.message}`)
    }
  }

  const handleConnectNewLinkedInAccount = async () => {
    try {
      const authResponse = await axios.post(`${API_URL}/api/linkedin/connect`, {
        campaign_id: linkedInModal.campaign?.campaign_id
      })
      if (authResponse.data.success) {
        // Redirect to Unipile hosted auth
        window.location.href = authResponse.data.auth_url
      }
    } catch (error: any) {
      console.error('Error connecting LinkedIn account:', error)
      alert(`Failed to connect account: ${error.response?.data?.detail || error.message}`)
    }
  }

  const handleContinueWithAccount = () => {
    if (!linkedInModal.selectedAccount) return
    // Move to generate step
    setLinkedInModal({ ...linkedInModal, step: 'generate' })
  }

  const handleGenerateMessage = async () => {
    if (!linkedInModal.campaign) return

    try {
      setLinkedInModal({ ...linkedInModal, loading: true })

      // Generate message using web search
      const messageResponse = await axios.post(`${API_URL}/api/linkedin/generate-message`, {
        campaign_id: linkedInModal.campaign.campaign_id,
        user_id: user.id
      })

      if (messageResponse.data.success) {
        setLinkedInModal({
          ...linkedInModal,
          step: 'preview',
          message: messageResponse.data.message,
          loading: false
        })
      }
    } catch (error: any) {
      console.error('Error generating LinkedIn message:', error)
      alert(`Failed to generate message: ${error.response?.data?.detail || error.message}`)
      setLinkedInModal({ ...linkedInModal, loading: false })
    }
  }

  const handleShowLeadPreview = async () => {
    if (!linkedInModal.campaign) return

    try {
      setLinkedInModal({ ...linkedInModal, loading: true, step: 'confirm' })

      // Fetch leads from campaign
      const leadsResponse = await axios.get(
        `${API_URL}/api/linkedin/campaign-leads/${linkedInModal.campaign.campaign_id}`,
        {
          params: {
            user_id: user.id,
            limit: 10
          }
        }
      )

      if (leadsResponse.data.success) {
        setLinkedInModal({
          ...linkedInModal,
          loading: false,
          step: 'confirm',
          leads: leadsResponse.data.leads || []
        })
      } else {
        // No leads found, still show confirm step
        setLinkedInModal({
          ...linkedInModal,
          loading: false,
          step: 'confirm',
          leads: []
        })
      }
    } catch (error: any) {
      console.error('Error loading leads:', error)
      setLinkedInModal({ ...linkedInModal, loading: false, step: 'confirm', leads: [] })
    }
  }

  const launchLinkedInCampaign = async () => {
    if (!linkedInModal.campaign) return

    try {
      setLinkedInModal({ ...linkedInModal, loading: true })

      const response = await axios.post(`${API_URL}/api/linkedin/launch-campaign`, {
        campaign_id: linkedInModal.campaign.campaign_id,
        user_id: user.id,
        message: linkedInModal.message,
        account_id: linkedInModal.selectedAccount?.id
      })

      if (response.data.success) {
        const { sent_count, connection_requests_sent } = response.data
        let message = 'LinkedIn campaign launched successfully!\n'
        if (sent_count > 0) message += `✓ ${sent_count} direct message${sent_count > 1 ? 's' : ''} sent\n`
        if (connection_requests_sent > 0) message += `✓ ${connection_requests_sent} connection request${connection_requests_sent > 1 ? 's' : ''} sent with your message`

        alert(message)
        setLinkedInModal({ show: false, campaign: null, step: 'generate', message: '', loading: false, leads: [], previewLead: null })
        loadDashboardData() // Refresh dashboard
      } else if (response.data.needs_auth) {
        alert(response.data.message)
        setLinkedInModal({ show: false, campaign: null, step: 'generate', message: '', loading: false, leads: [], previewLead: null })
      }
    } catch (error: any) {
      console.error('Error launching LinkedIn campaign:', error)
      alert(`Failed to launch LinkedIn campaign: ${error.response?.data?.detail || error.message}`)
      setLinkedInModal({ show: false, campaign: null, step: 'generate', message: '', loading: false, leads: [] })
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    )
  }

  const chartData = campaigns.slice(0, 5).map(campaign => ({
    name: campaign.url.substring(0, 20) + '...',
    sent: campaign.sent,
    opened: campaign.opened,
    replied: campaign.replied
  }))

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
          <p className="text-gray-600">Overview of all your campaigns</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            icon={<Mail className="w-6 h-6" />}
            label="Total Sent"
            value={stats?.total_sent || 0}
            color="blue"
          />
          <StatCard
            icon={<MousePointer className="w-6 h-6" />}
            label="Avg Open Rate"
            value={`${stats?.avg_open_rate || 0}%`}
            color="green"
          />
          <StatCard
            icon={<Reply className="w-6 h-6" />}
            label="Avg Reply Rate"
            value={`${stats?.avg_reply_rate || 0}%`}
            color="purple"
          />
          <StatCard
            icon={<TrendingUp className="w-6 h-6" />}
            label="Active Campaigns"
            value={stats?.active_campaigns || 0}
            color="orange"
          />
        </div>

        {/* Chart */}
        {campaigns.length > 0 && (
          <div className="card mb-8">
            <h2 className="text-xl font-semibold mb-4">Campaign Performance</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="sent" fill="#3b82f6" name="Sent" />
                <Bar dataKey="opened" fill="#10b981" name="Opened" />
                <Bar dataKey="replied" fill="#8b5cf6" name="Replied" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Campaigns List */}
        <div className="card">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold">Your Campaigns</h2>
            <div className="flex gap-3">
              <a href="/dashboard/domains">
                <button className="btn-secondary">🌐 Manage Domains</button>
              </a>
              <a href="/dashboard/new-campaign">
                <button className="btn-primary">+ New Campaign</button>
              </a>
            </div>
          </div>

          {campaigns.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 mb-4">No campaigns yet</p>
              <a href="/dashboard/new-campaign">
                <button className="btn-primary">Create Your First Campaign</button>
              </a>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="border-b border-gray-200">
                  <tr className="text-left">
                    <th className="pb-3 font-semibold">URL</th>
                    <th className="pb-3 font-semibold">Status</th>
                    <th className="pb-3 font-semibold text-right">Sent</th>
                    <th className="pb-3 font-semibold text-right">Open Rate</th>
                    <th className="pb-3 font-semibold text-right">Reply Rate</th>
                    <th className="pb-3 font-semibold">Created</th>
                    <th className="pb-3"></th>
                  </tr>
                </thead>
                <tbody>
                  {campaigns.map((campaign) => (
                    <tr key={campaign.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-4">
                        <div className="font-medium">{campaign.url}</div>
                        <div className="text-sm text-gray-500">{campaign.target_audience.substring(0, 50)}...</div>
                      </td>
                      <td className="py-4">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                          campaign.status === 'active'
                            ? 'bg-green-100 text-green-700'
                            : 'bg-gray-100 text-gray-700'
                        }`}>
                          {campaign.status}
                        </span>
                      </td>
                      <td className="py-4 text-right">{campaign.sent || 0}</td>
                      <td className="py-4 text-right">{campaign.open_rate || 0}%</td>
                      <td className="py-4 text-right">{campaign.reply_rate || 0}%</td>
                      <td className="py-4">
                        {new Date(campaign.created_at).toLocaleDateString()}
                      </td>
                      <td className="py-4">
                        <div className="flex items-center gap-3">
                          <a
                            href={`/dashboard/campaigns/${campaign.campaign_id}`}
                            className="text-primary-600 hover:text-primary-700 font-medium"
                          >
                            View →
                          </a>
                          <button
                            onClick={() => handleLaunchLinkedIn(campaign)}
                            className="flex items-center gap-1 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors"
                          >
                            <Linkedin className="w-4 h-4" />
                            LinkedIn
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Message Preview Modal */}
      {linkedInModal.previewLead && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[60] p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-lg w-full">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-gray-900">Message Preview</h3>
                <button
                  onClick={() => setLinkedInModal({ ...linkedInModal, previewLead: null })}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
            </div>
            <div className="p-6">
              <div className="mb-4">
                <p className="text-sm text-gray-600 mb-2">Sending to:</p>
                <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-semibold">
                    {linkedInModal.previewLead.first_name?.[0]}{linkedInModal.previewLead.last_name?.[0]}
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">
                      {linkedInModal.previewLead.first_name} {linkedInModal.previewLead.last_name}
                    </p>
                    <p className="text-xs text-gray-600">{linkedInModal.previewLead.title} at {linkedInModal.previewLead.company}</p>
                  </div>
                </div>
              </div>

              <div>
                <p className="text-sm text-gray-600 mb-2">Message:</p>
                <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg">
                  <p className="text-sm whitespace-pre-wrap">
                    {linkedInModal.message.replace('[First Name]', linkedInModal.previewLead.first_name)}
                  </p>
                  <p className="text-xs text-gray-500 mt-3">
                    {linkedInModal.message.replace('[First Name]', linkedInModal.previewLead.first_name).length} / 300 characters
                  </p>
                </div>
              </div>

              <button
                onClick={() => setLinkedInModal({ ...linkedInModal, previewLead: null })}
                className="mt-4 w-full px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* LinkedIn Campaign Modal */}
      {linkedInModal.show && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">
                    {linkedInModal.step === 'select-account' && 'Select LinkedIn Account'}
                    {linkedInModal.step === 'generate' && 'Generate LinkedIn Message'}
                    {linkedInModal.step === 'preview' && 'Review & Edit Message'}
                    {linkedInModal.step === 'confirm' && 'Confirm Lead Selection'}
                  </h2>
                  <p className="text-sm text-gray-600 mt-1">
                    {linkedInModal.campaign?.url}
                  </p>
                </div>
                <button
                  onClick={() => setLinkedInModal({ show: false, campaign: null, step: 'select-account', message: '', loading: false, leads: [], previewLead: null, accounts: [], selectedAccount: null })}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
            </div>

            <div className="p-6">
              {linkedInModal.loading ? (
                <div className="flex items-center justify-center py-12">
                  <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
                  <span className="ml-3 text-gray-600">
                    {linkedInModal.step === 'generate' && 'Analyzing website...'}
                    {linkedInModal.step === 'preview' && 'Generating message...'}
                    {linkedInModal.step === 'confirm' && 'Loading leads...'}
                  </span>
                </div>
              ) : (
                <>
                  {/* Step 0: Select Account */}
                  {linkedInModal.step === 'select-account' && (
                    <div className="py-4">
                      <h3 className="text-lg font-semibold mb-4">Choose a LinkedIn account:</h3>

                      {linkedInModal.accounts.length > 0 ? (
                        <div className="space-y-3 mb-6">
                          {linkedInModal.accounts.map((account: any) => (
                            <button
                              key={account.id}
                              onClick={() => setLinkedInModal({ ...linkedInModal, selectedAccount: account })}
                              className={`w-full p-4 border-2 rounded-lg text-left transition-colors ${
                                linkedInModal.selectedAccount?.id === account.id
                                  ? 'border-blue-600 bg-blue-50'
                                  : 'border-gray-200 hover:border-blue-300'
                              }`}
                            >
                              <div className="flex items-center gap-3">
                                <Linkedin className="w-8 h-8 text-blue-600" />
                                <div>
                                  <p className="font-medium text-gray-900">{account.name || 'LinkedIn Account'}</p>
                                  <p className="text-sm text-gray-500">
                                    Connected: {new Date(account.created_at).toLocaleDateString()}
                                  </p>
                                </div>
                              </div>
                            </button>
                          ))}
                        </div>
                      ) : (
                        <p className="text-gray-600 mb-6">No LinkedIn accounts connected yet.</p>
                      )}

                      <div className="flex items-center justify-between gap-3 pt-4 border-t border-gray-200">
                        <button
                          onClick={handleConnectNewLinkedInAccount}
                          className="px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors border border-blue-600"
                        >
                          + Connect New Account
                        </button>
                        <button
                          onClick={handleContinueWithAccount}
                          disabled={!linkedInModal.selectedAccount}
                          className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium rounded-lg transition-colors"
                        >
                          Continue
                        </button>
                      </div>
                    </div>
                  )}

                  {/* Step 1: Generate Message */}
                  {linkedInModal.step === 'generate' && (
                    <div className="text-center py-8">
                      <Linkedin className="w-16 h-16 mx-auto text-blue-600 mb-4" />
                      <h3 className="text-xl font-semibold mb-2">Ready to reach your leads on LinkedIn?</h3>
                      <p className="text-gray-600 mb-6">
                        We'll analyze your website and generate a personalized message for your target audience.
                      </p>
                      <button
                        onClick={handleGenerateMessage}
                        className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
                      >
                        Generate Message
                      </button>
                    </div>
                  )}

                  {/* Step 2: Preview & Edit Message */}
                  {linkedInModal.step === 'preview' && (
                    <>
                      <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          LinkedIn Message Preview
                        </label>
                        <textarea
                          value={linkedInModal.message}
                          onChange={(e) => setLinkedInModal({ ...linkedInModal, message: e.target.value })}
                          className="w-full h-64 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 font-mono text-sm"
                          placeholder="Message will be generated..."
                        />
                        <p className="mt-2 text-xs text-gray-500">
                          Use [First Name] as a placeholder for personalization
                        </p>
                      </div>

                      <div className="flex items-center justify-end gap-3">
                        <button
                          onClick={() => setLinkedInModal({ ...linkedInModal, step: 'generate' })}
                          className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                        >
                          Back
                        </button>
                        <button
                          onClick={handleShowLeadPreview}
                          disabled={!linkedInModal.message}
                          className="flex items-center gap-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium rounded-lg transition-colors"
                        >
                          Continue to Leads
                        </button>
                      </div>
                    </>
                  )}

                  {/* Step 3: Confirm & Send to Leads */}
                  {linkedInModal.step === 'confirm' && (
                    <>
                      <div className="mb-6">
                        <h3 className="font-semibold mb-2">Your Message:</h3>
                        <div className="bg-gray-50 p-4 rounded-lg text-sm whitespace-pre-wrap">
                          {linkedInModal.message}
                        </div>
                      </div>

                      <div className="mb-6">
                        <h3 className="font-semibold mb-2">Target Leads ({linkedInModal.leads.length} with LinkedIn profiles):</h3>
                        {linkedInModal.leads.length > 0 ? (
                          <div className="bg-gray-50 rounded-lg p-3 max-h-64 overflow-y-auto">
                            <div className="space-y-2">
                              {linkedInModal.leads.map((lead: any, index: number) => (
                                <div key={index} className="flex items-start gap-3 p-2 bg-white rounded border border-gray-200">
                                  <div className="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-semibold">
                                    {lead.first_name?.[0] || 'L'}{lead.last_name?.[0] || ''}
                                  </div>
                                  <div className="flex-1 min-w-0">
                                    <p className="text-sm font-medium text-gray-900">
                                      {lead.first_name} {lead.last_name}
                                    </p>
                                    <p className="text-xs text-gray-600">{lead.title} at {lead.company}</p>
                                    <p className="text-xs text-gray-500 truncate">{lead.email}</p>
                                    {lead.linkedin_url && (
                                      <a
                                        href={lead.linkedin_url.startsWith('http') ? lead.linkedin_url : `https://${lead.linkedin_url}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-xs text-blue-600 hover:text-blue-800 flex items-center gap-1 mt-1"
                                      >
                                        <Linkedin className="w-3 h-3" />
                                        View LinkedIn Profile
                                      </a>
                                    )}
                                  </div>
                                  <button
                                    onClick={() => setLinkedInModal({ ...linkedInModal, previewLead: lead })}
                                    className="flex-shrink-0 px-3 py-1 text-xs bg-blue-50 text-blue-600 hover:bg-blue-100 rounded transition-colors"
                                  >
                                    Preview
                                  </button>
                                </div>
                              ))}
                            </div>
                          </div>
                        ) : (
                          <p className="text-sm text-gray-600 mb-3">
                            Loading leads from {linkedInModal.campaign?.target_audience}...
                          </p>
                        )}

                        <div className="bg-blue-50 border border-blue-200 p-3 rounded-lg text-xs text-blue-800 mt-3">
                          <strong>How it works:</strong>
                          <ul className="list-disc ml-4 mt-1 space-y-1">
                            <li>If you're already connected with a lead, they'll receive a direct message</li>
                            <li>If you're not connected, they'll receive a connection request with your message as a note (max 300 characters)</li>
                          </ul>
                        </div>
                      </div>

                      <div className="flex items-center justify-end gap-3">
                        <button
                          onClick={() => setLinkedInModal({ ...linkedInModal, step: 'preview' })}
                          className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                        >
                          Back
                        </button>
                        <button
                          onClick={launchLinkedInCampaign}
                          disabled={!linkedInModal.message || linkedInModal.loading || linkedInModal.leads.length === 0}
                          className="flex items-center gap-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium rounded-lg transition-colors"
                        >
                          <Linkedin className="w-4 h-4" />
                          Confirm & Send to {linkedInModal.leads.length} Lead{linkedInModal.leads.length !== 1 ? 's' : ''}
                        </button>
                      </div>
                    </>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function StatCard({ icon, label, value, color }: {
  icon: React.ReactNode
  label: string
  value: string | number
  color: 'blue' | 'green' | 'purple' | 'orange'
}) {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600 border-blue-200',
    green: 'bg-green-50 text-green-600 border-green-200',
    purple: 'bg-purple-50 text-purple-600 border-purple-200',
    orange: 'bg-orange-50 text-orange-600 border-orange-200'
  }

  return (
    <div className={`stat-card ${colorClasses[color]}`}>
      <div className="flex items-center gap-3 mb-2">
        {icon}
        <span className="text-sm font-medium opacity-80">{label}</span>
      </div>
      <div className="text-3xl font-bold">{value}</div>
    </div>
  )
}
