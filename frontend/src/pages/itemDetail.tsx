// src/pages/itemDetail.tsx
import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { Card, CardContent } from "@/components/ui/card"
import { formatNumber } from "@/utils/formatData"

type ItemDetail = {
  id: number
  sku: string
  uom: string
  cost: number
  type: string
  description: string
  details: string
}

export default function ItemDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [item, setItem] = useState<ItemDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchItem() {
      try {
        const res = await fetch(`http://localhost:8000/items/${id}`)
        if (!res.ok) throw new Error("Failed to fetch item details")
        const data = await res.json()
        setItem(data)
      } catch (err: any) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    if (id) fetchItem()
  }, [id])

  if (loading) return <p className="p-6 text-green-700">Loading item...</p>
  if (error) return <p className="p-6 text-red-600">Error: {error}</p>
  if (!item) return <p className="p-6 text-brown-700">Item not found</p>

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <Card className="shadow-md">
        <CardContent className="p-6 space-y-4">
          <h1 className="text-3xl font-bold text-green-700">
            {item.sku}
          </h1>
          {item.description && (
            <p className="text-brown-700">{item.description}</p>
          )}

          <div className="grid grid-cols-2 gap-4 pt-4">
            <div>
              <span className="font-semibold text-brown-900">Cost:</span>{" "}
              ${formatNumber(item.cost, 2, false)}
            </div>
            <div>
              <span className="font-semibold text-brown-900">Type:</span>{" "}
              {item.type}
            </div>
            <div>
              <span className="font-semibold text-brown-900">Details:</span>{" "}
              {item.details}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
