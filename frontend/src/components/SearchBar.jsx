import { useState } from "react";
import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

function SearchBar() {
  const [searchQuery, setSearchQuery] = useState("");
  const [category, setCategory] = useState("all");

  const handleSearch = (e) => {
    e.preventDefault();
    console.log("Searching for:", searchQuery, "in category:", category);
    // Here you would typically call an API or update state to show search results
  };

  return (
    <form
      onSubmit={handleSearch}
      className="flex flex-col sm:flex-row gap-2 max-w-3xl mx-auto"
    >
      <div className="flex-1 flex">
        <Select value={category} onValueChange={setCategory}>
          <SelectTrigger className="w-[140px] rounded-r-none border-r-0">
            <SelectValue placeholder="Category" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Categories</SelectItem>
            <SelectItem value="electronics">Electronics</SelectItem>
            <SelectItem value="clothing">Clothing</SelectItem>
            <SelectItem value="home">Home & Kitchen</SelectItem>
            <SelectItem value="books">Books</SelectItem>
            <SelectItem value="toys">Toys</SelectItem>
          </SelectContent>
        </Select>
        <Input
          type="text"
          placeholder="Search for products, brands, and more..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="flex-1 rounded-l-none focus-visible:ring-0"
        />
      </div>
      <Button type="submit" className="px-8">
        <Search className="h-4 w-4 mr-2" />
        Search
      </Button>
    </form>
  );
}
export default SearchBar;
