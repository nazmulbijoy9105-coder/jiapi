import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { LogIn, Mail, Lock, Eye, EyeOff, Scale } from 'lucide-react'

function Login() {
  const [showPassword, setShowPassword] = useState(false)
  const [isLogin, setIsLogin] = useState(true)

  return (
    <div className="min-h-screen flex items-center justify-center bg-dark-900">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-primary-600 rounded-xl flex items-center justify-center mx-auto mb-4">
            <Scale className="text-white" size={32} />
          </div>
          <h1 className="text-2xl font-bold text-white">JIAPI</h1>
          <p className="text-dark-400 mt-1">Justice & Income API</p>
        </div>

        <div className="card">
          <h2 className="text-xl font-bold text-dark-900 text-center mb-6">
            {isLogin ? 'Sign In' : 'Create Account'}
          </h2>

          <form className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-dark-700 mb-1">Email</label>
              <div className="relative">
                <Mail size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-dark-400" />
                <input 
                  type="email" 
                  placeholder="you@example.com"
                  className="input-field pl-10"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-dark-700 mb-1">Password</label>
              <div className="relative">
                <Lock size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-dark-400" />
                <input 
                  type={showPassword ? 'text' : 'password'}
                  placeholder="••••••••"
                  className="input-field pl-10 pr-10"
                />
                <button 
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-dark-400"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {!isLogin && (
              <div>
                <label className="block text-sm font-medium text-dark-700 mb-1">Organization</label>
                <input 
                  type="text" 
                  placeholder="Your firm or company"
                  className="input-field"
                />
              </div>
            )}

            <button type="submit" className="w-full btn-primary py-3">
              <LogIn size={18} className="inline mr-2" />
              {isLogin ? 'Sign In' : 'Create Account'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-dark-500">
              {isLogin ? "Don't have an account?" : "Already have an account?"}
              <button 
                onClick={() => setIsLogin(!isLogin)}
                className="ml-1 text-primary-600 font-medium hover:text-primary-700"
              >
                {isLogin ? 'Sign Up' : 'Sign In'}
              </button>
            </p>
          </div>

          <div className="mt-6 pt-6 border-t border-dark-200">
            <p className="text-xs text-dark-500 text-center">
              Free tier includes 100 requests/day. Upgrade anytime.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
