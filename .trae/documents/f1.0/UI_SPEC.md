# f1.0 UI 组件规范

> 视频分析工作台前端 UI 组件文档
> 版本: 1.0.0

---

## 1. 布局组件

## 1.1 AppLayout - 主布局

```tsx
<AppLayout>
  <Outlet />  // 子页面渲染位置
</AppLayout>
```

**属性**:
- 无

**结构**:
```
┌──────────────────────────────────────┐
│           AppHeader (64px)           │
├─────────┬────────────────────────────┤
│         │                            │
│ Sidebar │      Main Content         │
│ (240px) │       (flex-1)            │
│         │                            │
└─────────┴────────────────────────────┘
```

---

## 2. 页面组件

## 2.1 VideosPage - 视频管理

**路由**: `/videos`

**功能**:
- 视频上传（点击/拖拽）
- 视频列表展示
- 视频删除

**代码示例**:
```tsx
function VideosPage() {
  const [videos, setVideos] = useState<VideoSource[]>([])
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [dragOver, setDragOver] = useState(false)
  
  // 加载视频列表
  const loadVideos = useCallback(async () => {
    const response = await videoApi.list()
    setVideos(response.videos)
  }, [])
  
  // 上传视频
  const handleUpload = async (file: File) => {
    await videoApi.upload(file)
    await loadVideos()
  }
  
  // 删除视频
  const handleDelete = async (id: string) => {
    await videoApi.delete(id)
    setVideos(videos.filter(v => v.id !== id))
  }
}
```

**子组件**:

### UploadZone - 上传区域

```
┌─────────────────────────────────────┐
│          + (Upload 图标)            │
│     点击上传视频 或 拖拽文件到此处   │
│     支持 MP4, AVI, MOV, MKV 格式   │
└─────────────────────────────────────┘
```

| 状态 | 样式 |
|------|------|
| Default | `border-gray-600` |
| DragOver | `border-app-primary bg-app-primary/10` |
| Hover | `hover:border-app-primary/50` |

### VideoCard - 视频卡片

```
┌─────────────────────────┐
│                         │
│    [Film 图标]          │
│    缩略图区域            │
│                         │
├─────────────────────────┤
│  视频名称               │
│  ⏱ 0:45  💾 33MB       │
└─────────────────────────┘
```

| 状态 | 样式 |
|------|------|
| Default | `bg-app-card` |
| Hover | 显示删除按钮遮罩 |

---

## 2.2 TasksPage - 任务管理

**路由**: `/tasks`

**功能**:
- 创建新任务（3步引导）
- 任务列表展示
- 启动/停止任务

**代码结构**:
```
┌───────────────────────────┬─────────────────────┐
│                           │                     │
│   创建任务卡片             │    任务列表         │
│   (2/3 宽度)              │    (1/3 宽度)       │
│                           │                     │
│   ┌─────────────────┐    │   ┌─────────────┐   │
│   │ 步骤条 [1][2][3] │    │   │ 任务卡片    │   │
│   └─────────────────┘    │   └─────────────┘   │
│                           │                     │
│   ┌─────────────────┐    │   ┌─────────────┐   │
│   │ 任务名称输入    │    │   │ 任务卡片    │   │
│   └─────────────────┘    │   └─────────────┘   │
│                           │                     │
│   ┌─────────────────┐    │   ┌─────────────┐   │
│   │ 视频选择网格    │    │   │ 任务卡片    │   │
│   └─────────────────┘    │   └─────────────┘   │
│                           │                     │
│   [上一步] [下一步] [创建]                      │
│                           │                     │
└───────────────────────────┴─────────────────────┘
```

### StepIndicator - 步骤指示器

```
[1]────[2]────[3]
```

| 状态 | 样式 |
|------|------|
| Completed | `bg-app-primary text-white` |
| Current | `bg-app-primary/50` |
| Pending | `bg-gray-700 text-gray-400` |

### TaskCard - 任务卡片

```
┌─────────────────────────────────────┐
│ 任务名称              [运行中]      │
│ ─────────────────────────────────  │
│ ████████████░░░░░░░░░ 45%          │
│ 视频: xxx.mp4                      │
│ 模型: YOLOv8                        │
│ ─────────────────────────────────  │
│ [停止] [查看输出]                   │
└─────────────────────────────────────┘
```

---

## 2.3 ModelsPage - 模型管理

**路由**: `/models`

**功能**:
- 展示可用模型卡片
- 展示实例状态表格

