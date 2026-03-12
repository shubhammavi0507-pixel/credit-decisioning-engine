interface Props{
cam:string
}

export default function CAMViewer({cam}:Props){

return(

<div className="bg-gray-50 p-6 rounded-lg whitespace-pre-wrap font-mono text-sm">
{cam}
</div>

)
}
