import { Link } from "react-router-dom";
import { ShoppingCart, Menu, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

function Navbar() {
  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center ">
            <Link to="/" className=" items-center">
              <span className="text-2xl font-bold text-primary">
                {/* <img
                  src="logo.png"
                  alt=""
                  className="w-[200px] bord er-2 border-amber-900"
                /> */}
                DealHunt
              </span>
            </Link>
            <nav className="hidden md:ml-8 md:flex md:space-x-8 bor der-2 border-amber-900">
              <Link
                to="/"
                className="text-gray-700 hover:text-black inline-flex items-center px-1 pt-1 text-sm font-medium"
              >
                Home
              </Link>
              <Link
                to="/categories"
                className="text-gray-700 hover:text-black inline-flex items-center px-1 pt-1 text-sm font-medium"
              >
                Categories
              </Link>
              <Link
                to="/trending"
                className="text-gray-700 hover:text-black inline-flex items-center px-1 pt-1 text-sm font-medium"
              >
                Trending
              </Link>
              <Link
                to="/deals"
                className="text-gray-700 hover:text-black inline-flex items-center px-1 pt-1 text-sm font-medium"
              >
                Today's Deals
              </Link>
            </nav>
          </div>
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Button variant="ghost" size="icon" className="mr-2">
                <User className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon">
                <ShoppingCart className="h-5 w-5" />
              </Button>
            </div>
            <div className="md:hidden ml-4">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon">
                    <Menu className="h-6 w-6" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-48">
                  <DropdownMenuItem>
                    <Link to="/" className="w-full">
                      Home
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Link to="/categories" className="w-full">
                      Categories
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Link to="/trending" className="w-full">
                      Trending
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Link to="/deals" className="w-full">
                      Today's Deals
                    </Link>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
export default Navbar;
