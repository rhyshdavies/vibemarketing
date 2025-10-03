'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import axios from 'axios'
import Link from 'next/link'
import { ArrowLeft, Loader2, ExternalLink } from 'lucide-react'

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
  supersearch_list_id?: string
}

interface Lead {
  email: string
  first_name?: string
  last_name?: string
  company_name?: string
  title?: string
  linkedin?: string
  location?: string
}

export default function CampaignDetailPage() {
  const params = useParams()
  const campaignId = params.id as string

  const [campaign, setCampaign] = useState<Campaign | null>(null)
  const [leads, setLeads] = useState<Lead[]>([])
  const [loading, setLoading] = useState(true)
  const [leadsLoading, setLeadsLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    loadCampaign()
  }, [campaignId])

  const loadCampaign = async () => {
    try {
      setLoading(true)
      // For now, we'll fetch from the campaigns list and find the one
      const response = await axios.get(`${API_URL}/api/campaigns`, {
        params: { user_id: 'demo_user_123' }
      })

      const foundCampaign = response.data.campaigns.find(
        (c: Campaign) => c.campaign_id === campaignId
      )

      if (foundCampaign) {
        setCampaign(foundCampaign)

        // Try to load leads if we have a list ID
        if (foundCampaign.supersearch_list_id) {
          loadLeads(foundCampaign.supersearch_list_id)
        }
      } else {
        setError('Campaign not found')
      }
    } catch (err) {
      console.error('Error loading campaign:', err)
      setError('Failed to load campaign')
    } finally {
      setLoading(false)
    }
  }

  const loadLeads = async (listId: string) => {
    try {
      setLeadsLoading(true)
      const response = await axios.get(`${API_URL}/api/leads/${listId}`)

      if (response.data.success && response.data.leads) {
        setLeads(response.data.leads)
      }
    } catch (err) {
      console.error('Error loading leads:', err)
    } finally {
      setLeadsLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    )
  }

  if (error || !campaign) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container mx-auto px-4">
          <div className="card text-center py-12">
            <p className="text-red-600 mb-4">{error || 'Campaign not found'}</p>
            <Link href="/dashboard">
              <button className="btn-primary">Back to Dashboard</button>
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        {/* Header */}
        <div className="mb-6">
          <Link href="/dashboard">
            <button className="text-gray-600 hover:text-gray-900 flex items-center gap-2 mb-4">
              <ArrowLeft className="w-5 h-5" />
              Back to Dashboard
            </button>
          </Link>
          <h1 className="text-3xl font-bold mb-2">Campaign Details</h1>
          <p className="text-gray-600">{campaign.url}</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <p className="text-sm text-gray-600 mb-1">Sent</p>
            <p className="text-3xl font-bold">{campaign.sent || 0}</p>
          </div>
          <div className="card">
            <p className="text-sm text-gray-600 mb-1">Open Rate</p>
            <p className="text-3xl font-bold text-green-600">{campaign.open_rate || 0}%</p>
          </div>
          <div className="card">
            <p className="text-sm text-gray-600 mb-1">Click Rate</p>
            <p className="text-3xl font-bold text-blue-600">{campaign.click_rate || 0}%</p>
          </div>
          <div className="card">
            <p className="text-sm text-gray-600 mb-1">Reply Rate</p>
            <p className="text-3xl font-bold text-purple-600">{campaign.reply_rate || 0}%</p>
          </div>
        </div>

        {/* Campaign Info */}
        <div className="card mb-8">
          <h2 className="text-xl font-semibold mb-4">Campaign Information</h2>
          <div className="space-y-3">
            <div>
              <span className="text-gray-600">Target Audience:</span>
              <p className="font-medium text-gray-900">{campaign.target_audience}</p>
            </div>
            <div>
              <span className="text-gray-600">Status:</span>
              <span className={`ml-2 px-3 py-1 rounded-full text-sm font-medium ${
                campaign.status === 'active'
                  ? 'bg-green-100 text-green-700'
                  : 'bg-gray-100 text-gray-700'
              }`}>
                {campaign.status}
              </span>
            </div>
            <div>
              <span className="text-gray-600">Created:</span>
              <p className="font-medium text-gray-900">{new Date(campaign.created_at).toLocaleString()}</p>
            </div>
            <div>
              <span className="text-gray-600">Campaign ID:</span>
              <p className="font-mono text-sm text-gray-900">{campaign.campaign_id}</p>
            </div>
            {campaign.supersearch_list_id && (
              <div>
                <span className="text-gray-600">Lead List ID:</span>
                <p className="font-mono text-sm text-gray-900">{campaign.supersearch_list_id}</p>
              </div>
            )}
          </div>

          {/* View in Instantly */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <a
              href={`https://app.instantly.ai/app/campaigns/${campaign.campaign_id}`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary inline-flex items-center gap-2"
            >
              View Campaign in Instantly
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
        </div>

        {/* Leads Section */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Leads ({leads.length})</h2>
            <a
              href="https://app.instantly.ai/app/lead-finder"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-700 flex items-center gap-2 text-sm"
            >
              View All in Instantly
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>

          {!campaign.supersearch_list_id ? (
            <div className="text-center py-12">
              <p className="text-gray-500 mb-2">No lead list associated with this campaign</p>
              <p className="text-sm text-gray-400">This campaign was created before lead tracking was implemented</p>
            </div>
          ) : leadsLoading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
            </div>
          ) : leads.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="border-b border-gray-200">
                    <tr className="text-left">
                      <th className="pb-3 font-semibold text-gray-900">Name</th>
                      <th className="pb-3 font-semibold text-gray-900">Email</th>
                      <th className="pb-3 font-semibold text-gray-900">Company</th>
                      <th className="pb-3 font-semibold text-gray-900">Title</th>
                      <th className="pb-3 font-semibold text-gray-900">Location</th>
                    </tr>
                  </thead>
                  <tbody>
                    {leads.map((lead, index) => (
                      <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
                        <td className="py-4">
                          <div className="font-medium text-gray-900">{lead.first_name} {lead.last_name}</div>
                          {lead.linkedin && (
                            <a
                              href={lead.linkedin}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-xs text-primary-600 hover:underline"
                            >
                              LinkedIn →
                            </a>
                          )}
                        </td>
                        <td className="py-4">
                          <a href={`mailto:${lead.email}`} className="text-primary-600 hover:underline">
                            {lead.email}
                          </a>
                        </td>
                        <td className="py-4 text-gray-900">{lead.company_name || '-'}</td>
                        <td className="py-4 text-gray-900">{lead.title || '-'}</td>
                        <td className="py-4 text-sm text-gray-600">{lead.location || '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500 mb-2">Leads are being enriched</p>
                <p className="text-sm text-gray-400">Check back in 2-5 minutes or view in Instantly dashboard</p>
                <p className="text-xs text-gray-400 mt-2">List ID: {campaign.supersearch_list_id}</p>
              </div>
            )}
        </div>
      </div>
    </div>
  )
}
