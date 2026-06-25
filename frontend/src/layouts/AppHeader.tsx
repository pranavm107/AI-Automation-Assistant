import { Bell, Search, User } from "lucide-react";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

export function AppHeader() {
  return (
    <header className="flex h-16 items-center justify-between border-b bg-card px-6">
      <div className="flex items-center space-x-4 w-1/3">
        <div className="relative w-full">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input 
            type="search" 
            placeholder="Search..." 
            className="w-full bg-background pl-9 md:w-[300px] lg:w-[400px]" 
          />
        </div>
      </div>
      
      <div className="flex items-center space-x-4">
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="h-5 w-5" />
          <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-destructive"></span>
        </Button>
        <Button variant="ghost" size="icon" className="rounded-full bg-secondary">
          <User className="h-5 w-5" />
        </Button>
      </div>
    </header>
  );
}
