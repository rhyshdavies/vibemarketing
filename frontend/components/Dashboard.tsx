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

  const loadDashboardData = useCallback(async () => {
    try {
      setLoading(true)

      // Load campaigns
      const campaignsResponse = await axios.get(`${API_URL}/api/campaigns`, {
        params: { user_id: user.id }
      })
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
  }, [loadDashboardData])

  const handleLaunchLinkedIn = async (campaign: Campaign) => {
    try {
      // Check if LinkedIn account is connected
      const accountsResponse = await axios.get(`${API_URL}/api/linkedin/accounts`)

      if (!accountsResponse.data.has_account) {
        // Need to connect LinkedIn account first
        if (confirm('No LinkedIn account connected. Would you like to connect one now?')) {
          const authResponse = await axios.post(`${API_URL}/api/linkedin/connect`)
          if (authResponse.data.success) {
            // Redirect to Unipile hosted auth
            window.location.href = authResponse.data.auth_url
          }
        }
        return
      }

      // Launch LinkedIn campaign
      if (confirm(`Launch LinkedIn campaign for ${campaign.url}? This will send LinkedIn messages to the campaign's leads.`)) {
        const response = await axios.post(`${API_URL}/api/linkedin/launch-campaign`, {
          campaign_id: campaign.campaign_id,
          user_id: user.id
        })

        if (response.data.success) {
          alert(`LinkedIn campaign launched successfully! Sent ${response.data.sent_count} messages.`)
          loadDashboardData() // Refresh dashboard
        } else if (response.data.needs_auth) {
          alert(response.data.message)
        }
      }
    } catch (error: any) {
      console.error('Error launching LinkedIn campaign:', error)
      alert(`Failed to launch LinkedIn campaign: ${error.response?.data?.detail || error.message}`)
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
