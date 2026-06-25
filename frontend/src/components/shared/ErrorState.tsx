import { AlertTriangle } from "lucide-react";
import { Button } from "../ui/button";

interface ErrorStateProps {
  message?: string;
  onRetry?: () => void;
}

export function ErrorState({ message = "Something went wrong.", onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] w-full text-destructive space-y-4">
      <AlertTriangle className="h-10 w-10" />
      <p className="text-lg font-medium">{message}</p>
      {onRetry && (
        <Button variant="outline" onClick={onRetry}>
          Try Again
        </Button>
      )}
    </div>
  );
}
