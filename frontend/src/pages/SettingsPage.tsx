import { PageHeader } from "../components/shared/PageHeader";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { Server, Shield, Moon, Sun, Monitor } from "lucide-react";

export function SettingsPage() {
  return (
    <div>
      <PageHeader 
        title="Settings" 
        description="Manage platform preferences and system health."
      />

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Server className="mr-2 h-5 w-5" /> System Status
            </CardTitle>
            <CardDescription>Backend API connection health</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center p-3 rounded-lg border">
              <div>
                <p className="font-medium text-sm">FastAPI Backend</p>
                <p className="text-xs text-muted-foreground">http://localhost:8000</p>
              </div>
              <Badge variant="success">Online</Badge>
            </div>
            <div className="flex justify-between items-center p-3 rounded-lg border">
              <div>
                <p className="font-medium text-sm">PostgreSQL DB</p>
                <p className="text-xs text-muted-foreground">Connected</p>
              </div>
              <Badge variant="success">Online</Badge>
            </div>
            <div className="flex justify-between items-center p-3 rounded-lg border">
              <div>
                <p className="font-medium text-sm">FAISS Vector Store</p>
                <p className="text-xs text-muted-foreground">Active Indexes: 2</p>
              </div>
              <Badge variant="success">Online</Badge>
            </div>
            <div className="flex justify-between items-center p-3 rounded-lg border">
              <div>
                <p className="font-medium text-sm">Gemini AI Engine</p>
                <p className="text-xs text-muted-foreground">API Key valid</p>
              </div>
              <Badge variant="success">Online</Badge>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Shield className="mr-2 h-5 w-5" /> Preferences
            </CardTitle>
            <CardDescription>Local UI settings</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <p className="text-sm font-medium mb-3">Theme</p>
              <div className="flex gap-2">
                <Button variant="outline" className="flex-1">
                  <Sun className="mr-2 h-4 w-4" /> Light
                </Button>
                <Button variant="outline" className="flex-1 bg-secondary text-secondary-foreground">
                  <Moon className="mr-2 h-4 w-4" /> Dark
                </Button>
                <Button variant="outline" className="flex-1">
                  <Monitor className="mr-2 h-4 w-4" /> System
                </Button>
              </div>
            </div>
            <hr />
            <div>
              <p className="text-sm font-medium mb-3">Application Version</p>
              <p className="text-sm text-muted-foreground">v1.0.0 (Phase 10 Release)</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
