import { useState, useCallback, useEffect } from 'react';
import { Upload, Trash2, Film, Clock, HardDrive } from 'lucide-react';
import { videoApi } from '../services/api';
import type { VideoSource } from '../types';

export default function VideosPage() {
  const [videos, setVideos] = useState<VideoSource[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const loadVideos = useCallback(async () => {
    setLoading(true);
    try {
      const response = await videoApi.list();
      setVideos(response.videos);
    } catch (error) {
      console.error('Failed to load videos:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadVideos();
  }, [loadVideos]);

  const handleUpload = async (file: File) => {
    setUploading(true);
    try {
      await videoApi.upload(file);
      await loadVideos();
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('video/')) {
      handleUpload(file);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await videoApi.delete(id);
      setVideos(videos.filter(v => v.id !== id));
    } catch (error) {
      console.error('Delete failed:', error);
    }
  };

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
    return `${(bytes / 1024 / 1024 / 1024).toFixed(1)} GB`;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-app-text">视频管理</h1>
        <button
          onClick={loadVideos}
          className="px-4 py-2 text-sm bg-app-card hover:bg-gray-700 rounded-lg transition-colors"
        >
          刷新列表
        </button>
      </div>

      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-input')?.click()}
        className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-200 ${
          dragOver
            ? 'border-app-primary bg-app-primary/10'
            : 'border-gray-600 hover:border-app-primary/50 hover:bg-app-card/50'
        }`}
      >
        <input
          id="file-input"
          type="file"
          accept="video/*"
          className="hidden"
          onChange={(e) => e.target.files?.[0] && handleUpload(e.target.files[0])}
        />
        <Upload className={`w-12 h-12 mx-auto mb-4 ${dragOver ? 'text-app-primary' : 'text-app-text-secondary'}`} />
        <p className="text-lg text-app-text mb-2">
          {uploading ? '上传中...' : '点击上传视频 或 拖拽文件到此处'}
        </p>
        <p className="text-sm text-app-text-secondary">支持 MP4, AVI, MOV, MKV, FLV 格式</p>
      </div>

      <div>
        <h2 className="text-lg font-medium text-app-text mb-4">已上传视频</h2>
        {loading ? (
          <div className="grid grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="skeleton h-48 rounded-lg" />
            ))}
          </div>
        ) : videos.length === 0 ? (
          <div className="text-center py-12 text-app-text-secondary">
            暂无视频，请上传
          </div>
        ) : (
          <div className="grid grid-cols-4 gap-4">
            {videos.map((video) => (
              <div
                key={video.id}
                className="bg-app-card rounded-lg overflow-hidden hover:-translate-y-1 hover:shadow-lg hover:shadow-black/20 transition-all duration-200 group"
              >
                <div className="h-32 bg-gray-800 flex items-center justify-center relative">
                  <Film className="w-12 h-12 text-gray-600" />
                  <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                    <button
                      onClick={() => handleDelete(video.id)}
                      className="p-2 bg-app-error/80 hover:bg-app-error rounded-lg transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                <div className="p-3">
                  <p className="text-sm text-app-text truncate" title={video.name}>
                    {video.name}
                  </p>
                  <div className="flex items-center gap-3 mt-2 text-xs text-app-text-secondary">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {formatDuration(video.duration)}
                    </span>
                    <span className="flex items-center gap-1">
                      <HardDrive className="w-3 h-3" />
                      {formatSize(video.size)}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}