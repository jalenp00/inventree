// src/pages/items.tsx
import { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { formatNumber } from "@/utils/formatData"
import { Link } from "react-router-dom"

type InventoryItem = {
  item_id: number
  sku: number
  on_hand: string
  allocated: string
  incoming: string
  reorder_point: string | null
  reorder_to: string | null
  backordered: string
  available: string
  available_to_build: string | null
}

export default function Items() {
  const [items, setItems] = useState<InventoryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchInventory() {
      try {
        const res = await fetch("http://localhost:8000/inventory/") // adjust URL if needed
        if (!res.ok) throw new Error("Failed to fetch inventory")
        const data = await res.json()
        setItems(data)
      } catch (err: any) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    fetchInventory()
  }, [])

  if (loading) return <p className="p-6 text-green-700">Loading inventory...</p>
  if (error) return <p className="p-6 text-red-600">Error: {error}</p>

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-green-700 mb-6">Inventory</h1>

      <Card className="overflow-x-auto shadow-md">
        <CardContent className="p-0">
          <table className="min-w-full border-collapse">
            <thead className="bg-brown-900 text-black">
              <tr>
                <th className="px-4 py-2 text-left">SKU</th>
                <th className="px-4 py-2 text-left">On Hand</th>
                <th className="px-4 py-2 text-left">Allocated</th>
                <th className="px-4 py-2 text-left">Incoming</th>
                <th className="px-4 py-2 text-left">Reorder Point</th>
                <th className="px-4 py-2 text-left">Reorder To</th>
                <th className="px-4 py-2 text-left">Backordered</th>
                <th className="px-4 py-2 text-left">Available</th>
                <th className="px-4 py-2 text-left">Available to Build</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr
                  key={item.item_id}
                  className="odd:bg-white even:bg-green-50 hover:bg-green-100 transition"
                >
                  <td className="px-4 py-2">
                    <Link to={`/items/${item.item_id}`} className="hover:underline">
                        {item.sku}
                    </Link>
                    </td>
                  <td className="px-4 py-2">{formatNumber(item.on_hand)}</td>
                  <td className="px-4 py-2">{formatNumber(item.allocated)}</td>
                  <td className="px-4 py-2">{formatNumber(item.incoming)}</td>
                  <td className="px-4 py-2">{formatNumber(item.reorder_point) ?? "-"}</td>
                  <td className="px-4 py-2">{formatNumber(item.reorder_to) ?? "-"}</td>
                  <td className="px-4 py-2">{formatNumber(item.backordered)}</td>
                  <td className="px-4 py-2">{formatNumber(item.available)}</td>
                  <td className="px-4 py-2">{formatNumber(item.available_to_build) ?? "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  )
}