**代码结构**:
```
┌─────────────────────────────────────────┐
│                                         │
│  可用模型                                │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │  模型   │ │  模型   │ │  模型   │   │
│  │  卡片   │ │  卡片   │ │  卡片   │   │
│  └─────────┘ └─────────┘ └─────────┘   │
│                                         │
│  实例状态                                │
│  ┌─────────────────────────────────┐   │
│  │ 表格                             │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

### ModelCard - 模型卡片

```
┌─────────────────────────────┐
│  [Box 图标]                  │
│  YOLO v8                    │
│  类型: 检测                  │
│  设备: CPU                  │
└─────────────────────────────┘
```

### InstanceTable - 实例表格

| 列名 | 字段 | 宽度 |
|------|------|------|
| 实例ID | instance_id | auto |
| 模型 | model_name | 120px |
| 设备 | device | 80px |
| 状态 | status | 100px |
| 内存 | gpu_memory | 100px |
| 最后使用 | last_used | 150px |

---

## 3. 组件状态样式

## 3.1 按钮状态

```tsx
// Primary
<button className="bg-app-primary hover:bg-blue-600">
// Secondary  
<button className="bg-app-card hover:bg-gray-700">
// Danger
<button className="bg-app-error/80 hover:bg-app-error">
// Disabled
<button disabled className="opacity-50 cursor-not-allowed">
```

## 3.2 输入框状态

```tsx
// Default
<input className="bg-app-bg border border-gray-700">

// Focus
<input className="focus:border-app-primary focus:outline-none">

// Error
<input className="border-app-error">
```

## 3.3 卡片状态

```tsx
// Default
<div className="bg-app-card rounded-lg">

// Hover
<div className="hover:-translate-y-1 hover:shadow-lg hover:shadow-black/20 transition-all duration-200">
```

## 3.4 标签状态

```tsx
// Success
<span className="bg-app-success/20 text-app-success">

// Warning
<span className="bg-app-warning/20 text-app-warning">

// Error
<span className="bg-app-error/20 text-app-error">

// Info
<span className="bg-app-primary/20 text-app-primary">
```

---

## 4. 动画规范

## 4.1 过渡动画

```css
/* 基础过渡 */
transition-all duration-200

/* 快速过渡 */
transition-colors duration-150

/* 骨架屏 */
animation: shimmer 1.5s infinite
```

## 4.2 动效参数

| 动画 | 时长 | 缓动 |
|------|------|------|
| 页面切换 | 150ms | ease-out |
| 按钮悬停 | 150ms | ease |
| 卡片悬停 | 200ms | ease |
| 加载骨架 | 1500ms | linear |

---

## 5. 响应式断点

```css
/* 桌面端 >= 1024px */
@media (min-width: 1024px) {
  .sidebar { width: 240px; }
}

/* 平板端 768-1023px */
@media (min-width: 768px) and (max-width: 1023px) {
  .sidebar { width: 64px; }
}

/* 移动端 < 768px */
@media (max-width: 767px) {
  .sidebar { display: none; }
}
```

---

## 6. 图标使用

使用 `lucide-react` 图标库:

```tsx
import { 
  Video,          // 视频
  PlaySquare,     // 任务
  Box,            // 模型
  Upload,         // 上传
  Trash2,         // 删除
  Film,           // 视频文件
  Clock,          // 时长
  HardDrive,      // 文件大小
  Cpu,            // 设备
  MemoryStick,    // 内存
} from 'lucide-react'
```

图标大小规范:
- 导航: `w-5 h-5`
- 标题: `w-12 h-12`
- 按钮: `w-4 h-4`

---

## 7. 工具函数

## 7.1 格式化函数

```tsx
// 格式化时长
const formatDuration = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 格式化文件大小
const formatSize = (bytes: number) => {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(1)} MB`
  return `${(bytes / 1024 / 1024 / 1024).toFixed(1)} GB`
}
```

## 7.2 状态颜色函数

```tsx
const getStatusColor = (status: string) => {
  switch (status) {
    case 'running': return 'bg-app-primary'
    case 'completed': return 'bg-app-success'
    case 'failed': return 'bg-app-error'
    default: return 'bg-app-text-secondary'
  }
}

const getStatusBadge = (status: string) => {
  switch (status) {
    case 'ready': return '就绪'
    case 'in_use': return '使用中'
    case 'loading': return '加载中'
    case 'error': return '错误'
  }
}
```

---

## 8. 文件对应

| 组件 | 文件路径 |
|------|----------|
| AppLayout | `src/components/AppLayout.tsx` |
| VideosPage | `src/pages/VideosPage.tsx` |
| TasksPage | `src/pages/TasksPage.tsx` |
| ModelsPage | `src/pages/ModelsPage.tsx` |
| API | `src/services/api.ts` |
| Types | `src/types/index.ts` |
| Styles | `src/index.css` |
