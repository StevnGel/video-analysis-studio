import { useState, useEffect } from 'react';
import { Box, Cpu, MemoryStick, Clock } from 'lucide-react';
import { modelApi } from '../services/api';

interface ModelInstance {
  instance_id: string;
  model_name: string;
  device: string;
  status: string;
  gpu_memory?: number;
  last_used?: string;
}

export default function ModelsPage() {
  const [models, setModels] = useState<any[]>([]);
  const [instances, setInstances] = useState<ModelInstance[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [modelsData, instancesData] = await Promise.all([
        modelApi.list(),
        modelApi.getInstances(),
      ]);
      setModels(modelsData);
      setInstances(instancesData);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'ready':
        return <span className="px-2 py-0.5 text-xs rounded bg-app-success/20 text-app-success">就绪</span>;
      case 'in_use':
        return <span className="px-2 py-0.5 text-xs rounded bg-app-primary/20 text-app-primary">使用中</span>;
      case 'loading':
        return <span className="px-2 py-0.5 text-xs rounded bg-app-warning/20 text-app-warning">加载中</span>;
      case 'error':
        return <span className="px-2 py-0.5 text-xs rounded bg-app-error/20 text-app-error">错误</span>;
      default:
        return <span className="px-2 py-0.5 text-xs rounded bg-gray-600 text-gray-300">{status}</span>;
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-app-text">模型管理</h1>

      <div>
        <h2 className="text-lg font-medium text-app-text mb-4">可用模型</h2>
        {loading ? (
          <div className="grid grid-cols-3 gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="skeleton h-40 rounded-xl" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-3 gap-4">
            {models.map((model) => (
              <div
                key={model.name}
                className="bg-app-card rounded-xl p-6 hover:-translate-y-1 hover:shadow-lg hover:shadow-black/20 transition-all duration-200"
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-12 h-12 bg-app-primary/20 rounded-lg flex items-center justify-center">
                    <Box className="w-6 h-6 text-app-primary" />
                  </div>
                  <div>
                    <h3 className="font-medium text-app-text">{model.name}</h3>
                    <p className="text-sm text-app-text-secondary">{model.framework}</p>
                  </div>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center justify-between">
                    <span className="text-app-text-secondary">类型</span>
                    <span className="text-app-text">{model.type}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-app-text-secondary">设备</span>
                    <span className="text-app-text">{model.device || 'CPU'}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-medium text-app-text">实例状态</h2>
          <button
            onClick={loadData}
            className="px-4 py-2 text-sm bg-app-card hover:bg-gray-700 rounded-lg transition-colors"
          >
            刷新
          </button>
        </div>
        <div className="bg-app-card rounded-xl overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="px-6 py-3 text-left text-xs font-medium text-app-text-secondary uppercase tracking-wider">
                  实例ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-app-text-secondary uppercase tracking-wider">
                  模型
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-app-text-secondary uppercase tracking-wider">
                  设备
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-app-text-secondary uppercase tracking-wider">
                  状态
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-app-text-secondary uppercase tracking-wider">
                  内存
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-app-text-secondary uppercase tracking-wider">
                  最后使用
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {instances.map((instance) => (
                <tr key={instance.instance_id} className="hover:bg-app-bg/50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-app-text">
                    {instance.instance_id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-app-text">
                    {instance.model_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="flex items-center gap-1 text-sm text-app-text">
                      <Cpu className="w-4 h-4" />
                      {instance.device}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {getStatusBadge(instance.status)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="flex items-center gap-1 text-sm text-app-text">
                      <MemoryStick className="w-4 h-4" />
                      {instance.gpu_memory ? `${instance.gpu_memory}MB` : '-'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="flex items-center gap-1 text-sm text-app-text-secondary">
                      <Clock className="w-4 h-4" />
                      {instance.last_used || '-'}
                    </span>
                  </td>
                </tr>
              ))}
              {instances.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-app-text-secondary">
                    暂无实例数据
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}