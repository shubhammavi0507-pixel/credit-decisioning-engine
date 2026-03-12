const API_BASE_URL = "/api"

export async function processCredit(files: File[], companyInfo: any) {
  // Step 1: Upload documents
  const formData = new FormData()
  files.forEach(file => formData.append('files', file))
  
  Object.keys(companyInfo).forEach(key => {
    formData.append(key, companyInfo[key])
  })

  const uploadResponse = await fetch(`${API_BASE_URL}/api/upload`, {
    method: 'POST',
    body: formData
  })
  
  const uploadResult = await uploadResponse.json()
  const caseId = uploadResult.case_id

  // Step 2: Process documents
  await fetch(`${API_BASE_URL}/api/process/${caseId}`, {
    method: 'POST'
  })

  // Step 3: Research company
  await fetch(`${API_BASE_URL}/api/research/${caseId}`, {
    method: 'POST'
  })

  // Step 4: Make credit decision
  await fetch(`${API_BASE_URL}/api/decision/${caseId}`, {
    method: 'POST'
  })

  // Step 5: Generate CAM
  const camResponse = await fetch(`${API_BASE_URL}/api/cam/${caseId}`, {
    method: 'POST'
  })

  return await camResponse.json()
}

export async function getCreditCase(caseId: string) {
  const response = await fetch(`${API_BASE_URL}/api/case/${caseId}`)
  return await response.json()
}
