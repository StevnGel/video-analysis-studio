export interface VideoSource {
  id: string;
  name: string;
  original_name: string;
  type: 'file' | 'rtsp';
  path: string;
  size: number;
  duration: number;
  width: number;
  height: number;
  fps: number;
  codec: string;
  status: 'ready' | 'processing' | 'deleted';
  tags?: string[];
  metadata?: {
    bitrate?: string;
    audio_codec?: string;
    has_audio?: boolean;
  };
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: string;
  name: string;
  task_type: 'realtime' | 'offline';
  video_source_id?: string;
  input_config?: InputConfig;
  output_config?: OutputConfig;
  model_settings?: ModelConfig;
  status: TaskStatus;
  progress: number;
  gpu_device?: string;
  result_url?: string;
  priority: number;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  error_message?: string;
  statistics?: TaskStatistics;
}

export type TaskStatus =
  | 'pending'
  | 'pending_with_inference'
  | 'queued'
  | 'running'
  | 'paused'
  | 'completed'
  | 'failed'
  | 'cancelled';

export interface InputConfig {
  source: VideoSourceInput;
  resize?: ResizeConfig;
  roi?: ROIConfig;
  skip_frames: number;
  buffer_size: number;
  decode_threads: number;
}

export interface VideoSourceInput {
  type: 'local' | 'rtsp' | 'http' | 'https';
  id?: string;
  url?: string;
  auto_download: boolean;
  timeout: number;
}

export interface ResizeConfig {
  width: number;
  height: number;
  maintain_aspect: boolean;
}

export interface ROIConfig {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

export interface OutputConfig {
  type: 'file' | 'rtmp' | 'hls';
  path?: string;
  rtmp_url?: string;
  hls_dir?: string;
  format?: OutputFormatConfig;
}

export interface OutputFormatConfig {
  width?: number;
  height?: number;
  fps?: number;
  codec?: 'h264' | 'h265';
  bitrate?: string;
  gop_size?: number;
  profile?: string;
}

export interface ModelConfig {
  parallel: boolean;
  models: ModelItem[];
}

export interface ModelItem {
  name: string;
  config?: InferenceConfig;
  enabled: boolean;
  for_display: boolean;
  draw_config?: DrawConfig;
}

export interface InferenceConfig {
  confidence_threshold: number;
  iou_threshold: number;
  max_det: number;
  classes?: number[];
  device: string;
  batch_size: number;
  half_precision: boolean;
  track_objects: boolean;
}

export interface DrawConfig {
  draw_bbox: boolean;
  draw_mask: boolean;
  draw_label: boolean;
  draw_confidence: boolean;
  bbox_color: string;
  mask_alpha: number;
  line_thickness: number;
  font_scale: number;
  label_prefix?: string;
  z_order: number;
}

export interface TaskStatistics {
  frames_processed: number;
  frames_total: number;
  detections_count: number;
  avg_fps: number;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

export interface ApiResponse<T> {
  code: number;
  message: string;
  data?: T;
  request_id?: string;
}