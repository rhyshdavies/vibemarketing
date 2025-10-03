'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'
import { Loader2, Check, X, Search, ShoppingCart, Mail, DollarSign, Globe, Zap } from 'lucide-react'
import Link from 'next/link'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface PrewarmedDomain {
  name: string
  selected: boolean
}

interface EmailAccount {
  id: string
  domain: string
  email: string
  first_name: string
  last_name: string
  email_provider: number
  is_pre_warmed_up: boolean
  timestamp_created: string
  timestamp_cancelled?: string
}

interface DomainOrder {
  workspace_id: string
  domain: string
  timestamp_created: string
  forwarding_domain?: string
  is_pre_warmed_up?: boolean
  timestamp_cancelled?: string
}

interface OrderQuote {
  order_is_valid: boolean
  number_of_domains_ordered: number
  number_of_accounts_ordered: number
  price_per_account_per_month: number
  price_per_domain_per_year: number
  total_price_per_month: number
  total_price_per_year: number
  total_price: number
  total_discount: number
}

export default function DomainsPage() {
  const [activeTab, setActiveTab] = useState<'browse' | 'orders' | 'accounts'>('browse')
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')

  // Pre-warmed domains
  const [prewarmedDomains, setPrewarmedDomains] = useState<PrewarmedDomain[]>([])
  const [filteredDomains, setFilteredDomains] = useState<PrewarmedDomain[]>([])
  const [selectedDomains, setSelectedDomains] = useState<Set<string>>(new Set())

  // Orders and accounts
  const [domainOrders, setDomainOrders] = useState<DomainOrder[]>([])
  const [emailAccounts, setEmailAccounts] = useState<EmailAccount[]>([])

  // Order preview
  const [orderQuote, setOrderQuote] = useState<OrderQuote | null>(null)
  const [showOrderModal, setShowOrderModal] = useState(false)

  useEffect(() => {
    if (activeTab === 'browse') {
      loadPrewarmedDomains()
    } else if (activeTab === 'orders') {
      loadDomainOrders()
    } else if (activeTab === 'accounts') {
      loadEmailAccounts()
    }
  }, [activeTab])

  useEffect(() => {
    // Filter domains based on search
    if (searchTerm) {
      setFilteredDomains(
        prewarmedDomains.filter(d =>
          d.name.toLowerCase().includes(searchTerm.toLowerCase())
        )
      )
    } else {
      setFilteredDomains(prewarmedDomains)
    }
  }, [searchTerm, prewarmedDomains])

  const loadPrewarmedDomains = async () => {
    try {
      setLoading(true)
      const response = await axios.post(`${API_URL}/api/domains/prewarmed`, {
        extensions: ['com', 'org', 'co']
      })

      const domains = response.data.domains.map((name: string) => ({
        name,
        selected: false
      }))

      setPrewarmedDomains(domains)
      setFilteredDomains(domains)

      if (domains.length === 0) {
        toast('No pre-warmed domains available right now. Try again later!', { icon: '⚠️' })
      }
    } catch (error: any) {
      console.error('Error loading domains:', error)
      toast.error('Failed to load pre-warmed domains')
    } finally {
      setLoading(false)
    }
  }

  const loadDomainOrders = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_URL}/api/domains/orders?limit=50`)
      setDomainOrders(response.data.items || [])
    } catch (error) {
      console.error('Error loading orders:', error)
      toast.error('Failed to load domain orders')
    } finally {
      setLoading(false)
    }
  }

  const loadEmailAccounts = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_URL}/api/domains/accounts?limit=50&with_passwords=true`)
      setEmailAccounts(response.data.items || [])
    } catch (error) {
      console.error('Error loading accounts:', error)
      toast.error('Failed to load email accounts')
    } finally {
      setLoading(false)
    }
  }

  const toggleDomainSelection = (domainName: string) => {
    const newSelected = new Set(selectedDomains)
    if (newSelected.has(domainName)) {
      newSelected.delete(domainName)
    } else {
      newSelected.add(domainName)
    }
    setSelectedDomains(newSelected)
  }

  const getOrderQuote = async () => {
    if (selectedDomains.size === 0) {
      toast.error('Please select at least one domain')
      return
    }

    try {
      setLoading(true)

      // Get quote for first selected domain (can expand to multiple later)
      const domain = Array.from(selectedDomains)[0]

      const response = await axios.post(`${API_URL}/api/domains/order/prewarmed`, {
        domain,
        number_of_accounts: 1,
        simulation: true // Just get pricing
      })

      setOrderQuote(response.data)
      setShowOrderModal(true)
    } catch (error: any) {
      console.error('Error getting quote:', error)
      toast.error(error.response?.data?.detail || 'Failed to get order quote')
    } finally {
      setLoading(false)
    }
  }

  const placeOrder = async () => {
    if (!orderQuote) return

    try {
      setLoading(true)

      const domain = Array.from(selectedDomains)[0]

      const response = await axios.post(`${API_URL}/api/domains/order/prewarmed`, {
        domain,
        number_of_accounts: 1,
        simulation: false // Actually place order
      })

      if (response.data.order_placed) {
        toast.success('Order placed successfully! 🎉')
        setShowOrderModal(false)
        setSelectedDomains(new Set())
        setOrderQuote(null)

        // Refresh the domains list
        loadPrewarmedDomains()

        // Switch to orders tab
        setActiveTab('orders')
      } else {
        toast.error(response.data.order_error || 'Failed to place order')
      }
    } catch (error: any) {
      console.error('Error placing order:', error)
      toast.error(error.response?.data?.detail || 'Failed to place order')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <Link href="/dashboard">
            <button className="text-gray-600 hover:text-gray-900 mb-4">
              ← Back to Dashboard
            </button>
          </Link>
          <h1 className="text-4xl font-bold mb-2">Domain & Email Management</h1>
          <p className="text-gray-600">
            Purchase pre-warmed domains and manage your email sending accounts
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-8 border-b border-gray-200">
          <button
            onClick={() => setActiveTab('browse')}
            className={`pb-4 px-2 font-semibold transition-colors ${
              activeTab === 'browse'
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Globe className="w-5 h-5 inline mr-2" />
            Browse Pre-Warmed Domains
          </button>
          <button
            onClick={() => setActiveTab('orders')}
            className={`pb-4 px-2 font-semibold transition-colors ${
              activeTab === 'orders'
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <ShoppingCart className="w-5 h-5 inline mr-2" />
            My Orders
          </button>
          <button
            onClick={() => setActiveTab('accounts')}
            className={`pb-4 px-2 font-semibold transition-colors ${
              activeTab === 'accounts'
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Mail className="w-5 h-5 inline mr-2" />
            Email Accounts
          </button>
        </div>

        {/* Browse Tab */}
        {activeTab === 'browse' && (
          <div>
            {/* Info Banner */}
            <div className="card bg-gradient-to-r from-blue-50 to-purple-50 mb-6">
              <div className="flex items-start gap-4">
                <Zap className="w-6 h-6 text-primary-600 mt-1" />
                <div>
                  <h3 className="font-semibold text-lg mb-2">Why Pre-Warmed Domains?</h3>
                  <ul className="text-sm text-gray-700 space-y-1">
                    <li>✅ Already warmed up and ready to send</li>
                    <li>✅ Better deliverability from day one</li>
                    <li>✅ No waiting for domain reputation to build</li>
                    <li>✅ Instantly provisions Google Workspace accounts</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Search */}
            <div className="mb-6">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search domains..."
                  className="input-field pl-12"
                />
              </div>
              {/* Domain Count */}
              <div className="mt-3 text-sm text-gray-600">
                {searchTerm ? (
                  <span>Showing <strong>{filteredDomains.length}</strong> of <strong>{prewarmedDomains.length}</strong> domains</span>
                ) : (
                  <span><strong>{prewarmedDomains.length}</strong> pre-warmed domain{prewarmedDomains.length !== 1 ? 's' : ''} available</span>
                )}
              </div>
            </div>

            {loading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
              </div>
            ) : filteredDomains.length === 0 ? (
              <div className="card text-center py-12">
                <p className="text-gray-500 mb-4">
                  {searchTerm ? 'No domains match your search' : 'No pre-warmed domains available'}
                </p>
                {!searchTerm && (
                  <button onClick={loadPrewarmedDomains} className="btn-secondary">
                    Refresh
                  </button>
                )}
              </div>
            ) : (
              <>
                {/* Domain Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                  {filteredDomains.map((domain) => (
                    <div
                      key={domain.name}
                      onClick={() => toggleDomainSelection(domain.name)}
                      className={`card cursor-pointer transition-all hover:shadow-lg ${
                        selectedDomains.has(domain.name)
                          ? 'border-2 border-primary-500 bg-primary-50'
                          : 'border border-gray-200'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <p className="font-mono font-semibold text-lg text-gray-900">{domain.name}</p>
                          <p className="text-sm text-gray-500 mt-1">Pre-warmed & ready</p>
                        </div>
                        <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                          selectedDomains.has(domain.name)
                            ? 'bg-primary-600 border-primary-600'
                            : 'border-gray-300'
                        }`}>
                          {selectedDomains.has(domain.name) && (
                            <Check className="w-4 h-4 text-white" />
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Order Button */}
                {selectedDomains.size > 0 && (
                  <div className="fixed bottom-8 right-8 z-50">
                    <button
                      onClick={getOrderQuote}
                      disabled={loading}
                      className="btn-primary shadow-2xl text-lg px-8 py-4 flex items-center gap-3"
                    >
                      {loading ? (
                        <Loader2 className="w-6 h-6 animate-spin" />
                      ) : (
                        <ShoppingCart className="w-6 h-6" />
                      )}
                      Get Quote ({selectedDomains.size} domain{selectedDomains.size > 1 ? 's' : ''})
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {/* Orders Tab */}
        {activeTab === 'orders' && (
          <div>
            {loading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
              </div>
            ) : domainOrders.length === 0 ? (
              <div className="card text-center py-12">
                <p className="text-gray-500 mb-4">No domain orders yet</p>
                <button onClick={() => setActiveTab('browse')} className="btn-primary">
                  Browse Domains
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                {domainOrders.map((order, index) => (
                  <div key={index} className="card">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-mono font-semibold text-lg">{order.domain}</p>
                        <p className="text-sm text-gray-500">
                          Ordered: {new Date(order.timestamp_created).toLocaleString()}
                        </p>
                        {order.is_pre_warmed_up && (
                          <span className="inline-block mt-2 bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-semibold">
                            Pre-Warmed
                          </span>
                        )}
                      </div>
                      {order.timestamp_cancelled ? (
                        <span className="bg-red-100 text-red-700 px-4 py-2 rounded-lg font-semibold">
                          Cancelled
                        </span>
                      ) : (
                        <span className="bg-green-100 text-green-700 px-4 py-2 rounded-lg font-semibold">
                          Active
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Accounts Tab */}
        {activeTab === 'accounts' && (
          <div>
            {loading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
              </div>
            ) : emailAccounts.length === 0 ? (
              <div className="card text-center py-12">
                <p className="text-gray-500 mb-4">No email accounts yet</p>
                <button onClick={() => setActiveTab('browse')} className="btn-primary">
                  Order Domains
                </button>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="border-b-2 border-gray-200">
                    <tr className="text-left">
                      <th className="pb-4 font-semibold">Email</th>
                      <th className="pb-4 font-semibold">Name</th>
                      <th className="pb-4 font-semibold">Domain</th>
                      <th className="pb-4 font-semibold">Type</th>
                      <th className="pb-4 font-semibold">Created</th>
                      <th className="pb-4 font-semibold">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {emailAccounts.map((account) => (
                      <tr key={account.id} className="border-b border-gray-100">
                        <td className="py-4">
                          <p className="font-mono font-semibold">{account.email}</p>
                        </td>
                        <td className="py-4">
                          {account.first_name} {account.last_name}
                        </td>
                        <td className="py-4">{account.domain}</td>
                        <td className="py-4">
                          {account.is_pre_warmed_up ? (
                            <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-semibold">
                              Pre-Warmed
                            </span>
                          ) : (
                            <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-semibold">
                              Custom
                            </span>
                          )}
                        </td>
                        <td className="py-4 text-sm text-gray-600">
                          {new Date(account.timestamp_created).toLocaleDateString()}
                        </td>
                        <td className="py-4">
                          {account.timestamp_cancelled ? (
                            <span className="text-red-600 font-semibold">Cancelled</span>
                          ) : (
                            <span className="text-green-600 font-semibold">Active</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* Order Modal */}
        {showOrderModal && orderQuote && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-8">
                <h2 className="text-3xl font-bold mb-6">Order Summary</h2>

                <div className="space-y-6">
                  {/* Domain Info */}
                  <div className="bg-gray-50 rounded-lg p-6">
                    <h3 className="font-semibold mb-4">Domain</h3>
                    <p className="font-mono text-xl">{Array.from(selectedDomains)[0]}</p>
                    <p className="text-sm text-gray-600 mt-2">
                      {orderQuote.number_of_accounts_ordered} email account(s)
                    </p>
                  </div>

                  {/* Pricing */}
                  <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
                    <h3 className="font-semibold mb-4 flex items-center gap-2">
                      <DollarSign className="w-5 h-5" />
                      Pricing Breakdown
                    </h3>

                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-gray-700">Domain (per year)</span>
                        <span className="font-semibold">${orderQuote.price_per_domain_per_year}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-700">Email accounts (per month)</span>
                        <span className="font-semibold">${orderQuote.price_per_account_per_month}</span>
                      </div>

                      {orderQuote.total_discount > 0 && (
                        <div className="flex justify-between text-green-600">
                          <span>Discount</span>
                          <span className="font-semibold">-${orderQuote.total_discount}</span>
                        </div>
                      )}

                      <div className="border-t-2 border-gray-300 pt-3 mt-3">
                        <div className="flex justify-between text-lg">
                          <span className="font-bold">Due Today</span>
                          <span className="font-bold text-primary-600 text-2xl">
                            ${orderQuote.total_price}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mt-2">
                          Then ${orderQuote.total_price_per_month}/month
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* What's Included */}
                  <div className="bg-green-50 rounded-lg p-6">
                    <h3 className="font-semibold mb-3">✅ What's Included</h3>
                    <ul className="space-y-2 text-sm text-gray-700">
                      <li>• Pre-warmed domain with good reputation</li>
                      <li>• Google Workspace email account</li>
                      <li>• Ready to send emails immediately</li>
                      <li>• Full integration with Instantly.ai</li>
                      <li>• Automatic domain configuration</li>
                    </ul>
                  </div>

                  {/* Buttons */}
                  <div className="flex gap-4">
                    <button
                      onClick={() => {
                        setShowOrderModal(false)
                        setOrderQuote(null)
                      }}
                      className="flex-1 btn-secondary"
                      disabled={loading}
                    >
                      Cancel
                    </button>
                    <button
                      onClick={placeOrder}
                      disabled={loading}
                      className="flex-1 btn-primary flex items-center justify-center gap-2"
                    >
                      {loading ? (
                        <Loader2 className="w-5 h-5 animate-spin" />
                      ) : (
                        <Check className="w-5 h-5" />
                      )}
                      Place Order - ${orderQuote.total_price}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
