import { useState, useEffect } from 'react';
import { Play, Square, Plus, Check } from 'lucide-react';
import { taskApi, videoApi } from '../services/api';
import type { Task, VideoSource, ModelConfig } from '../types';

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [videos, setVideos] = useState<VideoSource[]>([]);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(1);
  const [selectedVideo, setSelectedVideo] = useState<string | null>(null);
  const [selectedModel, setSelectedModel] = useState<string>('yolo_v8');
  const [taskName, setTaskName] = useState('');
  const [taskType, setTaskType] = useState<'offline' | 'realtime'>('offline');
  const [outputType, setOutputType] = useState<'file' | 'rtmp' | 'hls'>('file');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [tasksData, videosData] = await Promise.all([
        taskApi.list(),
        videoApi.list(),
      ]);
      setTasks(tasksData.tasks);
      setVideos(videosData.videos);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async () => {
    if (!selectedVideo || !taskName) return;

    try {
      await taskApi.create({
        name: taskName,
        task_type: taskType,
        input_config: {
          source: { type: 'local', id: selectedVideo, auto_download: true, timeout: 300 },
          skip_frames: 0,
          buffer_size: 30,
          decode_threads: 4,
        },
        output_config: {
          type: outputType,
          path: '/data/output',
        },
        model_settings: {
          parallel: true,
          models: [
            {
              name: selectedModel,
              enabled: true,
              for_display: true,
              config: {
                confidence_threshold: 0.25,
                iou_threshold: 0.45,
                device: 'cpu',
              },
            },
          ],
        },
        priority: 50,
      });
      await loadData();
      resetForm();
    } catch (error) {
      console.error('Failed to create task:', error);
    }
  };

  const resetForm = () => {
    setStep(1);
    setSelectedVideo(null);
    setSelectedModel('yolo_v8');
    setTaskName('');
    setTaskType('offline');
    setOutputType('file');
  };

  const handleStartTask = async (id: string) => {
    try {
      await taskApi.start(id);
      await loadData();
    } catch (error) {
      console.error('Failed to start task:', error);
    }
  };

  const handleStopTask = async (id: string) => {
    try {
      await taskApi.stop(id);
      await loadData();
    } catch (error) {
      console.error('Failed to stop task:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'bg-app-primary';
      case 'completed':
        return 'bg-app-success';
      case 'failed':
        return 'bg-app-error';
      default:
        return 'bg-app-text-secondary';
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-app-text">任务管理</h1>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 bg-app-card rounded-xl p-6">
          <h2 className="text-lg font-medium mb-4">创建新任务</h2>

          <div className="flex items-center gap-2 mb-6">
            {[1, 2, 3].map((s) => (
              <div key={s} className="flex items-center">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center font-medium transition-colors ${
                    step >= s
                      ? 'bg-app-primary text-white'
                      : 'bg-gray-700 text-gray-400'
                  }`}
                >
                  {step > s ? <Check className="w-4 h-4" /> : s}
                </div>
                {s < 3 && (
                  <div className={`w-16 h-0.5 mx-2 ${step > s ? 'bg-app-primary' : 'bg-gray-700'}`} />
                )}
              </div>
            ))}
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm text-app-text-secondary mb-2">任务名称</label>
              <input
                type="text"
                value={taskName}
                onChange={(e) => setTaskName(e.target.value)}
                placeholder="输入任务名称"
                className="w-full px-4 py-2 bg-app-bg border border-gray-700 rounded-lg focus:border-app-primary focus:outline-none text-app-text"
              />
            </div>

            <div>
              <label className="block text-sm text-app-text-secondary mb-2">任务类型</label>
              <div className="flex gap-4">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    checked={taskType === 'offline'}
                    onChange={() => setTaskType('offline')}
                    className="accent-app-primary"
                  />
                  <span>离线任务</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    checked={taskType === 'realtime'}
                    onChange={() => setTaskType('realtime')}
                    className="accent-app-primary"
                  />
                  <span>实时任务</span>
                </label>
              </div>
            </div>

            {step >= 1 && (
              <div>
                <label className="block text-sm text-app-text-secondary mb-2">选择视频</label>
                <div className="grid grid-cols-3 gap-3">
                  {videos.map((video) => (
                    <div
                      key={video.id}
                      onClick={() => setSelectedVideo(video.id)}
                      className={`p-3 rounded-lg border cursor-pointer transition-all ${
                        selectedVideo === video.id
                          ? 'border-app-primary bg-app-primary/10'
                          : 'border-gray-700 hover:border-gray-600'
                      }`}
                    >
                      <p className="text-sm truncate">{video.name}</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {video.width}x{video.height}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {step >= 2 && (
              <div>
                <label className="block text-sm text-app-text-secondary mb-2">选择模型</label>
                <div className="grid grid-cols-2 gap-3">
                  {['yolo_v8', 'yolo_v8s', 'yolo_v8m'].map((model) => (
                    <div
                      key={model}
                      onClick={() => setSelectedModel(model)}
                      className={`p-3 rounded-lg border cursor-pointer transition-all ${
                        selectedModel === model
                          ? 'border-app-primary bg-app-primary/10'
                          : 'border-gray-700 hover:border-gray-600'
                      }`}
                    >
                      <p className="text-sm">{model}</p>
                      <p className="text-xs text-gray-500 mt-1">YOLOv8</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {step >= 3 && (
              <div>
                <label className="block text-sm text-app-text-secondary mb-2">输出类型</label>
                <div className="flex gap-4">
                  {(['file', 'rtmp', 'hls'] as const).map((type) => (
                    <label key={type} className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        checked={outputType === type}
                        onChange={() => setOutputType(type)}
                        className="accent-app-primary"
                      />
                      <span>{type.toUpperCase()}</span>
                    </label>
                  ))}
                </div>
              </div>
            )}

            <div className="flex gap-3 pt-4">
              {step > 1 && (
                <button
                  onClick={() => setStep(step - 1)}
                  className="px-4 py-2 text-sm bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
                >
                  上一步
                </button>
              )}
              {step < 3 && (
                <button
                  onClick={() => setStep(step + 1)}
                  disabled={step === 1 && !selectedVideo}
                  className="px-4 py-2 text-sm bg-app-primary hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors"
                >
                  下一步
                </button>
              )}
              {step === 3 && (
                <button
                  onClick={handleCreateTask}
                  disabled={!taskName || !selectedVideo}
                  className="px-4 py-2 text-sm bg-app-success hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors"
                >
                  创建任务
                </button>
              )}
            </div>
          </div>
        </div>

        <div className="bg-app-card rounded-xl p-6">
          <h2 className="text-lg font-medium mb-4">任务列表</h2>
          <div className="space-y-3">
            {tasks.slice(0, 5).map((task) => (
              <div key={task.id} className="p-3 bg-app-bg rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm truncate">{task.name}</p>
                  <span className={`px-2 py-0.5 text-xs rounded ${getStatusColor(task.status)}`}>
                    {task.status}
                  </span>
                </div>
                {task.status === 'running' && (
                  <div className="w-full bg-gray-700 rounded-full h-1.5 mb-2">
                    <div
                      className="bg-app-primary h-1.5 rounded-full transition-all"
                      style={{ width: `${task.progress}%` }}
                    />
                  </div>
                )}
                <div className="flex gap-2">
                  {task.status === 'pending' || task.status === 'queued' ? (
                    <button
                      onClick={() => handleStartTask(task.id)}
                      className="p-1.5 bg-app-primary/20 hover:bg-app-primary/30 rounded transition-colors"
                    >
                      <Play className="w-3 h-3" />
                    </button>
                  ) : task.status === 'running' ? (
                    <button
                      onClick={() => handleStopTask(task.id)}
                      className="p-1.5 bg-app-error/20 hover:bg-app-error/30 rounded transition-colors"
                    >
                      <Square className="w-3 h-3" />
                    </button>
                  ) : null}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}