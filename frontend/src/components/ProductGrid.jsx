import { useState } from "react";
import { Star, Heart } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";

// Mock product data
const mockProducts = [
  {
    id: 1,
    name: "Wireless Noise Cancelling Headphones",
    image:
      "https://cdn.thewirecutter.com/wp-content/media/2025/01/BEST-WIRELESS-BLUETOOTH-EARBUDS-2048px-5969-2x1-1.jpg?width=2048&quality=75&crop=2:1&auto=webp",
    description: "Premium sound quality with active noise cancellation",
    price: 199.99,
    originalPrice: 249.99,
    rating: 4.5,
    store: "Flipkart",
    storeimage:
      "https://seeklogo.com/images/F/flipkart-logo-3F33927DAA-seeklogo.com.png",
    discount: 20,
  },
  {
    id: 2,
    name: "Smart Fitness Watch",
    image:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ18BNFxSZm472eb5pbdWc0ZNzFHTxSp6HWXQ&s",
    description: "Track your fitness goals with this advanced smartwatch",
    price: 149.99,
    originalPrice: 179.99,
    rating: 4.2,
    store: "Flipkart",
    storeimage:
      "https://seeklogo.com/images/F/flipkart-logo-3F33927DAA-seeklogo.com.png",
    discount: 17,
  },
  {
    id: 3,
    name: 'Ultra HD 4K Smart TV - 55"',
    image:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRd0rKoVwBcfkTEpPnCqCqt0G7WJ7e89fNqIg&s",
    description: "Crystal clear picture quality with smart features",
    price: 499.99,
    originalPrice: 699.99,
    rating: 4.7,
    store: "Flipkart",
    storeimage:
      "https://seeklogo.com/images/F/flipkart-logo-3F33927DAA-seeklogo.com.png",
    discount: 29,
  },
  {
    id: 4,
    name: "Professional Blender",
    image:
      "https://hips.hearstapps.com/hmg-prod/images/ghk-digital-testing-immersionblenders-179-webres-1668457330.jpg?crop=1.00xw:0.752xh;0,0.149xh&resize=1200:*",
    description: "High-performance blender for smoothies and more",
    price: 89.99,
    originalPrice: 129.99,
    rating: 4.3,
    store: "Flipkart",
    storeimage:
      "https://seeklogo.com/images/F/flipkart-logo-3F33927DAA-seeklogo.com.png",
    discount: 31,
  },
  {
    id: 5,
    name: "Ergonomic Office Chair",
    image:
      "https://cdn.thewirecutter.com/wp-content/media/2024/11/cheapgamingchairs-2048px-00096.jpg?auto=webp&quality=75&width=1024",
    description: "Comfortable seating for long work hours",
    price: 199.99,
    originalPrice: 249.99,
    rating: 4.6,
    store: "Flipkart",
    storeimage:
      "https://seeklogo.com/images/F/flipkart-logo-3F33927DAA-seeklogo.com.png",
    discount: 20,
  },
  {
    id: 6,
    name: "Smartphone - Latest Model",
    image:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTIO7fTUd5jc377Iuz_z3-quj-zc74KH9SfCA&s",
    description: "Cutting-edge technology in the palm of your hand",
    price: 799.99,
    originalPrice: 899.99,
    rating: 4.8,
    store: "Flipkart",
    storeimage:
      "https://seeklogo.com/images/F/flipkart-logo-3F33927DAA-seeklogo.com.png",
    discount: 11,
  },
];

function ProductGrid() {
  const [favorites, setFavorites] = useState([]);

  const toggleFavorite = (id) => {
    setFavorites((prev) =>
      prev.includes(id) ? prev.filter((favId) => favId !== id) : [...prev, id]
    );
  };

  return (
    <div>
      <h3 className="text-2xl font-bold mb-6">Popular Deals</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockProducts.map((product) => (
          <Card
            key={product.id}
            className="overflow-hidden hover:shadow-lg transition-shadow"
          >
            <CardHeader className="p-0 relative">
              <div className="relative h-48 w-full">
                <img
                  src={product.image || "/placeholder.svg"}
                  alt={product.name}
                  className="h-full w-full"
                />
              </div>
              <Badge className="absolute top-2 right-2 bg-red-500">
                {product.discount}% OFF
              </Badge>
              <Button
                variant="ghost"
                size="icon"
                className="absolute top-2 left-2 bg-white/80 hover:bg-white rounded-full"
                onClick={() => toggleFavorite(product.id)}
              >
                <Heart
                  className={`h-5 w-5 ${
                    favorites.includes(product.id)
                      ? "fill-red-500 text-red-500"
                      : ""
                  }`}
                />
              </Button>
            </CardHeader>
            <CardContent className="p-4">
              <div className="flex items-center mb-2">
                <div className="w-6 h-6 relative mr-2">
                  <img
                    src={product.storeimage || "/placeholder.svg"}
                    alt={product.store}
                    fill
                    className="object-contain rounded-full"
                  />
                </div>
                <span className="text-sm text-gray-500">{product.store}</span>
              </div>
              <h3 className="font-semibold text-lg line-clamp-1">
                {product.name}
              </h3>
              <p className="text-gray-500 text-sm line-clamp-2 h-10 mb-2">
                {product.description}
              </p>
              <div className="flex items-center mb-2">
                <div className="flex items-center">
                  <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                  <span className="ml-1 text-sm">{product.rating}</span>
                </div>
              </div>
              <div className="flex items-baseline">
                <span className="text-xl font-bold">${product.price}</span>
                <span className="ml-2 text-sm text-gray-500 line-through">
                  ${product.originalPrice}
                </span>
              </div>
            </CardContent>
            <CardFooter className="p-4 pt-0">
              <Button className="w-full">View Deal</Button>
            </CardFooter>
          </Card>
        ))}
      </div>
      <div className="mt-8 text-center">
        <Button variant="outline" className="mx-auto">
          Load More Deals
        </Button>
      </div>
    </div>
  );
}
export default ProductGrid;
