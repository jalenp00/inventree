import { Link } from "react-router-dom"

export function Navbar() {
  return (
    <header className="bg-green-700 text-white shadow-md">
      {/* content wrapper with padding */}
      <div className="flex items-center justify-between px-6 py-3">
        {/* Logo */}
        <header className="px-20 py-6">
            <Link to="/home" className="text-2xl font-bold">Inventree</Link>
        </header>

        {/* Navigation */}
        <nav className="flex gap-7">
          <Link to="/inventory" className="hover:text-brown-300">Inventory</Link>
          <Link to="/inventory" className="hover:text-brown-300">Sales</Link>
          <Link to="/suppliers" className="hover:text-brown-300">Suppliers</Link>
        </nav>
      </div>
    </header>
  )
}

