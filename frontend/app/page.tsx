import Link from 'next/link'
import { Zap, Target, TrendingUp, Mail } from 'lucide-react'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <nav className="flex justify-between items-center mb-16">
          <div className="text-2xl font-bold text-primary-600">
            ⚡ Vibe Marketing
          </div>
          <div className="space-x-4">
            {/* Temporarily removed Clerk auth - using direct links */}
            <Link href="/dashboard">
              <button className="btn-secondary">Dashboard</button>
            </Link>
            <Link href="/dashboard/new-campaign">
              <button className="btn-primary">Get Started</button>
            </Link>
          </div>
        </nav>

        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-6xl font-bold text-gray-900 mb-6">
            Cold Outreach,
            <span className="text-primary-600"> Automated</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Paste your URL, define your audience, and watch AI build + launch your cold email campaign in minutes.
          </p>
          <div className="flex justify-center gap-4">
            <Link href="/dashboard/new-campaign">
              <button className="btn-primary text-lg px-8 py-3">
                Start Free Campaign
              </button>
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mt-24">
          <FeatureCard
            icon={<Zap className="w-8 h-8 text-primary-600" />}
            title="AI-Powered Copy"
            description="Generate 3 A/B tested email variants instantly with GPT-4"
          />
          <FeatureCard
            icon={<Target className="w-8 h-8 text-primary-600" />}
            title="Smart Targeting"
            description="Upload leads or connect to Clay/Apollo for automatic enrichment"
          />
          <FeatureCard
            icon={<Mail className="w-8 h-8 text-primary-600" />}
            title="Instantly Integration"
            description="Campaigns launch directly in Instantly.ai with warmup"
          />
          <FeatureCard
            icon={<TrendingUp className="w-8 h-8 text-primary-600" />}
            title="Real-Time Analytics"
            description="Track opens, clicks, replies, and booked calls in one dashboard"
          />
        </div>

        {/* How It Works */}
        <div className="mt-24">
          <h2 className="text-4xl font-bold text-center mb-12">
            Launch in 3 Steps
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <StepCard
              number="1"
              title="Paste Your URL"
              description="Enter your product URL and describe your target audience (e.g., 'SaaS founders, 1-10 employees')"
            />
            <StepCard
              number="2"
              title="AI Writes Copy"
              description="GPT-4 generates 3 email variants with personalized subject lines and CTAs"
            />
            <StepCard
              number="3"
              title="Campaign Launches"
              description="System creates campaign in Instantly.ai, uploads leads, and starts sending"
            />
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-24 text-center bg-primary-600 rounded-2xl p-12 text-white">
          <h2 className="text-4xl font-bold mb-4">
            Ready to automate your outreach?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Join indie founders who've booked 100+ meetings on autopilot
          </p>
          <Link href="/dashboard/new-campaign">
            <button className="bg-white text-primary-600 hover:bg-gray-100 font-semibold py-3 px-8 rounded-lg text-lg transition-colors duration-200">
              Create Your First Campaign
            </button>
          </Link>
        </div>

        {/* Temporary Notice */}
        <div className="mt-12 text-center">
          <div className="inline-block bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-sm text-yellow-800">
              <strong>Demo Mode:</strong> Authentication temporarily disabled for testing.
              Add your Clerk API keys to <code className="bg-yellow-100 px-2 py-1 rounded">.env.local</code> to enable sign-up.
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="card hover:shadow-xl transition-shadow duration-200">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

function StepCard({ number, title, description }: { number: string; title: string; description: string }) {
  return (
    <div className="text-center">
      <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-600 text-white text-2xl font-bold rounded-full mb-4">
        {number}
      </div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}
