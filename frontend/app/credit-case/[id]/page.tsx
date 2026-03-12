'use client'

import {useEffect,useState} from "react"
import {useParams} from "next/navigation"
import {getCreditCase} from "@/lib/api-client"
import CAMViewer from "@/components/CAMViewer"
import DecisionDisplay from "@/components/DecisionDisplay"

export default function Page(){

const params=useParams()
const id=params.id

const [data,setData]=useState<any>(null)

useEffect(()=>{

async function load(){
const res=await getCreditCase(id)
setData(res)
}

load()

},[id])

if(!data) return <div>Loading...</div>

return(

<div className="space-y-6">

<DecisionDisplay decision={data.ml_decision}/>

<CAMViewer cam={data.cam?.full_document || ""}/>

</div>

)

}
