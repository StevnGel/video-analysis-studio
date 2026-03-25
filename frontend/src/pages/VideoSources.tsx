import { useState, useEffect } from 'react'
import { Table, Button, Modal, Form, Input, Select, message, Typography } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import './VideoSources.css'

const { Title } = Typography
const { Option } = Select

interface VideoSource {
  id: string
  name: string
  type: 'file' | 'stream'
  url: string
  status: 'active' | 'inactive'
  description: string
  resolution: string
  framerate: number
  created_at: string
  updated_at: string
}

function VideoSources() {
  const [videoSources, setVideoSources] = useState<VideoSource[]>([])
  const [isModalVisible, setIsModalVisible] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [currentVideoSource, setCurrentVideoSource] = useState<VideoSource | null>(null)
  const [form] = Form.useForm()

  // 模拟数据
  useEffect(() => {
    const mockData: VideoSource[] = [
      {
        id: '1',
        name: '本地视频文件',
        type: 'file',
        url: '/path/to/video.mp4',
        status: 'active',
        description: '本地测试视频文件',
        resolution: '1920x1080',
        framerate: 30,
        created_at: '2023-12-01T10:00:00Z',
        updated_at: '2023-12-01T10:00:00Z'
      },
      {
        id: '2',
        name: 'RTSP 流',
        type: 'stream',
        url: 'rtsp://192.168.1.100:554/stream1',
        status: 'active',
        description: '网络摄像头 RTSP 流',
        resolution: '1280x720',
        framerate: 25,
        created_at: '2023-12-01T11:00:00Z',
        updated_at: '2023-12-01T11:00:00Z'
      }
    ]
    setVideoSources(mockData)
  }, [])

  const showAddModal = () => {
    setIsEditing(false)
    setCurrentVideoSource(null)
    form.resetFields()
    setIsModalVisible(true)
  }

  const showEditModal = (videoSource: VideoSource) => {
    setIsEditing(true)
    setCurrentVideoSource(videoSource)
    form.setFieldsValue(videoSource)
    setIsModalVisible(true)
  }

  const handleOk = () => {
    form.validateFields().then(values => {
      if (isEditing && currentVideoSource) {
        // 更新视频源
        const updatedVideoSources = videoSources.map(vs => 
          vs.id === currentVideoSource.id ? { ...vs, ...values } : vs
        )
        setVideoSources(updatedVideoSources)
        message.success('视频源更新成功')
      } else {
        // 添加视频源
        const newVideoSource: VideoSource = {
          id: Date.now().toString(),
          ...values,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
        setVideoSources([...videoSources, newVideoSource])
        message.success('视频源添加成功')
      }
      setIsModalVisible(false)
    })
  }

  const handleDelete = (id: string) => {
    const updatedVideoSources = videoSources.filter(vs => vs.id !== id)
    setVideoSources(updatedVideoSources)
    message.success('视频源删除成功')
  }

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => type === 'file' ? '文件' : '流'
    },
    {
      title: 'URL',
      dataIndex: 'url',
      key: 'url'
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => status === 'active' ? '活跃' : '非活跃'
    },
    {
      title: '分辨率',
      dataIndex: 'resolution',
      key: 'resolution'
    },
    {
      title: '帧率',
      dataIndex: 'framerate',
      key: 'framerate'
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: VideoSource) => (
        <div>
          <Button
            type="primary"
            icon={<EditOutlined />}
            size="small"
            style={{ marginRight: 8 }}
            onClick={() => showEditModal(record)}
          >
            编辑
          </Button>
          <Button
            danger
            icon={<DeleteOutlined />}
            size="small"
            onClick={() => handleDelete(record.id)}
          >
            删除
          </Button>
        </div>
      )
    }
  ]

  return (
    <div className="video-sources-container">
      <div className="page-header">
        <Title level={2}>视频源管理</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={showAddModal}>
          添加视频源
        </Button>
      </div>
      
      <Table 
        columns={columns} 
        dataSource={videoSources} 
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />
      
      <Modal
        title={isEditing ? "编辑视频源" : "添加视频源"}
        open={isModalVisible}
        onOk={handleOk}
        onCancel={() => setIsModalVisible(false)}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="名称"
            rules={[{ required: true, message: '请输入视频源名称' }]}
          >
            <Input placeholder="请输入视频源名称" />
          </Form.Item>
          <Form.Item
            name="type"
            label="类型"
            rules={[{ required: true, message: '请选择视频源类型' }]}
          >
            <Select placeholder="请选择视频源类型">
              <Option value="file">文件</Option>
              <Option value="stream">流</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="url"
            label="URL"
            rules={[{ required: true, message: '请输入视频源URL' }]}
          >
            <Input placeholder="请输入视频源URL" />
          </Form.Item>
          <Form.Item
            name="status"
            label="状态"
            rules={[{ required: true, message: '请选择视频源状态' }]}
          >
            <Select placeholder="请选择视频源状态">
              <Option value="active">活跃</Option>
              <Option value="inactive">非活跃</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="description"
            label="描述"
          >
            <Input.TextArea placeholder="请输入视频源描述" />
          </Form.Item>
          <Form.Item
            name="resolution"
            label="分辨率"
          >
            <Input placeholder="请输入分辨率，如 1920x1080" />
          </Form.Item>
          <Form.Item
            name="framerate"
            label="帧率"
          >
            <Input type="number" placeholder="请输入帧率" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default VideoSources
