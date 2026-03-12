interface Props{
decision:any
}

export default function DecisionDisplay({decision}:Props){

return(

<div className="p-6 bg-white shadow rounded">

<h2 className="text-2xl font-bold mb-4">Credit Decision</h2>

<p><b>Approved:</b> {decision.approved ? "YES" : "NO"}</p>

<p><b>Risk Grade:</b> {decision.risk_grade}</p>

<p><b>Approval Probability:</b> {decision.approval_probability}</p>

<p><b>Credit Limit:</b> {decision.credit_limit}</p>

<p><b>Interest Rate:</b> {decision.interest_rate}%</p>

</div>

)
}
