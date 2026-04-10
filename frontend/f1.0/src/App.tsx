import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AppLayout from './components/AppLayout';
import VideosPage from './pages/VideosPage';
import TasksPage from './pages/TasksPage';
import ModelsPage from './pages/ModelsPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Navigate to="/videos" replace />} />
          <Route path="videos" element={<VideosPage />} />
          <Route path="tasks" element={<TasksPage />} />
          <Route path="models" element={<ModelsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;