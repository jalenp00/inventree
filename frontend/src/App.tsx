import { Button } from "@/components/ui/button"
import { Navbar } from "@/components/global/Navbar"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Routes, Route } from "react-router-dom"
import { motion } from "framer-motion"

import Inventory from "@/pages/inventory"
import Home from "@/pages/home"
import ItemDetail from "@/pages/itemDetail"

export default function App() {
  return (
    <div className="h-screen flex flex-col bg-white text-brown-900">
      {/* Navbar */}
      <Navbar />

      {/* Hero Section */}
      <main className="flex-1 flex flex-col">
        <Routes>
          <Route path="/home" element={<Home />} />
          <Route path="/inventory" element={<Inventory />} />
          <Route path="items/:id" element={<ItemDetail />} />
        </Routes>
      </main>

      {/* Footer */}
      <footer className="flex bg-brown-900 justify-center text-black text-center">
        <p>&copy; {new Date().getFullYear()} Your App. All rights reserved.</p>
      </footer>
    </div>
  )
}