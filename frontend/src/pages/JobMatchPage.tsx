import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { documentService, jobService } from "../services/api";
import { PageHeader } from "../components/shared/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { LoadingState } from "../components/shared/LoadingState";
import { Briefcase, Target, AlertCircle } from "lucide-react";

export function JobMatchPage() {
  const [selectedDocId, setSelectedDocId] = useState<string>("");
  const [jdText, setJdText] = useState("");
  const [isMatching, setIsMatching] = useState(false);

  const { data: documents } = useQuery({
    queryKey: ['documents'],
    queryFn: documentService.getDocuments
  });
  const processedDocs = documents?.filter(d => d.processed) || [];

  const { data: recData, refetch: refetchRecs, isFetching: isFetchingRecs } = useQuery({
    queryKey: ['jobRecs', selectedDocId],
    queryFn: () => jobService.recommendJobs(selectedDocId),
    enabled: false
  });

  const { data: matchData, refetch: refetchMatch, isFetching: isFetchingMatch } = useQuery({
    queryKey: ['jobMatch', selectedDocId, jdText],
    queryFn: () => jobService.matchJob(selectedDocId, jdText),
    enabled: false
  });

  const handleRecommend = () => {
    if (selectedDocId) refetchRecs();
  };

  const handleMatch = () => {
    if (selectedDocId && jdText.trim()) {
      setIsMatching(true);
      refetchMatch().finally(() => setIsMatching(false));
    }
  };

  return (
    <div>
      <PageHeader 
        title="Job Matching" 
        description="Find recommended roles or score your resume against a specific JD."
      />

      <Card className="mb-8">
        <CardContent className="pt-6 flex flex-wrap gap-4 items-center">
          <div className="space-y-2">
            <label className="text-sm font-medium">Select Resume</label>
            <select 
              className="flex h-10 w-[300px] rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              value={selectedDocId}
              onChange={(e) => setSelectedDocId(e.target.value)}
            >
              <option value="" disabled>Select a resume</option>
              {processedDocs.map(doc => (
                <option key={doc.id} value={doc.id}>{doc.filename}</option>
              ))}
            </select>
          </div>
          <div className="mt-7">
            <Button onClick={handleRecommend} disabled={!selectedDocId || isFetchingRecs} variant="secondary">
              {isFetchingRecs ? "Finding Roles..." : "Suggest Roles"}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* AI Recommendations */}
      {recData && (
        <div className="mb-8">
          <h3 className="text-xl font-bold mb-4 flex items-center">
            <Briefcase className="mr-2 h-5 w-5" /> Top Recommended Roles
          </h3>
          <div className="grid gap-4 md:grid-cols-3">
            {recData.map((rec, i) => (
              <Card key={i}>
                <CardHeader className="pb-2">
                  <div className="flex justify-between items-start">
                    <CardTitle className="text-lg">{rec.role}</CardTitle>
                    <Badge variant={rec.match > 80 ? "success" : "secondary"}>{rec.match}% Match</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{rec.reason}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Specific JD Match */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Compare Specific Job Description</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <textarea
              className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring min-h-[250px]"
              placeholder="Paste Job Description here..."
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
            />
            <Button onClick={handleMatch} disabled={!selectedDocId || !jdText.trim() || isMatching} className="w-full">
              {isMatching ? "Calculating Match..." : "Calculate Match Score"}
            </Button>
          </CardContent>
        </Card>

        {isFetchingMatch ? (
          <LoadingState message="Analyzing Job Description..." />
        ) : matchData ? (
          <Card>
            <CardHeader className="pb-2 border-b">
              <div className="flex justify-between items-center">
                <CardTitle>Match Results</CardTitle>
                <div className="text-3xl font-bold text-primary">{matchData.match_score}/100</div>
              </div>
            </CardHeader>
            <CardContent className="pt-6 space-y-6">
              <div>
                <h4 className="flex items-center font-medium text-green-600 mb-2">
                  <Target className="h-4 w-4 mr-2" /> Matching Skills
                </h4>
                <div className="flex flex-wrap gap-2">
                  {matchData.matching_skills.map((skill, i) => (
                    <Badge key={i} variant="outline" className="bg-green-50 text-green-700 border-green-200">{skill}</Badge>
                  ))}
                </div>
              </div>

              {matchData.missing_skills.length > 0 && (
                <div>
                  <h4 className="flex items-center font-medium text-destructive mb-2">
                    <AlertCircle className="h-4 w-4 mr-2" /> Missing Skills
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {matchData.missing_skills.map((skill, i) => (
                      <Badge key={i} variant="outline" className="bg-red-50 text-red-700 border-red-200">{skill}</Badge>
                    ))}
                  </div>
                </div>
              )}

              <div className="bg-muted/50 p-4 rounded-lg">
                <h4 className="font-semibold text-sm mb-2">Recommendations</h4>
                <ul className="list-disc pl-5 text-sm text-muted-foreground space-y-1">
                  {matchData.recommendations.map((r, i) => <li key={i}>{r}</li>)}
                </ul>
              </div>
            </CardContent>
          </Card>
        ) : (
          <div className="flex items-center justify-center border rounded-lg bg-card text-muted-foreground p-6">
            Paste a JD and click calculate to see your match score.
          </div>
        )}
      </div>
    </div>
  );
}
