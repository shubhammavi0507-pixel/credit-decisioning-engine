'use client'

import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'

interface FileUploaderProps {
  files: File[]
  onChange: (files: File[]) => void
}

export default function FileUploader({ files, onChange }: FileUploaderProps) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    onChange([...files, ...acceptedFiles])
  }, [files, onChange])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    }
  })

  const removeFile = (index: number) => {
    const newFiles = [...files]
    newFiles.splice(index, 1)
    onChange(newFiles)
  }

  return (
    <div>
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}`}
      >
        <input {...getInputProps()} />
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        <p className="mt-2 text-sm text-gray-600">
          {isDragActive
            ? 'Drop the files here...'
            : 'Drag & drop PDF files here, or click to select'}
        </p>
      </div>

      {files.length > 0 && (
        <ul className="mt-4 space-y-2">
          {files.map((file, index) => (
            <li key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
              <span className="text-sm">{file.name}</span>
              <button
                onClick={() => removeFile(index)}
                className="text-red-500 hover:text-red-700"
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
