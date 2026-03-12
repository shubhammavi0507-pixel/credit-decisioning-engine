'use client'

interface Props {
  companyInfo: any
  onChange: (info:any)=>void
}

export default function CreditForm({companyInfo,onChange}:Props){

const update=(field:string,value:string)=>{
    onChange({...companyInfo,[field]:value})
}

return(
<div className="space-y-4">

<input
className="w-full border p-2 rounded"
placeholder="Company Name"
value={companyInfo.company_name}
onChange={(e)=>update("company_name",e.target.value)}
/>

<input
className="w-full border p-2 rounded"
placeholder="Industry"
value={companyInfo.industry}
onChange={(e)=>update("industry",e.target.value)}
/>

<input
className="w-full border p-2 rounded"
placeholder="Location"
value={companyInfo.location}
onChange={(e)=>update("location",e.target.value)}
/>

</div>
)
}
