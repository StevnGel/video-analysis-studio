import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import VideoSources from './pages/VideoSources'
import Models from './pages/Models'
import Tasks from './pages/Tasks'
import Events from './pages/Events'
import Configs from './pages/Configs'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="video-sources" element={<VideoSources />} />
          <Route path="models" element={<Models />} />
          <Route path="tasks" element={<Tasks />} />
          <Route path="events" element={<Events />} />
          <Route path="configs" element={<Configs />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

export default App
