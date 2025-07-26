interface Alert {
  type: string
  severity: string
  message: string
  timestamp: string
}

export default function AlertCard({ alert }: { alert: Alert }) {
  const severityColors = {
    low: 'bg-blue-50 border-blue-200 text-blue-800',
    medium: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    high: 'bg-red-50 border-red-200 text-red-800',
  }

  const severityIcons = {
    low: 'ℹ️',
    medium: '⚠️',
    high: '🚨',
  }

  return (
    <div className={`
      p-4 rounded-lg border
      ${severityColors[alert.severity as keyof typeof severityColors]}
    `}>
      <div className="flex items-start gap-3">
        <span className="text-2xl">
          {severityIcons[alert.severity as keyof typeof severityIcons]}
        </span>
        <div className="flex-1">
          <p className="font-medium">{alert.message}</p>
          <p className="text-sm opacity-75 mt-1">
            {new Date(alert.timestamp).toLocaleString()}
          </p>
        </div>
      </div>
    </div>
  )
}