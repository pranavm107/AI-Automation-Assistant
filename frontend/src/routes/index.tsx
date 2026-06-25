import { createBrowserRouter } from "react-router-dom";
import { AppLayout } from "../layouts/AppLayout";
import { DashboardPage } from "../pages/DashboardPage";
import { DocumentsPage } from "../pages/DocumentsPage";
import { ChatPage } from "../pages/ChatPage";
import { ResumePage } from "../pages/ResumePage";
import { InterviewPage } from "../pages/InterviewPage";
import { JobMatchPage } from "../pages/JobMatchPage";
import { RoadmapPage } from "../pages/RoadmapPage";
import { SettingsPage } from "../pages/SettingsPage";
import LoginPage from "../pages/LoginPage";
import RegisterPage from "../pages/RegisterPage";
import { ProtectedRoute } from "../components/auth/ProtectedRoute";
export const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/register",
    element: <RegisterPage />,
  },
  {
    path: "/",
    element: (
      <ProtectedRoute>
        <AppLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
      {
        path: "documents",
        element: <DocumentsPage />,
      },
      {
        path: "chat",
        element: <ChatPage />,
      },
      {
        path: "resume",
        element: <ResumePage />,
      },
      {
        path: "interview",
        element: <InterviewPage />,
      },
      {
        path: "job-match",
        element: <JobMatchPage />,
      },
      {
        path: "roadmap",
        element: <RoadmapPage />,
      },
      {
        path: "settings",
        element: <SettingsPage />,
      },
    ],
  },
]);
