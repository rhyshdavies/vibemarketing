'use client'

import { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'
import { Loader2, Sparkles, Check, ArrowLeft, AlertTriangle, RefreshCw, Edit2, ChevronRight, ChevronLeft } from 'lucide-react'
import Link from 'next/link'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface ICP {
  name: string
  description: string
  target_audience: string
  pain_points: string[]
  company_size: string
}

interface Lead {
  email: string
  first_name?: string
  last_name?: string
  company_name?: string
  title?: string
  website?: string
  location?: string
}

interface EmailVariant {
  subject: string
  body: string
}

interface DFYDomain {
  domain: string
  score: number
  reasoning: string
  suggested_use: string
}

interface EmailAccount {
  email: string
  first_name: string
  last_name: string
  status: number
  warmup_status: number
}

export default function ICPCampaignFlow() {
  const user = { id: 'demo_user_123' }

  // Form state
  const [url, setUrl] = useState('')
  const [campaignName, setCampaignName] = useState('')
  const [senderName, setSenderName] = useState('')
  const [leadCount, setLeadCount] = useState(10)

  // Flow state
  const [currentStep, setCurrentStep] = useState(1)
  const [loading, setLoading] = useState(false)

  // Step 1: ICPs
  const [suggestedICPs, setSuggestedICPs] = useState<ICP[]>([])
  const [selectedICP, setSelectedICP] = useState<ICP | null>(null)

  // Step 2: Leads
  const [enrichmentId, setEnrichmentId] = useState('')
  const [leads, setLeads] = useState<Lead[]>([])
  const [pollingLeads, setPollingLeads] = useState(false)

  // Step 3: Emails
  const [emailVariants, setEmailVariants] = useState<EmailVariant[]>([])
  const [editingVariant, setEditingVariant] = useState<number | null>(null)
  const [editedVariants, setEditedVariants] = useState<EmailVariant[]>([])

  // Step 4: Domains
  const [dfyDomains, setDfyDomains] = useState<DFYDomain[]>([])
  const [existingAccounts, setExistingAccounts] = useState<EmailAccount[]>([])
  const [selectedDomains, setSelectedDomains] = useState<string[]>([])
  const [selectedAccounts, setSelectedAccounts] = useState<string[]>([])

  // Step 5: Campaign creation
  const [campaignCreating, setCampaignCreating] = useState(false)
  const [campaignId, setCampaignId] = useState('')
  const [creationLogs, setCreationLogs] = useState<string[]>([])

  const resetFlow = () => {
    setCurrentStep(1)
    setUrl('')
    setCampaignName('')
    setSenderName('')
    setLeadCount(10)
    setSuggestedICPs([])
    setSelectedICP(null)
    setEnrichmentId('')
    setLeads([])
    setEmailVariants([])
    setEditedVariants([])
    setDfyDomains([])
    setExistingAccounts([])
    setSelectedDomains([])
    setSelectedAccounts([])
    setCampaignId('')
    setCreationLogs([])
  }

  // Step 1: Analyze URL for ICPs
  const analyzeURL = async () => {
    if (!url) {
      toast.error('Please enter a website URL')
      return
    }

    setLoading(true)
    try {
      // Use longer timeout for GPT-5 web search analysis (3 minutes)
      const response = await axios.post(
        `${API_URL}/api/icp/analyze`,
        { url },
        { timeout: 180000 } // 3 minutes
      )
      setSuggestedICPs(response.data.icps)
      setCurrentStep(2)
      toast.success(`Found ${response.data.icps.length} ICP suggestions!`)
    } catch (error: any) {
      console.error('Error analyzing URL:', error)
      if (error.code === 'ECONNABORTED') {
        toast.error('Request timed out. The website analysis took too long. Please try again.')
      } else {
        toast.error(error.response?.data?.detail || 'Failed to analyze URL')
      }
    } finally {
      setLoading(false)
    }
  }

  // Step 2: Search for leads
  const searchLeads = async (icp: ICP) => {
    setSelectedICP(icp)
    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/api/icp/search-leads`, {
        url,
        target_audience: icp.target_audience,
        lead_count: leadCount
      })

      setEnrichmentId(response.data.enrichment_id)
      toast.success('Lead search started! Waiting for results...')

      // Start polling for leads
      pollForLeads(response.data.enrichment_id)
    } catch (error: any) {
      console.error('Error searching leads:', error)
      toast.error(error.response?.data?.detail || 'Failed to search for leads')
      setLoading(false)
    }
  }

  const pollForLeads = async (enrichmentId: string) => {
    setPollingLeads(true)
    const maxAttempts = 24 // 120 seconds total (2 minutes)
    let attempts = 0

    const poll = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/icp/leads/${enrichmentId}?limit=${leadCount}`)

        // Check if we got enriched leads
        if (response.data.success && response.data.leads.length > 0) {
          setLeads(response.data.leads)
          setPollingLeads(false)
          setLoading(false)
          setCurrentStep(3)
          toast.success(`Found ${response.data.leads.length} enriched leads!`)
          return
        }

        // Check if enrichment is in progress
        if (!response.data.success && response.data.enriching_count > 0) {
          attempts++
          console.log(`Enrichment in progress: ${response.data.enriching_count} leads found, waiting for emails... (attempt ${attempts}/${maxAttempts})`)

          if (attempts < maxAttempts) {
            setTimeout(poll, 5000) // Poll every 5 seconds
            return
          }
        }

        // No leads found and max attempts reached
        attempts++
        if (attempts < maxAttempts) {
          setTimeout(poll, 5000)
        } else {
          setPollingLeads(false)
          setLoading(false)
          toast.error('Lead enrichment is taking longer than expected. The leads are being created in Instantly - you can continue to email generation and they will be ready.')
          // Still proceed to next step even if enrichment isn't complete
          setCurrentStep(3)
        }
      } catch (error) {
        console.error('Error polling for leads:', error)
        attempts++
        if (attempts < maxAttempts) {
          setTimeout(poll, 5000)
        } else {
          setPollingLeads(false)
          setLoading(false)
          toast.error('Failed to fetch leads')
        }
      }
    }

    poll()
  }

  // Step 3: Generate emails
  const generateEmails = async () => {
    if (!selectedICP) return

    setLoading(true)
    try {
      const response = await axios.post(`${API_URL}/api/icp/generate-emails`, {
        url,
        selected_icp: selectedICP
      })

      setEmailVariants(response.data.variants)
      setEditedVariants(response.data.variants)
      setCurrentStep(4)
      toast.success('Email variants generated!')
    } catch (error: any) {
      console.error('Error generating emails:', error)
      toast.error(error.response?.data?.detail || 'Failed to generate emails')
    } finally {
      setLoading(false)
    }
  }

  const regenerateVariant = async (index: number) => {
    if (!selectedICP) return

    setLoading(true)
    try {
      const response = await axios.post(`${API_URL}/api/icp/regenerate-email`, {
        url,
        selected_icp: selectedICP,
        variant_index: index
      })

      const newVariants = [...editedVariants]
      newVariants[index] = response.data.variant
      setEditedVariants(newVariants)
      toast.success(`Variant ${index + 1} regenerated!`)
    } catch (error: any) {
      console.error('Error regenerating variant:', error)
      toast.error(error.response?.data?.detail || 'Failed to regenerate variant')
    } finally {
      setLoading(false)
    }
  }

  // Step 4: Match DFY domains and get existing accounts
  const matchDomains = async () => {
    setLoading(true)
    try {
      console.log('🔍 Calling match-domains API...')
      const response = await axios.post(`${API_URL}/api/icp/match-domains`, { url })
      console.log('📊 API Response:', response.data)
      console.log('📧 Existing accounts:', response.data.existing_accounts?.length || 0)

      setDfyDomains(response.data.matched_domains || [])
      setExistingAccounts(response.data.existing_accounts || [])

      console.log('✅ State updated - existingAccounts should have:', response.data.existing_accounts?.length || 0)

      setCurrentStep(5)

      const dfyCount = response.data.matched_domains?.length || 0
      const accountCount = response.data.existing_accounts?.length || 0
      toast.success(`Found ${dfyCount} DFY domains and ${accountCount} existing accounts!`)
    } catch (error: any) {
      console.error('Error matching domains:', error)
      toast.error(error.response?.data?.detail || 'Failed to match domains')
    } finally {
      setLoading(false)
    }
  }

  const toggleDomain = (domain: string) => {
    setSelectedDomains(prev =>
      prev.includes(domain)
        ? prev.filter(d => d !== domain)
        : [...prev, domain]
    )
  }

  const toggleAccount = (email: string) => {
    setSelectedAccounts(prev =>
      prev.includes(email)
        ? prev.filter(e => e !== email)
        : [...prev, email]
    )
  }

  // Step 5: Create campaign
  const createCampaign = async () => {
    if (!campaignName) {
      toast.error('Please enter a campaign name')
      return
    }

    setCampaignCreating(true)
    setCreationLogs([])

    try {
      const response = await fetch(`${API_URL}/api/icp/create-campaign`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          campaign_name: campaignName,
          url,
          user_id: user.id,
          selected_icp: selectedICP,
          enrichment_id: enrichmentId,
          lead_count: leads.length,
          approved_variants: editedVariants,
          selected_domains: selectedDomains,
          selected_accounts: selectedAccounts,  // Send selected email accounts
          sender_name: senderName
        })
      })

      if (!response.ok || !response.body) {
        throw new Error('Failed to create campaign')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6))

            if (data.step === 'done' && data.status === 'success') {
              setCampaignId(data.data.campaign_id)
              setCurrentStep(6)
              toast.success('Campaign created successfully!')
            } else if (data.status === 'error') {
              toast.error(data.message)
            } else if (data.message) {
              setCreationLogs(prev => [...prev, data.message])
            }
          }
        }
      }
    } catch (error: any) {
      console.error('Error creating campaign:', error)
      toast.error('Failed to create campaign')
    } finally {
      setCampaignCreating(false)
    }
  }

  // Render different steps
  if (currentStep === 1) {
    return (
      <div className="card max-w-2xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <Sparkles className="w-8 h-8 text-primary-600" />
            <h2 className="text-2xl font-bold">Create New Campaign</h2>
          </div>
          <Link href="/dashboard">
            <button className="text-gray-500 hover:text-gray-700 flex items-center gap-2">
              <ArrowLeft className="w-5 h-5" />
              Dashboard
            </button>
          </Link>
        </div>

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Your Website URL
            </label>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://yourapp.com"
              className="input-field"
              required
            />
            <p className="text-sm text-gray-500 mt-1">
              Enter your website to analyze and get ICP suggestions
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Number of Leads
            </label>
            <input
              type="number"
              value={leadCount}
              onChange={(e) => setLeadCount(parseInt(e.target.value) || 10)}
              min="1"
              max="100"
              className="input-field"
            />
            <p className="text-sm text-gray-500 mt-1">
              How many leads to find (recommended: 10-50)
            </p>
          </div>

          <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
            <h3 className="font-semibold text-primary-900 mb-2">What happens next?</h3>
            <ul className="text-sm text-primary-800 space-y-1">
              <li>✓ AI analyzes your website</li>
              <li>✓ Suggests 10 ideal customer profiles (ICPs)</li>
              <li>✓ You pick the best ICP</li>
              <li>✓ We find matching leads automatically</li>
              <li>✓ Generate and approve email variants</li>
              <li>✓ Select DFY email domains</li>
              <li>✓ Launch your campaign!</li>
            </ul>
          </div>

          <button
            onClick={analyzeURL}
            disabled={loading || !url}
            className="btn-primary w-full flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Analyzing website...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                Analyze & Get ICPs
              </>
            )}
          </button>
        </div>
      </div>
    )
  }

  if (currentStep === 2) {
    return (
      <div className="card max-w-4xl mx-auto">
        <div className="mb-6">
          <button onClick={() => setCurrentStep(1)} className="text-primary-600 hover:text-primary-700 mb-4 flex items-center gap-2">
            <ChevronLeft className="w-4 h-4" />
            Back
          </button>
          <h2 className="text-2xl font-bold">Select Your Ideal Customer Profile</h2>
          <p className="text-gray-600 mt-2">Choose the ICP that best matches your target audience</p>
        </div>

        <div className="space-y-4">
          {suggestedICPs.map((icp, index) => (
            <div
              key={index}
              className="border-2 border-gray-200 rounded-lg p-6 hover:border-primary-500 transition-all cursor-pointer"
              onClick={() => searchLeads(icp)}
            >
              <div className="flex items-start justify-between mb-3">
                <h3 className="text-xl font-bold text-gray-900">{icp.name}</h3>
                <span className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm">
                  {icp.company_size}
                </span>
              </div>
              <p className="text-gray-700 mb-4">{icp.description}</p>
              <div className="mb-4">
                <p className="text-sm font-semibold text-gray-600 mb-2">Target Audience:</p>
                <p className="text-sm text-gray-700">{icp.target_audience}</p>
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-600 mb-2">Pain Points:</p>
                <ul className="text-sm text-gray-700 space-y-1">
                  {icp.pain_points.map((pain, idx) => (
                    <li key={idx}>• {pain}</li>
                  ))}
                </ul>
              </div>
              <div className="mt-4 flex justify-end">
                <button className="btn-primary flex items-center gap-2">
                  Select This ICP
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>

        {loading && (
          <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-center gap-3">
            <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
            <div>
              <p className="font-semibold text-blue-900">Searching for leads...</p>
              <p className="text-sm text-blue-700">This may take up to 90 seconds</p>
            </div>
          </div>
        )}
      </div>
    )
  }

  if (currentStep === 3) {
    return (
      <div className="card max-w-4xl mx-auto">
        <div className="mb-6">
          <h2 className="text-2xl font-bold">Review Found Leads</h2>
          <p className="text-gray-600 mt-2">
            Found {leads.length} leads matching <span className="font-semibold">{selectedICP?.name}</span>
          </p>
        </div>

        <div className="border border-gray-200 rounded-lg overflow-hidden mb-6">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">#</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Name</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Email</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Company</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Title</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Location</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {leads.map((lead, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm text-gray-900">{index + 1}</td>
                  <td className="px-4 py-3 text-sm font-medium text-gray-900">
                    {lead.first_name} {lead.last_name}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-900">{lead.email}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{lead.company_name || '-'}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{lead.title || '-'}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{lead.location || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="flex gap-4">
          <button onClick={() => setCurrentStep(2)} className="btn-secondary">
            Back to ICPs
          </button>
          <button onClick={generateEmails} disabled={loading} className="btn-primary flex-1 flex items-center justify-center gap-2">
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Generating emails...
              </>
            ) : (
              <>
                Continue to Email Generation
                <ChevronRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>
    )
  }

  if (currentStep === 4) {
    return (
      <div className="card max-w-4xl mx-auto">
        <div className="mb-6">
          <h2 className="text-2xl font-bold">Review & Edit Email Variants</h2>
          <p className="text-gray-600 mt-2">Approve, edit, or regenerate each email variant</p>
        </div>

        <div className="space-y-6 mb-6">
          {editedVariants.map((variant, index) => (
            <div key={index} className="border-2 border-gray-200 rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <span className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm font-semibold">
                  Variant {index + 1}
                </span>
                <div className="flex gap-2">
                  <button
                    onClick={() => regenerateVariant(index)}
                    disabled={loading}
                    className="text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1"
                  >
                    <RefreshCw className="w-4 h-4" />
                    Regenerate
                  </button>
                  <button
                    onClick={() => setEditingVariant(editingVariant === index ? null : index)}
                    className="text-sm text-gray-600 hover:text-gray-700 flex items-center gap-1"
                  >
                    <Edit2 className="w-4 h-4" />
                    Edit
                  </button>
                </div>
              </div>

              {editingVariant === index ? (
                <>
                  <div className="mb-4">
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Subject</label>
                    <input
                      type="text"
                      value={variant.subject}
                      onChange={(e) => {
                        const newVariants = [...editedVariants]
                        newVariants[index].subject = e.target.value
                        setEditedVariants(newVariants)
                      }}
                      className="input-field"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Body</label>
                    <textarea
                      value={variant.body}
                      onChange={(e) => {
                        const newVariants = [...editedVariants]
                        newVariants[index].body = e.target.value
                        setEditedVariants(newVariants)
                      }}
                      rows={10}
                      className="input-field font-mono text-sm"
                    />
                  </div>
                </>
              ) : (
                <>
                  <div className="mb-4 bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
                    <label className="block text-xs font-bold text-yellow-800 mb-2">SUBJECT</label>
                    <div className="text-base font-semibold text-gray-900">{variant.subject}</div>
                  </div>
                  <div className="bg-gray-50 border-l-4 border-blue-400 p-4 rounded">
                    <label className="block text-xs font-bold text-blue-800 mb-2">BODY</label>
                    <div className="text-sm whitespace-pre-wrap text-gray-900">{variant.body}</div>
                  </div>
                </>
              )}
            </div>
          ))}
        </div>

        <div className="flex gap-4">
          <button onClick={() => setCurrentStep(3)} className="btn-secondary">
            Back to Leads
          </button>
          <button onClick={matchDomains} disabled={loading} className="btn-primary flex-1 flex items-center justify-center gap-2">
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Finding domains...
              </>
            ) : (
              <>
                Continue to Domain Selection
                <ChevronRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>
    )
  }

  if (currentStep === 5) {
    console.log('🎨 Rendering Step 5')
    console.log('📧 existingAccounts state:', existingAccounts.length)
    console.log('🌐 dfyDomains state:', dfyDomains.length)

    return (
      <div className="card max-w-4xl mx-auto">
        <div className="mb-6">
          <h2 className="text-2xl font-bold">Select Email Accounts</h2>
          <p className="text-gray-600 mt-2">Choose DFY domains or use your existing email accounts</p>
        </div>

        {/* Existing Email Accounts Section */}
        {existingAccounts.length > 0 && (
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Your Existing Email Accounts ({existingAccounts.length})
            </h3>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {existingAccounts.map((account, index) => (
                <div
                  key={index}
                  onClick={() => toggleAccount(account.email)}
                  className={`border-2 rounded-lg p-4 cursor-pointer transition-all ${
                    selectedAccounts.includes(account.email)
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      checked={selectedAccounts.includes(account.email)}
                      onChange={() => {}}
                      className="w-5 h-5"
                    />
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-gray-900">{account.email}</span>
                        {account.warmup_status === 1 && (
                          <span className="bg-green-100 text-green-700 px-2 py-0.5 rounded text-xs font-medium">
                            Warmed Up
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-gray-600">
                        {account.first_name} {account.last_name}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* DFY Domains Section */}
        {dfyDomains.length > 0 ? (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Pre-Warmed DFY Domains ({dfyDomains.length})
            </h3>
            <div className="space-y-4">
              {dfyDomains.map((domain, index) => (
                <div
                  key={index}
                  onClick={() => toggleDomain(domain.domain)}
                  className={`border-2 rounded-lg p-6 cursor-pointer transition-all ${
                    selectedDomains.includes(domain.domain)
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <input
                        type="checkbox"
                        checked={selectedDomains.includes(domain.domain)}
                        onChange={() => {}}
                        className="w-5 h-5"
                      />
                      <div>
                        <h3 className="text-lg font-bold text-gray-900">{domain.domain}</h3>
                        <span className="text-sm text-gray-600">{domain.suggested_use}</span>
                      </div>
                    </div>
                    <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">
                      Score: {domain.score}/100
                    </span>
                  </div>
                  <p className="text-sm text-gray-700">{domain.reasoning}</p>
                </div>
              ))}
            </div>
          </div>
        ) : existingAccounts.length === 0 ? (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
            <div className="flex gap-3">
              <AlertTriangle className="w-6 h-6 text-blue-600 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-blue-900 font-semibold mb-2">No email accounts or DFY domains available</p>
                <p className="text-blue-800 text-sm mb-2">
                  You can still create the campaign and manually configure accounts later in Instantly.
                </p>
              </div>
            </div>
          </div>
        ) : null}

        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-2">Campaign Name</label>
          <input
            type="text"
            value={campaignName}
            onChange={(e) => setCampaignName(e.target.value)}
            placeholder="Q1 2025 Outreach"
            className="input-field"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-2">Your Name</label>
          <input
            type="text"
            value={senderName}
            onChange={(e) => setSenderName(e.target.value)}
            placeholder="John Smith"
            className="input-field"
            required
          />
        </div>

        <div className="flex gap-4">
          <button onClick={() => setCurrentStep(4)} className="btn-secondary">
            Back to Emails
          </button>
          <button
            onClick={createCampaign}
            disabled={!campaignName || campaignCreating}
            className="btn-primary flex-1 flex items-center justify-center gap-2"
          >
            {campaignCreating ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Creating campaign...
              </>
            ) : (
              <>
                Create Campaign
                <ChevronRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>

        {creationLogs.length > 0 && (
          <div className="mt-6 bg-gray-50 border border-gray-200 rounded-lg p-4">
            <h4 className="font-semibold mb-2">Progress:</h4>
            <div className="space-y-1 text-sm">
              {creationLogs.map((log, i) => (
                <div key={i} className="text-gray-700">• {log}</div>
              ))}
            </div>
          </div>
        )}
      </div>
    )
  }

  if (currentStep === 6) {
    return (
      <div className="card max-w-2xl mx-auto text-center">
        <div className="mb-6">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-green-100 rounded-full mb-4">
            <Check className="w-10 h-10 text-green-600" />
          </div>
          <h2 className="text-3xl font-bold mb-2">Campaign Created!</h2>
          <p className="text-gray-600">
            Your campaign is ready in Instantly.ai
          </p>
        </div>

        <div className="bg-gray-50 rounded-lg p-6 mb-6">
          <div className="grid grid-cols-2 gap-4 text-left">
            <div>
              <p className="text-sm text-gray-500">Campaign ID</p>
              <p className="font-semibold">{campaignId}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Leads</p>
              <p className="font-semibold">{leads.length}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Email Variants</p>
              <p className="font-semibold">{editedVariants.length}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Email Accounts</p>
              <p className="font-semibold">{selectedAccounts.length || 'None'}</p>
            </div>
          </div>
        </div>

        <div className="flex gap-4 justify-center">
          <a
            href={`https://app.instantly.ai/app/campaigns/${campaignId}`}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary"
          >
            View in Instantly.ai
          </a>
          <button onClick={resetFlow} className="btn-secondary">
            Create Another Campaign
          </button>
        </div>
      </div>
    )
  }

  return null
}
