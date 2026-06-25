import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { documentService } from "../services/api";
import { PageHeader } from "../components/shared/PageHeader";
import { LoadingState } from "../components/shared/LoadingState";
import { ErrorState } from "../components/shared/ErrorState";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Badge } from "../components/ui/badge";
import { Card, CardContent } from "../components/ui/card";
import { Trash2, FileText, UploadCloud, RefreshCw, Database } from "lucide-react";

export function DocumentsPage() {
  const queryClient = useQueryClient();
  const [file, setFile] = useState<File | null>(null);

  const { data: documents, isLoading, isError, refetch } = useQuery({
    queryKey: ['documents'],
    queryFn: documentService.getDocuments
  });

  const uploadMutation = useMutation({
    mutationFn: documentService.uploadDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
      setFile(null);
    }
  });

  const processMutation = useMutation({
    mutationFn: documentService.processDocument,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['documents'] })
  });

  const indexMutation = useMutation({
    mutationFn: documentService.createIndex,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['documents'] })
  });

  const deleteMutation = useMutation({
    mutationFn: documentService.deleteDocument,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['documents'] })
  });

  const handleUpload = () => {
    if (file) {
      uploadMutation.mutate(file);
    }
  };

  if (isLoading) return <LoadingState message="Loading documents..." />;
  if (isError) return <ErrorState onRetry={refetch} />;

  return (
    <div>
      <PageHeader 
        title="Documents" 
        description="Manage your uploaded resumes and job descriptions."
      />

      <Card className="mb-8">
        <CardContent className="pt-6">
          <div className="flex items-center space-x-4">
            <Input 
              type="file" 
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="max-w-sm"
            />
            <Button 
              onClick={handleUpload} 
              disabled={!file || uploadMutation.isPending}
              className="flex items-center gap-2"
            >
              {uploadMutation.isPending ? <RefreshCw className="h-4 w-4 animate-spin" /> : <UploadCloud className="h-4 w-4" />}
              Upload
            </Button>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4">
        {documents?.length === 0 ? (
          <div className="text-center p-12 border rounded-lg bg-card text-muted-foreground">
            <FileText className="mx-auto h-12 w-12 mb-4 opacity-20" />
            <p>No documents uploaded yet.</p>
          </div>
        ) : (
          documents?.map((doc) => (
            <Card key={doc.id}>
              <CardContent className="flex items-center justify-between p-6">
                <div className="flex items-center space-x-4">
                  <div className="h-10 w-10 bg-secondary rounded flex items-center justify-center">
                    <FileText className="h-5 w-5 text-secondary-foreground" />
                  </div>
                  <div>
                    <h4 className="font-semibold">{doc.filename}</h4>
                    <p className="text-sm text-muted-foreground">ID: {doc.id.substring(0, 8)}...</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="flex space-x-2">
                    <Badge variant={doc.processed ? "success" : "secondary"}>
                      {doc.processed ? "Processed" : "Unprocessed"}
                    </Badge>
                    <Badge variant={doc.indexed ? "success" : "secondary"}>
                      {doc.indexed ? "Indexed" : "Not Indexed"}
                    </Badge>
                  </div>
                  
                  <div className="flex space-x-2">
                    {!doc.processed && (
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => processMutation.mutate(doc.id)}
                        disabled={processMutation.isPending}
                      >
                        <RefreshCw className={`h-4 w-4 mr-2 ${processMutation.isPending ? 'animate-spin' : ''}`} />
                        Process
                      </Button>
                    )}
                    {doc.processed && !doc.indexed && (
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => indexMutation.mutate(doc.id)}
                        disabled={indexMutation.isPending}
                      >
                        <Database className={`h-4 w-4 mr-2 ${indexMutation.isPending ? 'animate-spin' : ''}`} />
                        Index Vector
                      </Button>
                    )}
                    <Button 
                      variant="destructive" 
                      size="icon"
                      onClick={() => deleteMutation.mutate(doc.id)}
                      disabled={deleteMutation.isPending}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
