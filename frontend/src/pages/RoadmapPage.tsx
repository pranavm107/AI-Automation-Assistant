import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { documentService, jobService } from "../services/api";
import { PageHeader } from "../components/shared/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Badge } from "../components/ui/badge";
import { LoadingState } from "../components/shared/LoadingState";
import { Map, Flag, CheckCircle } from "lucide-react";

export function RoadmapPage() {
  const [selectedDocId, setSelectedDocId] = useState<string>("");
  const [targetRole, setTargetRole] = useState("Machine Learning Engineer");

  const { data: documents } = useQuery({
    queryKey: ['documents'],
    queryFn: documentService.getDocuments
  });

  const processedDocs = documents?.filter(d => d.processed) || [];

  const { data: roadmapData, refetch, isFetching } = useQuery({
    queryKey: ['roadmap', selectedDocId, targetRole],
    queryFn: () => jobService.generateRoadmap(selectedDocId, targetRole),
    enabled: false
  });

  const handleGenerate = () => {
    if (!selectedDocId || !targetRole) return;
    refetch();
  };

  return (
    <div>
      <PageHeader 
        title="Career Roadmap" 
        description="Generate a personalized learning path to reach your dream role."
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
              placeholder="e.g. Data Scientist"
              className="w-[250px]"
            />
          </div>
          <Button onClick={handleGenerate} disabled={!selectedDocId || !targetRole || isFetching}>
            {isFetching ? "Generating..." : "Build Roadmap"}
          </Button>
        </CardContent>
      </Card>

      {isFetching && <LoadingState message="Analyzing skill gaps and building curriculum..." />}

      {roadmapData && !isFetching && (
        <div className="space-y-8">
          <div className="flex flex-col md:flex-row gap-6">
            <Card className="flex-1 bg-primary text-primary-foreground">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-2xl font-bold">{roadmapData.target_role}</h3>
                  <Flag className="h-6 w-6 opacity-80" />
                </div>
                <p className="text-primary-foreground/80">
                  Estimated 6-Month Upskilling Path based on your current profile.
                </p>
              </CardContent>
            </Card>

            <Card className="flex-[2]">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center">
                  <Map className="mr-2 h-5 w-5" /> Master Skill Target List
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {roadmapData.recommended_skills.map((skill, i) => (
                    <Badge key={i} variant="secondary">{skill}</Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="relative border-l-2 border-muted ml-4 md:ml-6 space-y-8 pb-8">
            {roadmapData.milestones.map((milestone, idx) => (
              <div key={idx} className="relative pl-8 md:pl-10">
                <div className="absolute -left-[11px] top-1 h-5 w-5 rounded-full bg-background border-2 border-primary flex items-center justify-center">
                  <div className="h-2 w-2 rounded-full bg-primary" />
                </div>
                
                <Card>
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-center">
                      <CardTitle className="text-lg text-primary">{milestone.month}</CardTitle>
                    </div>
                    <p className="font-medium text-lg mt-1">{milestone.focus}</p>
                  </CardHeader>
                  <CardContent>
                    <div className="grid gap-2 md:grid-cols-2 lg:grid-cols-3">
                      {milestone.topics.map((topic, i) => (
                        <div key={i} className="flex items-center space-x-2 text-sm text-muted-foreground p-2 rounded-md bg-secondary/50">
                          <CheckCircle className="h-4 w-4 text-green-500" />
                          <span>{topic}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
