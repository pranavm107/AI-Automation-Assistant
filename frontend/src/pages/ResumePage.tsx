import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { documentService, resumeService } from "../services/api";
import { PageHeader } from "../components/shared/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { LoadingState } from "../components/shared/LoadingState";
import { CheckCircle2, XCircle, Lightbulb } from "lucide-react";

export function ResumePage() {
  const [selectedDocId, setSelectedDocId] = useState<string>("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const { data: documents } = useQuery({
    queryKey: ['documents'],
    queryFn: documentService.getDocuments
  });

  const processedDocs = documents?.filter(d => d.processed) || [];

  const { data: atsData, refetch: refetchAts, isFetching: isFetchingAts } = useQuery({
    queryKey: ['ats', selectedDocId],
    queryFn: () => resumeService.getAtsScore(selectedDocId),
    enabled: false
  });

  const { data: gapData, refetch: refetchGap, isFetching: isFetchingGap } = useQuery({
    queryKey: ['skillgap', selectedDocId],
    queryFn: () => resumeService.getSkillGap(selectedDocId),
    enabled: false
  });

  const handleAnalyze = async () => {
    if (!selectedDocId) return;
    setIsAnalyzing(true);
    await Promise.all([refetchAts(), refetchGap()]);
    setIsAnalyzing(false);
  };

  const isLoading = isAnalyzing || isFetchingAts || isFetchingGap;

  return (
    <div>
      <PageHeader 
        title="Resume Analysis" 
        description="Get ATS scores and uncover skill gaps."
      />

      <div className="flex items-center space-x-4 mb-8">
        <select 
          className="flex h-10 w-[300px] rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          value={selectedDocId}
          onChange={(e) => setSelectedDocId(e.target.value)}
        >
          <option value="" disabled>Select a processed resume</option>
          {processedDocs.map(doc => (
            <option key={doc.id} value={doc.id}>{doc.filename}</option>
          ))}
        </select>
        <Button onClick={handleAnalyze} disabled={!selectedDocId || isLoading}>
          {isLoading ? "Analyzing..." : "Analyze Resume"}
        </Button>
      </div>

      {isLoading && <LoadingState message="Scanning resume for ATS compatibility..." />}

      {atsData && !isLoading && (
        <div className="grid gap-6 md:grid-cols-2">
          {/* ATS Score */}
          <Card className="col-span-full md:col-span-1">
            <CardHeader>
              <CardTitle>ATS Compatibility Score</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col items-center justify-center p-6">
              <div className="relative flex h-40 w-40 items-center justify-center rounded-full border-8 border-secondary">
                <div className="absolute inset-0 rounded-full border-8 border-primary" style={{ clipPath: `inset(${100 - atsData.ats_score}% 0 0 0)` }}></div>
                <span className="text-4xl font-bold">{atsData.ats_score}</span>
              </div>
            </CardContent>
          </Card>

          {/* Strengths & Weaknesses */}
          <Card className="col-span-full md:col-span-1">
            <CardHeader>
              <CardTitle>Profile Breakdown</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <h4 className="flex items-center font-medium text-green-600 mb-2">
                  <CheckCircle2 className="h-4 w-4 mr-2" /> Improvements
                </h4>
                <ul className="list-disc pl-5 text-sm text-muted-foreground space-y-1">
                  {atsData.improvements.map((s, i) => <li key={i}>{s}</li>)}
                </ul>
              </div>
              <div>
                <h4 className="flex items-center font-medium text-destructive mb-2">
                  <XCircle className="h-4 w-4 mr-2" /> Missing Sections
                </h4>
                <ul className="list-disc pl-5 text-sm text-muted-foreground space-y-1">
                  {atsData.missing_sections.map((w, i) => <li key={i}>{w}</li>)}
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Skill Gaps */}
          {gapData && (
            <Card className="col-span-full">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Lightbulb className="h-5 w-5 mr-2 text-yellow-500" /> 
                  Skill Gap Analysis
                </CardTitle>
              </CardHeader>
              <CardContent className="grid gap-6 md:grid-cols-2">
                <div>
                  <h5 className="font-medium mb-2">Missing Industry Skills</h5>
                  <div className="flex flex-wrap gap-2">
                    {gapData.missing_skills.map((skill, i) => (
                      <span key={i} className="inline-flex items-center rounded-md bg-secondary px-2 py-1 text-xs font-medium text-secondary-foreground ring-1 ring-inset ring-secondary-foreground/10">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <h5 className="font-medium mb-2">Recommended Skills</h5>
                  <ul className="list-disc pl-5 text-sm text-muted-foreground space-y-1">
                    {gapData.recommended_skills.map((area, i) => <li key={i}>{area}</li>)}
                  </ul>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
