import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { documentService, interviewService } from "../services/api";
import { PageHeader } from "../components/shared/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Badge } from "../components/ui/badge";
import { LoadingState } from "../components/shared/LoadingState";
import { HelpCircle, ChevronDown, ChevronUp } from "lucide-react";

export function InterviewPage() {
  const [selectedDocId, setSelectedDocId] = useState<string>("");
  const [targetRole, setTargetRole] = useState("Software Engineer");
  const [expandedQ, setExpandedQ] = useState<number | null>(null);

  const { data: documents } = useQuery({
    queryKey: ['documents'],
    queryFn: documentService.getDocuments
  });

  const processedDocs = documents?.filter(d => d.processed) || [];

  const { data: mockData, refetch, isFetching } = useQuery({
    queryKey: ['mockInterview', selectedDocId, targetRole],
    queryFn: () => interviewService.generateMock(selectedDocId, targetRole),
    enabled: false
  });

  const handleGenerate = () => {
    if (!selectedDocId || !targetRole) return;
    refetch();
  };

  return (
    <div>
      <PageHeader 
        title="Mock Interview Generator" 
        description="Generate a personalized mock interview based on your resume."
      />

      <Card className="mb-8">
        <CardContent className="pt-6 flex flex-wrap gap-4 items-end">
          <div className="space-y-2">
            <label className="text-sm font-medium">Select Resume</label>
            <select 
              className="flex h-10 w-[250px] rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              value={selectedDocId}
              onChange={(e) => setSelectedDocId(e.target.value)}
            >
              <option value="" disabled>Select a resume</option>
              {processedDocs.map(doc => (
                <option key={doc.id} value={doc.id}>{doc.filename}</option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Target Role</label>
            <Input 
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g. Senior Data Scientist"
              className="w-[250px]"
            />
          </div>
          <Button onClick={handleGenerate} disabled={!selectedDocId || !targetRole || isFetching}>
            {isFetching ? "Generating..." : "Generate Session"}
          </Button>
        </CardContent>
      </Card>

      {isFetching && <LoadingState message="Generating personalized interview questions..." />}

      {mockData && !isFetching && (
        <div className="space-y-6">
          <Card className="bg-primary/5 border-primary/20">
            <CardContent className="pt-6">
              <h3 className="text-lg font-semibold mb-2">Interviewer Introduction</h3>
              <p className="text-muted-foreground italic">"{mockData.introduction}"</p>
            </CardContent>
          </Card>

          <div className="grid gap-4 md:grid-cols-4">
            <div className="md:col-span-3 space-y-4">
              <h3 className="text-xl font-bold mb-4 flex items-center">
                <HelpCircle className="mr-2 h-5 w-5" /> Interview Questions
              </h3>
              
              {mockData.questions.map((q, idx) => (
                <Card key={idx} className="overflow-hidden transition-all">
                  <div 
                    className="p-4 cursor-pointer hover:bg-muted/50 flex justify-between items-center"
                    onClick={() => setExpandedQ(expandedQ === idx ? null : idx)}
                  >
                    <div>
                      <div className="flex space-x-2 mb-2">
                        <Badge variant="outline">{q.category}</Badge>
                        <Badge variant={q.difficulty === 'Hard' ? 'destructive' : q.difficulty === 'Medium' ? 'secondary' : 'default'}>
                          {q.difficulty}
                        </Badge>
                      </div>
                      <p className="font-medium">{q.question}</p>
                    </div>
                    {expandedQ === idx ? <ChevronUp className="h-5 w-5 text-muted-foreground" /> : <ChevronDown className="h-5 w-5 text-muted-foreground" />}
                  </div>
                  
                  {expandedQ === idx && (
                    <div className="p-4 bg-muted/30 border-t">
                      <div className="mb-4">
                        <h4 className="text-sm font-semibold mb-1">Expected Answer:</h4>
                        <p className="text-sm text-muted-foreground">{q.expected_answer}</p>
                      </div>
                      <div>
                        <h4 className="text-sm font-semibold mb-1">Evaluation Criteria:</h4>
                        <ul className="list-disc pl-5 text-sm text-muted-foreground">
                          {q.evaluation_criteria.map((c, i) => <li key={i}>{c}</li>)}
                        </ul>
                      </div>
                    </div>
                  )}
                </Card>
              ))}
            </div>

            <div className="md:col-span-1">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Preparation Tips</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3">
                    {mockData.preparation_tips.map((tip, i) => (
                      <li key={i} className="text-sm flex items-start">
                        <span className="text-primary mr-2">•</span>
                        <span className="text-muted-foreground">{tip}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
