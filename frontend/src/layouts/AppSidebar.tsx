import { Link, useLocation } from "react-router-dom";
import { cn } from "../utils";
import { 
  LayoutDashboard, 
  Files, 
  MessageSquare, 
  FileText, 
  Users, 
  Briefcase, 
  Map, 
  Settings 
} from "lucide-react";

const navItems = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Documents", href: "/documents", icon: Files },
  { name: "RAG Chat", href: "/chat", icon: MessageSquare },
  { name: "Resume Analysis", href: "/resume", icon: FileText },
  { name: "Interview Prep", href: "/interview", icon: Users },
  { name: "Job Matching", href: "/job-match", icon: Briefcase },
  { name: "Career Roadmap", href: "/roadmap", icon: Map },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function AppSidebar() {
  const location = useLocation();

  return (
    <div className="flex h-full w-64 flex-col border-r bg-card px-4 py-6">
      <div className="flex items-center space-x-2 px-2 mb-8">
        <div className="h-8 w-8 rounded bg-primary flex items-center justify-center">
          <span className="text-primary-foreground font-bold text-lg">AI</span>
        </div>
        <span className="text-xl font-bold tracking-tight">Career Intel</span>
      </div>

      <nav className="flex-1 space-y-1">
        {navItems.map((item) => {
          const isActive = location.pathname === item.href;
          return (
            <Link
              key={item.name}
              to={item.href}
              className={cn(
                "flex items-center space-x-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                isActive 
                  ? "bg-secondary text-secondary-foreground" 
                  : "text-muted-foreground hover:bg-secondary/50 hover:text-foreground"
              )}
            >
              <item.icon className="h-5 w-5" />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
