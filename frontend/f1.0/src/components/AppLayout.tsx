import { Outlet, Link, useLocation } from 'react-router-dom';
import { Video, PlaySquare, Box, Menu, X } from 'lucide-react';
import { useState } from 'react';

const navItems = [
  { path: '/videos', label: '视频上传', icon: Video },
  { path: '/tasks', label: '任务创建', icon: PlaySquare },
  { path: '/models', label: '模型管理', icon: Box },
];

export default function AppLayout() {
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="flex h-screen bg-app-bg">
      <aside
        className={`${
          sidebarOpen ? 'w-60' : 'w-16'
        } bg-app-bg-secondary border-r border-gray-800 flex flex-col transition-all duration-200`}
      >
        <div className="h-16 flex items-center px-4 border-b border-gray-800">
          {sidebarOpen ? (
            <h1 className="text-lg font-bold text-app-primary">视频分析工作台</h1>
          ) : (
            <span className="text-2xl font-bold text-app-primary">V</span>
          )}
        </div>

        <nav className="flex-1 py-4">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center px-4 py-3 mx-2 rounded-lg transition-all duration-150 ${
                  isActive
                    ? 'bg-app-primary/20 text-app-primary'
                    : 'text-app-text-secondary hover:bg-app-card hover:text-app-text'
                }`}
              >
                <Icon className="w-5 h-5" />
                {sidebarOpen && <span className="ml-3">{item.label}</span>}
              </Link>
            );
          })}
        </nav>
      </aside>

      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="h-16 bg-app-bg-secondary border-b border-gray-800 flex items-center justify-between px-6">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-lg hover:bg-app-card text-app-text-secondary transition-colors"
          >
            {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>

          <div className="flex items-center gap-4">
            <span className="text-sm text-app-text-secondary">v1.0.0</span>
          </div>
        </header>

        <main className="flex-1 overflow-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}