import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { motion } from "framer-motion"

export default function App() {
  return (
    <>
        <section className="flex flex-col items-center justify-center text-center px-6 py-24 bg-gradient-to-br from-green-600 to-green-800 text-white">
            <motion.h1
            className="text-5xl font-extrabold mb-4 drop-shadow-lg"
            initial={{ opacity: 0, y: -40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            >
            Welcome to <span className="text-brown-200">Inventree</span>
            </motion.h1>
            <motion.p
            className="text-lg max-w-2xl mb-6 text-green-100"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            >
            Listings, orders, inventory and metrics all in one place.
            </motion.p>
            <Button className="bg-brown-700 hover:bg-brown-800 text-white rounded-xl px-6 py-3 shadow-lg">
            Get Started
            </Button>
        </section>

        {/* Features Section */}
        <section className="py-20 px-6 bg-white text-brown-900">
            <h2 className="text-3xl font-bold text-center mb-12">Why Choose Us?</h2>
            <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
                { title: "Fast", desc: "Optimized with Vite for blazing fast performance." },
                { title: "Modern", desc: "Built with React, Tailwind, and shadcn components." },
                { title: "Beautiful", desc: "Clean UI with green, white, and brown theme." },
            ].map((feature, i) => (
                <motion.div
                key={i}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.2 }}
                >
                <Card className="rounded-2xl border-green-200 shadow-md hover:shadow-lg transition">
                    <CardContent className="p-6">
                    <h3 className="text-xl font-semibold text-green-700 mb-2">
                        {feature.title}
                    </h3>
                    <p className="text-brown-700">{feature.desc}</p>
                    </CardContent>
                </Card>
                </motion.div>
            ))}
            </div>
        </section>
    </>
  )
}