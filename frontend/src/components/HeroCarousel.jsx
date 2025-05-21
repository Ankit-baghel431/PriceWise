import { useState, useEffect } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";

const carouselItems = [
  {
    id: 1,
    title: "Fashion Flash Sales",
    description: "Top brands, incredible discounts, limited time only",
    image:
      "https://storage.pixteller.com/designs/designs-images/2020-12-21/04/gym-fashion-final-sale-banner-1-5fe0b6ef9d952.png",
    color: "bg-purple-100",
  },
  {
    id: 2,
    title: "Discover Amazing Tech Deals",
    description: "Find the latest gadgets at unbeatable prices",
    image:
      "https://i.pcmag.com/imagery/articles/00JPvvhfkY1XHmRFByCAqok-6..v1737141667.jpg",
    color: "bg-blue-100",
  },
  {
    id: 3,
    title: "Home & Kitchen Essentials",
    description: "Transform your space with the best deals on home products",
    image: "https://www.mealime.com/images/kitchen.jpg",
    color: "bg-amber-100",
  },
];

function HeroCarousel() {
  const [currentSlide, setCurrentSlide] = useState(0);

  const nextSlide = () => {
    setCurrentSlide((prev) =>
      prev === carouselItems.length - 1 ? 0 : prev + 1
    );
  };

  const prevSlide = () => {
    setCurrentSlide((prev) =>
      prev === 0 ? carouselItems.length - 1 : prev - 1
    );
  };

  useEffect(() => {
    const interval = setInterval(() => {
      nextSlide();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative overflow-hidden">
      <div
        className="flex transition-transform duration-500 ease-out h-[350px] md:h-[350px]"
        style={{ transform: `translateX(-${currentSlide * 100}%)` }}
      >
        {carouselItems.map((item) => (
          <div
            key={item.id}
            className={`flex-shrink-0 w-full flex flex-col md:flex-row items-center ${item.color}`}
          >
            <div className="w-full md:w-1/2 p-8 md:p-16 flex flex-col justify-center">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                {item.title}
              </h2>
              <p className="text-lg md:text-xl mb-6">{item.description}</p>
              <Button className="w-fit">Shop Now</Button>
            </div>
            <div className="w-full md:w-1/2 relative h-[200px] md:h-full">
              <img
                src={item.image}
                alt={item.title}
                className="object-cover w-full h-full"
              />
            </div>
          </div>
        ))}
      </div>

      <Button
        variant="outline"
        size="icon"
        className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white rounded-full"
        onClick={prevSlide}
      >
        <ChevronLeft className="h-6 w-6" />
      </Button>

      <Button
        variant="outline"
        size="icon"
        className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white rounded-full"
        onClick={nextSlide}
      >
        <ChevronRight className="h-6 w-6" />
      </Button>

      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
        {carouselItems.map((_, index) => (
          <button
            key={index}
            className={`w-3 h-3 rounded-full ${
              index === currentSlide ? "bg-primary" : "bg-gray-300"
            }`}
            onClick={() => setCurrentSlide(index)}
          />
        ))}
      </div>
    </div>
  );
}
export default HeroCarousel;
