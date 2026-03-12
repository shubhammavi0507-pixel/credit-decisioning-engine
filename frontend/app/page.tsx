'use client'

import { useState } from 'react'
import FileUploader from '@/components/FileUploader'
import CreditForm from '@/components/CreditForm'
import { processCredit } from '@/lib/api-client'

export default function Home() {
  const [files, setFiles] = useState<File[]>([])
  const [companyInfo, setCompanyInfo] = useState({
    company_name: '',
    industry: '',
    location: ''
  })
  const [processing, setProcessing] = useState(false)
  const [result, setResult] = useState(null)

  const handleSubmit = async () => {
    setProcessing(true)
    try {
      const result = await processCredit(files, companyInfo)
      setResult(result)
    } catch (error) {
      console.error('Error processing credit:', error)
    } finally {
      setProcessing(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-3xl font-bold mb-6">Create New Credit Case</h2>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-xl font-semibold mb-4">Company Information</h3>
        <CreditForm 
          companyInfo={companyInfo}
          onChange={setCompanyInfo}
        />
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-xl font-semibold mb-4">Upload Documents</h3>
        <FileUploader 
          files={files}
          onChange={setFiles}
        />
      </div>

      <button
        onClick={handleSubmit}
        disabled={processing || files.length === 0}
        className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400"
      >
        {processing ? 'Processing...' : 'Analyze Credit'}
      </button>

      {result && (
        <div className="mt-6 bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4">Analysis Complete</h3>
          <a 
            href={`/credit-case/${result.case_id}`}
            className="text-blue-600 hover:underline"
          >
            View Credit Decision →
          </a>
        </div>
      )}
    </div>
  )
}
