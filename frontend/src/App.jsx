import React from "react";
import SearchBar from "./components/SearchBar";
import HeroCarousel from "./components/HeroCarousel";
import Navbar from "./components/Navbar";
import ProductGrid from "./components/ProductGrid";

function App() {
  return ( 
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main>
        <HeroCarousel />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
              Find the Best Deals Across the Web
            </h2>
            <p className="mt-4 text-xl text-gray-500">
              Search once, find the best prices from all major retailers
            </p>
            <div className="mt-8">
              <SearchBar />
            </div>
          </div>
          <ProductGrid />
        </div>
      </main>
      <footer className="bg-white">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            © {new Date().getFullYear()} DealFinder. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
