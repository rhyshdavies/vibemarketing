'use client'

import { useState, useRef } from 'react'
// Temporarily disabled Clerk for testing
// import { useUser } from '@clerk/nextjs'
import axios from 'axios'
import toast from 'react-hot-toast'
import { Loader2, Sparkles, Check, X, ArrowLeft, AlertTriangle, DollarSign } from 'lucide-react'
import Link from 'next/link'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface CopyVariant {
  subject: string
  body: string
}

interface Lead {
  email: string
  first_name?: string
  last_name?: string
  company?: string
  title?: string
  website?: string
}

interface ProgressStep {
  step: number
  status: 'pending' | 'in_progress' | 'completed'
  message: string
  log?: string
}

interface ConfirmationModal {
  isOpen: boolean
  title: string
  message: string
  estimatedCost?: string
  inputLabel?: string
  inputPlaceholder?: string
  inputType?: 'number' | 'text'
  inputValue?: string
  confirmText: string
  onConfirm: () => void
  onCancel: () => void
}

interface LeadListModal {
  isOpen: boolean
  leads: Lead[]
  onConfirm: () => void
  onCancel: () => void
}

export default function CampaignForm() {
  // Temporary: Using mock user for testing
  const user = { id: 'demo_user_123' }
  const [campaignName, setCampaignName] = useState('')
  const [url, setUrl] = useState('')
  const [targetAudience, setTargetAudience] = useState('')
  const [leadCount, setLeadCount] = useState('3')
  const [senderName, setSenderName] = useState('')
  const [loading, setLoading] = useState(false)
  const [generatedCopy, setGeneratedCopy] = useState<CopyVariant[]>([])
  const [previewCopy, setPreviewCopy] = useState<CopyVariant[]>([])
  const [debugLogs, setDebugLogs] = useState<string[]>([])
  const [completedSteps, setCompletedSteps] = useState<ProgressStep[]>([])
  const [step, setStep] = useState<'input' | 'loading' | 'review' | 'success'>('input')
  const [campaignId, setCampaignId] = useState('')
  const [progressSteps, setProgressSteps] = useState<ProgressStep[]>([
    { step: 1, status: 'pending', message: 'Generate AI-powered email copy' },
    { step: 2, status: 'pending', message: 'Search Instantly database for REAL leads' },
    { step: 3, status: 'pending', message: 'Create campaign in Instantly.ai' },
    { step: 4, status: 'pending', message: 'Activate campaign' },
    { step: 5, status: 'pending', message: 'Save to database' },
  ])
  const readerRef = useRef<ReadableStreamDefaultReader<Uint8Array> | null>(null)
  const abortControllerRef = useRef<AbortController | null>(null)

  // Confirmation modal state
  const [confirmationModal, setConfirmationModal] = useState<ConfirmationModal | null>(null)

  // Lead list modal state
  const [leadListModal, setLeadListModal] = useState<LeadListModal>({
    isOpen: false,
    leads: [],
    onConfirm: () => {},
    onCancel: () => {}
  })
  const [leadListId, setLeadListId] = useState('')

  const updateProgressStep = (stepNum: number, status: 'in_progress' | 'completed', message?: string, log?: string) => {
    setProgressSteps(prev => prev.map(s =>
      s.step === stepNum
        ? { ...s, status, message: message || s.message, log: log || s.log }
        : s
    ))
  }

  const handleStop = () => {
    // Cancel the fetch request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }
    // Cancel the stream reader
    if (readerRef.current) {
      readerRef.current.cancel()
    }
    setLoading(false)
    setStep('input')
    toast.error('Campaign creation cancelled')
  }

  const showGenerateCopyConfirmation = () => {
    if (!url || !targetAudience || !senderName) {
      toast.error('Please fill in all fields')
      return
    }

    setConfirmationModal({
      isOpen: true,
      title: '⚠️ Generate Campaign & Scrape Leads',
      message: `This will:\n• Generate AI email copy (OpenAI API cost)\n• Search for ${leadCount} lead${parseInt(leadCount) !== 1 ? 's' : ''} from Instantly database\n• Create a campaign in Instantly.ai`,
      estimatedCost: 'Est. $0.10 - $5.00 depending on lead count',
      confirmText: 'Generate Campaign',
      onConfirm: () => {
        setConfirmationModal(null)
        handleGenerateCopy()
      },
      onCancel: () => setConfirmationModal(null)
    })
  }

  const handleGenerateCopy = async () => {
    setLoading(true)
    setStep('loading')
    setPreviewCopy([])
    setDebugLogs([])

    // Reset progress steps
    setProgressSteps([
      { step: 1, status: 'pending', message: 'Generate AI-powered email copy' },
      { step: 2, status: 'pending', message: 'Search Instantly database for REAL leads' },
      { step: 3, status: 'pending', message: 'Create campaign in Instantly.ai' },
      { step: 4, status: 'pending', message: 'Activate campaign' },
      { step: 5, status: 'pending', message: 'Save to database' },
    ])

    // Create new abort controller
    abortControllerRef.current = new AbortController()

    try {
      // Use fetch with streaming for Server-Sent Events
      const response = await fetch(`${API_URL}/api/create-campaign-stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          campaign_name: campaignName,
          url,
          target_audience: targetAudience,
          sender_name: senderName,
          lead_count: parseInt(leadCount) || 3,
          user_id: user?.id || 'demo_user_123',
        }),
        signal: abortControllerRef.current.signal,
      })

      if (!response.ok || !response.body) {
        throw new Error('Failed to start campaign creation')
      }

      const reader = response.body.getReader()
      readerRef.current = reader
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6))

            // Log ALL incoming data for debugging
            const timestamp = new Date().toLocaleTimeString()
            setDebugLogs(prev => [...prev, `[${timestamp}] ${JSON.stringify(data, null, 2)}`])

            // Capture supersearch_list_id from step 2
            if (data.supersearch_list_id) {
              setLeadListId(data.supersearch_list_id)
            }

            if (data.step === 'done') {
              // Campaign completed successfully
              // Save completed steps for history
              setCompletedSteps([...progressSteps])
              setGeneratedCopy(data.data.variants)
              setCampaignId(data.data.campaign_id)
              setStep('review')
              setLoading(false)
              readerRef.current = null
              abortControllerRef.current = null
              toast.success('Campaign created! Review your email variants below.')
            } else if (data.step === 'awaiting_lead_confirmation') {
              // Step 3: Show lead list for confirmation
              updateProgressStep(3, 'in_progress', 'Review leads before adding to campaign', data.log)
              setLeadListId(data.data.lead_list_id)
              setLeadListModal({
                isOpen: true,
                leads: data.data.leads,
                onConfirm: async () => {
                  // User confirmed leads, continue campaign creation
                  setLeadListModal({ isOpen: false, leads: [], onConfirm: () => {}, onCancel: () => {} })
                  updateProgressStep(3, 'completed', 'Leads confirmed')

                  // Send confirmation to backend to continue
                  await fetch(`${API_URL}/api/confirm-leads`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                      session_id: data.data.session_id,
                      confirmed: true
                    })
                  })
                },
                onCancel: () => {
                  // User cancelled
                  setLeadListModal({ isOpen: false, leads: [], onConfirm: () => {}, onCancel: () => {} })
                  setLoading(false)
                  setStep('input')
                  toast.error('Campaign creation cancelled')
                  readerRef.current?.cancel()
                  abortControllerRef.current?.abort()
                }
              })
            } else if (data.step === 'error') {
              // Error occurred
              toast.error(data.message || 'Failed to create campaign')
              setLoading(false)
              setStep('input')
              readerRef.current = null
              abortControllerRef.current = null
            } else if (typeof data.step === 'number') {
              // Progress update
              updateProgressStep(data.step, data.status, data.message, data.log)

              // If step 1 is completed and variants are sent, show preview
              if (data.step === 1 && data.status === 'completed' && data.variants) {
                setPreviewCopy(data.variants)
              }
            }
          }
        }
      }

    } catch (error: any) {
      if (error.name === 'AbortError') {
        // User cancelled, already handled
        return
      }

      console.error('Error creating campaign:', error)

      // Fallback to regular POST request if streaming fails
      try {
        const response = await axios.post(`${API_URL}/api/create-campaign`, {
          url,
          target_audience: targetAudience,
          user_id: user?.id,
        })
        setGeneratedCopy(response.data.variants)
        setCampaignId(response.data.campaign_id)
        setStep('review')
        toast.success('Campaign created! Review your email variants below.')
      } catch (err: any) {
        console.error('Fallback error:', err)
        toast.error(err.response?.data?.detail || 'Failed to create campaign')
        setStep('input')
      } finally {
        setLoading(false)
        readerRef.current = null
        abortControllerRef.current = null
      }
    }
  }

  const showLaunchConfirmation = () => {
    setConfirmationModal({
      isOpen: true,
      title: '🚀 Launch Campaign',
      message: 'This will ACTIVATE your campaign and start sending emails immediately!\n\n⚠️ This action will:\n• Activate the campaign in Instantly.ai\n• Start sending emails to leads\n• Incur email sending costs',
      estimatedCost: 'Est. $10 - $50/month depending on volume',
      confirmText: 'Yes, Launch Campaign',
      onConfirm: () => {
        setConfirmationModal(null)
        handleLaunch()
      },
      onCancel: () => setConfirmationModal(null)
    })
  }

  const handleLaunch = () => {
    setStep('success')
    toast.success('Campaign launched! Check your Instantly.ai account.')
  }

  if (step === 'loading') {
    return (
      <div className="card max-w-2xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold mb-2">Creating Your Campaign</h2>
            <p className="text-gray-600">
              Please wait while we set up your automated email campaign...
            </p>
          </div>
          <Link href="/dashboard">
            <button className="text-gray-500 hover:text-gray-700">
              <ArrowLeft className="w-6 h-6" />
            </button>
          </Link>
        </div>

        <div className="space-y-4">
          {progressSteps.map((progressStep) => (
            <div
              key={progressStep.step}
              className={`flex items-start gap-4 p-4 rounded-lg border-2 transition-all ${
                progressStep.status === 'completed'
                  ? 'bg-green-50 border-green-200'
                  : progressStep.status === 'in_progress'
                  ? 'bg-blue-50 border-blue-200'
                  : 'bg-gray-50 border-gray-200'
              }`}
            >
              <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-semibold ${
                progressStep.status === 'completed'
                  ? 'bg-green-500 text-white'
                  : progressStep.status === 'in_progress'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-300 text-gray-600'
              }`}>
                {progressStep.status === 'completed' ? (
                  <Check className="w-5 h-5" />
                ) : progressStep.status === 'in_progress' ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  progressStep.step
                )}
              </div>
              <div className="flex-1">
                <p className={`font-medium ${
                  progressStep.status === 'in_progress' ? 'text-blue-900' :
                  progressStep.status === 'completed' ? 'text-green-900' :
                  'text-gray-700'
                }`}>
                  {progressStep.message}
                </p>
                {progressStep.status === 'in_progress' && (
                  <p className="text-sm text-blue-600 mt-1">In progress...</p>
                )}
                {progressStep.status === 'completed' && (
                  <p className="text-sm text-green-600 mt-1">✓ Completed</p>
                )}
                {progressStep.log && (
                  <div className="mt-2 p-3 bg-gray-900 rounded text-xs text-green-400 font-mono whitespace-pre-wrap border border-gray-700 max-h-40 overflow-y-auto">
                    <div className="text-gray-500 mb-1 sticky top-0 bg-gray-900 pb-1">📋 LOG OUTPUT:</div>
                    {progressStep.log}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 flex gap-4">
          <div className="flex-1 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm text-blue-800">
              <strong>Tip:</strong> This usually takes 10-20 seconds. AI is analyzing your website and generating personalized email copy.
            </p>
          </div>
          <button
            onClick={handleStop}
            className="px-6 py-2 bg-red-100 hover:bg-red-200 text-red-700 font-semibold rounded-lg transition-colors duration-200 flex items-center gap-2"
          >
            <X className="w-5 h-5" />
            Stop
          </button>
        </div>

        {/* Email Variants Preview */}
        {previewCopy.length > 0 && (
          <div className="mt-8 border-t-4 border-green-500 pt-6">
            <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg mb-4">
              <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                ✨ AI-Generated Email Variants
                <span className="bg-green-500 text-white px-3 py-1 rounded-full text-sm">
                  {previewCopy.length} Variants
                </span>
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                These email variants have been generated by AI and are ready for A/B testing
              </p>
            </div>

            <div className="space-y-6">
              {previewCopy.map((variant, index) => (
                <div key={index} className="border-2 border-green-200 rounded-xl p-6 bg-white shadow-lg hover:shadow-xl transition-shadow">
                  <div className="flex items-center justify-between mb-4">
                    <span className="bg-gradient-to-r from-green-500 to-blue-500 text-white px-4 py-2 rounded-full text-sm font-bold flex items-center gap-2">
                      📧 Variant {index + 1}
                    </span>
                    <div className="text-xs text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                      {variant.body.length} characters
                    </div>
                  </div>

                  <div className="mb-4 bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
                    <label className="block text-xs font-bold text-yellow-800 mb-2 uppercase tracking-wide">
                      📬 Subject Line
                    </label>
                    <div className="text-base font-semibold text-gray-900">
                      {variant.subject}
                    </div>
                  </div>

                  <div className="bg-gray-50 border-l-4 border-blue-400 p-4 rounded">
                    <label className="block text-xs font-bold text-blue-800 mb-2 uppercase tracking-wide">
                      ✉️ Email Body
                    </label>
                    <div className="text-sm text-gray-800 whitespace-pre-wrap leading-relaxed max-h-64 overflow-y-auto font-sans">
                      {variant.body.replace(/\[Your Name\]/g, senderName)}
                    </div>
                  </div>

                  <div className="mt-4 flex gap-2 text-xs text-gray-500">
                    <span className="bg-blue-100 px-2 py-1 rounded">
                      {variant.subject.length} char subject
                    </span>
                    <span className="bg-green-100 px-2 py-1 rounded">
                      {variant.body.split('\n').length} lines
                    </span>
                    <span className="bg-purple-100 px-2 py-1 rounded">
                      {variant.body.split(/\s+/).length} words
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Debug Panel - Raw API Responses */}
        {debugLogs.length > 0 && (
          <div className="mt-8 border-t-4 border-purple-500 pt-6">
            <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-lg mb-4">
              <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                🔍 Debug Console - Raw API Data
                <span className="bg-purple-500 text-white px-3 py-1 rounded-full text-sm">
                  {debugLogs.length} Events
                </span>
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                All server-sent events and API responses in real-time
              </p>
            </div>
            <div className="bg-black text-green-400 p-4 rounded-lg font-mono text-xs overflow-x-auto max-h-96 overflow-y-auto border-2 border-purple-300">
              {debugLogs.map((log, index) => (
                <div key={index} className="mb-4 pb-4 border-b border-gray-800 last:border-0">
                  <pre className="whitespace-pre-wrap">{log}</pre>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    )
  }

  if (step === 'success') {
    return (
      <div className="card max-w-2xl mx-auto text-center">
        <div className="mb-6">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-green-100 rounded-full mb-4">
            <span className="text-4xl">🎉</span>
          </div>
          <h2 className="text-3xl font-bold mb-2">Campaign Launched!</h2>
          <p className="text-gray-600">
            Your campaign is now live in Instantly.ai and emails are being sent.
          </p>
        </div>

        <div className="bg-gray-50 rounded-lg p-6 mb-6">
          <div className="grid grid-cols-2 gap-4 text-left">
            <div>
              <p className="text-sm text-gray-500">Campaign ID</p>
              <p className="font-semibold">{campaignId}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Status</p>
              <p className="font-semibold text-green-600">Active</p>
            </div>
          </div>
        </div>

        <div className="flex gap-4 justify-center">
          <a href={`/dashboard/campaigns/${campaignId}`}>
            <button className="btn-primary">View Analytics</button>
          </a>
          <button
            onClick={() => {
              setStep('input')
              setUrl('')
              setTargetAudience('')
              setGeneratedCopy([])
              setCampaignId('')
            }}
            className="btn-secondary"
          >
            Create Another Campaign
          </button>
        </div>
      </div>
    )
  }

  if (step === 'review') {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card mb-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold">Review Your Email Variants</h2>
            <Link href="/dashboard">
              <button className="text-gray-500 hover:text-gray-700 flex items-center gap-2">
                <ArrowLeft className="w-5 h-5" />
                Dashboard
              </button>
            </Link>
          </div>
          <p className="text-gray-600 mb-6">
            AI generated {generatedCopy.length} email variants for A/B testing. Review them below and launch when ready.
          </p>

          <div className="space-y-6">
            {generatedCopy.map((variant, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-6">
                <div className="flex items-center gap-2 mb-3">
                  <span className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm font-semibold">
                    Variant {index + 1}
                  </span>
                </div>
                <div className="mb-4">
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Subject Line
                  </label>
                  <div className="bg-gray-50 p-3 rounded border border-gray-200 text-gray-900 font-medium">
                    {variant.subject}
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Email Body
                  </label>
                  <div className="bg-gray-50 p-4 rounded border border-gray-200 whitespace-pre-wrap font-mono text-sm text-gray-800">
                    {variant.body}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="flex gap-4 mt-8">
            <button
              onClick={showLaunchConfirmation}
              className="btn-primary flex-1"
            >
              Launch Campaign
            </button>
            <button
              onClick={() => setStep('input')}
              className="btn-secondary"
            >
              Back
            </button>
          </div>

          {/* View Leads Button */}
          {leadListId && (
            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-semibold text-blue-900 mb-1">✅ 5 Real Leads Found</h4>
                  <p className="text-sm text-blue-700">
                    Your leads are ready in Instantly's database. Click to view them.
                  </p>
                </div>
                <a
                  href={`https://app.instantly.ai/app/lead-finder`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-primary whitespace-nowrap"
                >
                  View Leads →
                </a>
              </div>
              <p className="text-xs text-blue-600 mt-2">
                List ID: {leadListId}
              </p>
            </div>
          )}

          {/* Campaign Creation Logs - Persistent */}
          {completedSteps.length > 0 && (
            <div className="mt-8 border-t-2 border-gray-300 pt-6">
              <h3 className="text-lg font-semibold mb-4 text-gray-900">📜 Campaign Creation Log</h3>
              <div className="space-y-3">
                {completedSteps.map((step, index) => (
                  <div key={index} className="bg-gray-50 border border-gray-200 rounded-lg p-3">
                    <div className="flex items-center gap-2 mb-2">
                      <span className={`w-6 h-6 rounded-full flex items-center justify-center text-white text-xs font-bold ${
                        step.status === 'completed' ? 'bg-green-500' : 'bg-gray-400'
                      }`}>
                        {step.status === 'completed' ? '✓' : step.step}
                      </span>
                      <span className="font-medium text-sm">{step.message}</span>
                    </div>
                    {step.log && (
                      <div className="ml-8 mt-2 p-2 bg-gray-900 rounded text-xs text-green-400 font-mono whitespace-pre-wrap max-h-32 overflow-y-auto">
                        {step.log}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Debug Console - Also persistent on review page */}
          {debugLogs.length > 0 && (
            <div className="mt-8 border-t-2 border-purple-300 pt-6">
              <h3 className="text-lg font-semibold mb-4 text-gray-900 flex items-center gap-2">
                🔍 Full Debug Log
                <span className="bg-purple-500 text-white px-2 py-1 rounded-full text-xs">
                  {debugLogs.length} events
                </span>
              </h3>
              <div className="bg-black text-green-400 p-4 rounded-lg font-mono text-xs overflow-x-auto max-h-96 overflow-y-auto border-2 border-purple-300">
                {debugLogs.map((log, index) => (
                  <div key={index} className="mb-3 pb-3 border-b border-gray-800 last:border-0">
                    <pre className="whitespace-pre-wrap">{log}</pre>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    )
  }

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
            Campaign Name
          </label>
          <input
            type="text"
            value={campaignName}
            onChange={(e) => setCampaignName(e.target.value)}
            placeholder="e.g., Q1 2025 Outreach, Construction HR Campaign"
            className="input-field"
            required
          />
          <p className="text-sm text-gray-500 mt-1">
            This name will be used for your campaign and lead list in Instantly
          </p>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Your Website/App URL
          </label>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://yourapp.com"
            className="input-field"
          />
          <p className="text-sm text-gray-500 mt-1">
            The product or service you're promoting
          </p>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Target Audience (ICP)
          </label>
          <textarea
            value={targetAudience}
            onChange={(e) => setTargetAudience(e.target.value)}
            placeholder="Example: SaaS founders in US, 1-10 employees, CTOs at B2B companies"
            rows={4}
            className="input-field"
          />
          <p className="text-sm text-gray-500 mt-1">
            Describe your ideal customer profile in detail
          </p>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Number of Leads
          </label>
          <input
            type="number"
            value={leadCount}
            onChange={(e) => setLeadCount(e.target.value)}
            placeholder="3"
            min="1"
            max="100"
            className="input-field"
          />
          <p className="text-sm text-gray-500 mt-1">
            How many leads to generate from Instantly database (default: 3)
          </p>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Your Name
          </label>
          <input
            type="text"
            value={senderName}
            onChange={(e) => setSenderName(e.target.value)}
            placeholder="John Smith"
            className="input-field"
          />
          <p className="text-sm text-gray-500 mt-1">
            Name to use in email signatures (replaces [Your Name])
          </p>
        </div>

        <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
          <h3 className="font-semibold text-primary-900 mb-2">What happens next?</h3>
          <ul className="text-sm text-primary-800 space-y-1">
            <li>✓ AI generates 3 email variants with different approaches</li>
            <li>✓ Campaign is created in your Instantly.ai account</li>
            <li>✓ A/B testing is automatically set up</li>
            <li>✓ You can add leads manually or via CSV upload</li>
          </ul>
        </div>

        <button
          onClick={showGenerateCopyConfirmation}
          disabled={loading || !campaignName || !url || !targetAudience}
          className="btn-primary w-full flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Generating AI copy...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              Generate Campaign
            </>
          )}
        </button>
      </div>

      {/* Confirmation Modal */}
      {confirmationModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 animate-in fade-in zoom-in duration-200">
            <div className="flex items-start gap-4 mb-4">
              <div className="bg-yellow-100 rounded-full p-3">
                <AlertTriangle className="w-6 h-6 text-yellow-600" />
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-bold mb-2">{confirmationModal.title}</h3>
                <p className="text-gray-600 whitespace-pre-line">{confirmationModal.message}</p>
              </div>
            </div>

            {confirmationModal.estimatedCost && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4 flex items-center gap-2">
                <DollarSign className="w-5 h-5 text-blue-600" />
                <span className="text-sm text-blue-800 font-semibold">
                  {confirmationModal.estimatedCost}
                </span>
              </div>
            )}


            <div className="flex gap-3">
              <button
                onClick={confirmationModal.onCancel}
                className="btn-secondary flex-1"
              >
                Cancel
              </button>
              <button
                onClick={confirmationModal.onConfirm}
                className="btn-primary flex-1"
              >
                {confirmationModal.confirmText}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Lead List Review Modal */}
      {leadListModal.isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] flex flex-col animate-in fade-in zoom-in duration-200">
            {/* Header */}
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-2xl font-bold mb-2 flex items-center gap-2">
                📋 Review Lead List
                <span className="bg-blue-500 text-white px-3 py-1 rounded-full text-sm">
                  {leadListModal.leads.length} leads
                </span>
              </h3>
              <p className="text-gray-600">
                Review the scraped leads before adding them to your campaign. You can confirm or cancel.
              </p>
            </div>

            {/* Lead List Table */}
            <div className="flex-1 overflow-y-auto p-6">
              <div className="border border-gray-200 rounded-lg overflow-hidden">
                <table className="w-full">
                  <thead className="bg-gray-50 border-b border-gray-200">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">#</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Email</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Name</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Company</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Title</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {leadListModal.leads.map((lead, index) => (
                      <tr key={index} className="hover:bg-gray-50">
                        <td className="px-4 py-3 text-sm text-gray-500">{index + 1}</td>
                        <td className="px-4 py-3 text-sm font-medium text-gray-900">{lead.email}</td>
                        <td className="px-4 py-3 text-sm text-gray-700">
                          {lead.first_name || lead.last_name
                            ? `${lead.first_name || ''} ${lead.last_name || ''}`.trim()
                            : '-'}
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-700">{lead.company || '-'}</td>
                        <td className="px-4 py-3 text-sm text-gray-700">{lead.title || '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Footer with Actions */}
            <div className="p-6 border-t border-gray-200 bg-gray-50">
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4 flex items-start gap-3">
                <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                <div className="text-sm text-yellow-800">
                  <strong>Confirm to proceed:</strong> These leads will be added to your Instantly.ai campaign.
                  Make sure you have permission to contact them.
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={leadListModal.onCancel}
                  className="btn-secondary flex-1"
                >
                  ❌ Cancel Campaign
                </button>
                <button
                  onClick={leadListModal.onConfirm}
                  className="btn-primary flex-1 bg-green-600 hover:bg-green-700"
                >
                  ✅ Confirm & Add Leads
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
